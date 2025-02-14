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
#   Nikhil Biyani <nikhil.biyani@psi.ch>
#
# *****************************************************************************

"""
This module contains ESS specific Base classes for EPICS.
"""

from kafka.errors import KafkaError

from nicos import session
from nicos.core import Override, Param
from nicos.core.constants import SIMULATION
from nicos.core.errors import ConfigurationError
from nicos.devices.epics import EpicsAnalogMoveable, EpicsDevice, \
    EpicsDigitalMoveable, EpicsMoveable, EpicsReadable, EpicsStringReadable, \
    EpicsWindowTimeoutDevice


class EpicsDeviceEss(EpicsDevice):
    """ Base class for EPICS Device to be used in the ESS instrument devices.
    The ESS device has functionality to write and read PVs from Kafka topics.
    """
    parameters = {
        'devicepvtopic': Param(
            'Default topic for device where PVs are to be forwarded',
            type=str, userparam=False),
        'devicepvschema': Param('Default flatbuffers coding schema for device',
                                type=str, userparam=False),
        'pvdetails': Param(
            'Dict of specific PV and tuple of (topic, schema) if is different',
            type=dict, userparam=False),
    }

    def _get_record_fields(self):
        return {}

    def doPreinit(self, mode):
        self._record_fields = self._get_record_fields()
        EpicsDevice.doPreinit(self, mode)

        pv_details = {}
        # Get topics for each PV
        for pvparam in self._get_pv_parameters():
            topic = self.devicepvtopic if self.devicepvtopic else ''
            schema = self.devicepvschema if self.devicepvschema else ''
            pv = self._get_pv_name(pvparam)
            if self.pvdetails and pv in self.pvdetails:
                topic, schema = self.pvdetails[pv]
            pv_details[pv] = (topic, schema)

        # Configure the forwarder if the KafkaForwarder is available
        # Get the forwarded topic and schema for the PV
        try:
            forwarder = session.getDevice('KafkaForwarder')
        except ConfigurationError:
            return
        except KafkaError as ke:
            session.log.error('KafkaForwarder badly configured: %s', ke)
            return
        if mode != SIMULATION:
            try:
                forwarder.add(pv_details)
            except ConfigurationError as error:
                session.log.error("Couldn't add device to KafkaForwarder: %s",
                                  error)


class EpicsReadableEss(EpicsDeviceEss, EpicsReadable):
    parameter_overrides = {
        'fmtstr': Override(userparam=False),
        'maxage': Override(userparam=False),
        'pollinterval': Override(userparam=False),
        'warnlimits': Override(userparam=False)
    }

    def doPreinit(self, mode):
        EpicsDeviceEss.doPreinit(self, mode)
        EpicsReadable.doPreinit(self, mode)


class EpicsStringReadableEss(EpicsDeviceEss, EpicsStringReadable):

    parameter_overrides = {
        'readpv': Override(userparam=False)
    }

    def doPreinit(self, mode):
        EpicsDeviceEss.doPreinit(self, mode)
        EpicsStringReadable.doPreinit(self, mode)


class EpicsMoveableEss(EpicsDeviceEss, EpicsMoveable):
    parameter_overrides = {
        'fmtstr': Override(userparam=False),
        'maxage': Override(userparam=False),
        'pollinterval': Override(userparam=False),
        'warnlimits': Override(userparam=False)
    }

    def doPreinit(self, mode):
        EpicsDeviceEss.doPreinit(self, mode)
        EpicsMoveable.doPreinit(self, mode)


class EpicsAnalogMoveableEss(EpicsDeviceEss, EpicsAnalogMoveable):
    parameter_overrides = {
        'fmtstr': Override(userparam=False),
        'maxage': Override(userparam=False),
        'pollinterval': Override(userparam=False),
        'warnlimits': Override(userparam=False)
    }

    def doPreinit(self, mode):
        EpicsDeviceEss.doPreinit(self, mode)
        EpicsAnalogMoveable.doPreinit(self, mode)


class EpicsDigitalMoveableEss(EpicsDeviceEss, EpicsDigitalMoveable):
    parameter_overrides = {
        'fmtstr': Override(userparam=False),
        'maxage': Override(userparam=False),
        'pollinterval': Override(userparam=False),
        'warnlimits': Override(userparam=False)
    }

    def doPreinit(self, mode):
        EpicsDeviceEss.doPreinit(self, mode)
        EpicsDigitalMoveable.doPreinit(self, mode)


class EpicsWindowTimeoutDeviceEss(EpicsDeviceEss, EpicsWindowTimeoutDevice):
    parameter_overrides = {
        'fmtstr': Override(userparam=False),
        'maxage': Override(userparam=False),
        'pollinterval': Override(userparam=False),
        'warnlimits': Override(userparam=False)
    }

    def doPreinit(self, mode):
        EpicsDeviceEss.doPreinit(self, mode)
        EpicsWindowTimeoutDevice.doPreinit(self, mode)
