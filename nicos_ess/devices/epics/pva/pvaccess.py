#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2021 by the NICOS contributors (see AUTHORS)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Matt Clarke <matt.clarke@ess.eu>
#
# *****************************************************************************
from functools import partial

import numpy as np
import pvaccess

from nicos.core import CommunicationError, status
from nicos.devices.epics import SEVERITY_TO_STATUS


class PvapyWrapper:
    def __init__(self, use_pva=True, timeout=3.0):
        self.protocol = pvaccess.PVA if use_pva else pvaccess.CA
        self._channels = {}
        self._subscriptions = {}
        self._timeout = timeout

    def connect_pv(self, pvname):
        # Check pv is available
        try:
            self._get_current_value(pvname)
        except TimeoutError:
            raise CommunicationError(f'could not connect to PV {pvname}')
        return pvname

    def _get_current_value(self, pvname):
        chan = self._get_channel(pvname)
        result = chan.get()
        return result

    def _get_channel(self, pvname):
        # Can only create one connection to any particular PV
        if pvname in self._channels:
            return self._channels[pvname]
        chan = pvaccess.Channel(pvname, self.protocol)
        chan.setTimeout(self._timeout)
        self._channels[pvname] = chan
        return chan

    def get_pv_value(self, pvname, as_string=False):
        result = self._get_current_value(pvname)
        return self._convert_value(result['value'], as_string)

    def _convert_value(self, value, as_string=False):
        if isinstance(value, dict) and 'choices' in value:
            index = value['index']
            if as_string:
                return value['choices'][index]
            return index
        if as_string:
            if isinstance(value, np.ndarray):
                return value.tobytes().decode()
            return str(value)
        return value

    def put_pv_value(self, pvname, value, wait=False):
        chan = self._get_channel(pvname)
        chan.put(value)
        # TODO: how to wait?

    def put_pv_value_blocking(self, pvname, value, update_rate=0.1,
                              block_timeout=60):
        # if wait is set it will block until the value is set or it
        # times out
        # TODO: how to wait?
        chan = self._get_channel(pvname)
        chan.put(value)

    def get_pv_type(self, pvname):
        result = self._get_current_value(pvname)

        if isinstance(result['value'], dict) and 'choices' in result['value']:
            # Treat enums as ints
            return int
        return type(result['value'])

    def get_alarm_status(self, pvname):
        result = self._get_channel(pvname).get('alarm')
        return self._extract_alarm_info(result)

    def get_units(self, pvname, default=''):
        result = self._get_channel(pvname).get('display')
        if 'display' in result:
            return result['display']['units']
        return default

    def get_limits(self, pvname, default_low=-1e308, default_high=1e308):
        result = self._get_channel(pvname).get('display')
        if 'display' in result:
            default_low = result['display']['limitLow']
            default_high = result['display']['limitHigh']
        return default_low, default_high

    def get_control_values(self, pvname):
        result = self._get_channel(pvname).get('display')
        if 'display' in result:
            return result['display']
        result = self._get_channel(pvname).get('control')
        return result['control'] if 'control' in result else {}

    def get_value_choices(self, pvname):
        # Only works for enum types like MBBI and MBBO
        result = self._get_current_value(pvname)
        if isinstance(result['value'], dict) and 'choices' in result['value']:
            return result['value']['choices']
        return []

    def subscribe(self, pvname, pvparam, change_callback,
                  connection_callback=None, as_string=False):
        """
        Create a monitor subscription to the specified PV.

        :param pvname: The PV name.
        :param pvparam: The associated NICOS parameter
            (e.g. readpv, writepv, etc.).
        :param change_callback: The function to call when the value changes.
        :param connection_callback: The function to call when the connection
            status changes.
        :param as_string: Whether to return the value as a string.
        :return: the subscription object (must be assigned).
        """
        # Only subscribe once to any particular PV
        if pvname in self._subscriptions:
            return

        pv_callback = partial(self._pv_callback, pvname, pvparam,
                              change_callback, as_string)
        conn_callback = partial(self._conn_callback, pvname, pvparam,
                                connection_callback)

        chan = self._get_channel(pvname)
        chan.setMonitorMaxQueueLength(10)
        chan.subscribe(pvname, pv_callback)
        chan.setConnectionCallback(conn_callback)
        chan.startMonitor()
        self._subscriptions[pvname] = chan
        return chan

    def _pv_callback(self, name, pvparam, change_callback, as_string, result):
        if change_callback:
            value = self._convert_value(result['value'], as_string)
            if 'alarm' in result:
                severity, message = self._extract_alarm_info(result)
            else:
                # CA requires us to query the alarm manually for some fields
                severity, message = self.get_alarm_status(name)
            change_callback(name, pvparam, value, severity, message)

    def _extract_alarm_info(self, value):
        # The EPICS 'severity' matches to the NICOS `status` and the message has
        # a short description of the alarm details.
        try:
            severity = SEVERITY_TO_STATUS[value['alarm']['severity']]
            message = value['alarm']['message']
            return severity, '' if message == 'NO_ALARM' else message
        except KeyError:
            return status.UNKNOWN, 'alarm information unavailable'

    def _conn_callback(self, name, pvparam, conn_callback, result):
        conn_callback(name, pvparam, result)

    def close_subscription(self, subscription):
        if subscription:
            subscription.stopMonitor()
