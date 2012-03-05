#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2012 by the NICOS contributors (see AUTHORS)
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
#   Georg Brandl <georg.brandl@frm2.tum.de>
#
# *****************************************************************************

"""NICOS temperature controller classes."""

__version__ = "$Revision$"

import time

import TACOStates
import Temperature

from nicos.core import status, oneof, Param, Readable, Moveable, HasOffset, \
     HasLimits, TimeoutError
from nicos.taco.core import TacoDevice


class TemperatureSensor(TacoDevice, Readable):
    """TACO temperature sensor device."""
    taco_class = Temperature.Sensor


class TemperatureController(TacoDevice, HasLimits, HasOffset, Moveable):
    """TACO temperature controller device."""
    taco_class = Temperature.Controller

    parameters = {
        'setpoint':  Param('Current temperature setpoint', unit='main',
                           category='general'),
        'mode':      Param('Control mode (manual, zone or openloop)',
                           type=oneof('manual', 'zone', 'openloop'),
                           settable=True),
        'p':         Param('The P control parameter', settable=True,
                           type=float, category='general'),
        'i':         Param('The I control parameter', settable=True,
                           type=float, category='general'),
        'd':         Param('The D control parameter', settable=True,
                           type=float, category='general'),
        'ramp':      Param('Temperature ramp in K/min', unit='K/min',
                           settable=True),
        'tolerance': Param('The window\'s temperature tolerance', unit='K',
                           settable=True, category='general'),
        'window':    Param('Time window for checking stable temperature',
                           unit='s', settable=True, category='general'),
        'loopdelay': Param('Sleep time when waiting', unit='s', default=1,
                           settable=True),
        'timeout':   Param('Maximum time to wait for stable temperature',
                           unit='s', settable=True),
        'timeoutaction':  Param('What to do when a timeout occurs',
                                type=oneof('continue', 'raise'), settable=True),
        'controlchannel': Param('Control channel, possible values depend '
                                'on the type of device',
                                type=str, category='general', settable=True),
    }

    def doRead(self):
        return self._taco_guard(self._dev.read) - self.offset

    def doStart(self, target):
        if self.status()[0] == status.BUSY:
            self.log.debug('stopping running temperature change')
            self._taco_guard(self._dev.stop)
        self._taco_guard(self._dev.write, target + self.offset)
        self._pollParam('setpoint', 100)

    def doStop(self):
        self._taco_guard(self._dev.stop)

    def doStatus(self):
        state = self._taco_guard(self._dev.deviceState)
        if state == TACOStates.MOVING:
            return (status.BUSY, 'moving')
        elif state in [TACOStates.PRESELECTION_REACHED,
                       TACOStates.DEVICE_NORMAL]:
            return (status.OK, TACOStates.stateDescription(state))
        elif state == TACOStates.UNDEFINED:
            return (status.NOTREACHED, 'temperature not reached')
        else:
            return (status.ERROR, TACOStates.stateDescription(state))

    def doWait(self):
        delay = self.loopdelay
        # while 1:
        #     v = self.read()
        #     self.log.debug('current temperature %7.3f %s' % (v, self.unit))
        #     s = self.status()[0]
        #     if s == status.OK:
        #         return v
        #     elif s == status.ERROR:
        #         raise CommunicationError(self, 'device in error state')
        #     elif s == status.NOTREACHED:
        #         raise TimeoutError(self, 'temperature not reached in %s seconds'
        #                            % self.timeout)
        #     time.sleep(delay)
        tolerance = self.tolerance
        setpoint = self.target
        window = self.window
        timeout = self.timeout
        self.log.debug('wait time =  %d' % timeout)
        if self.ramp != 0.:
             timeout += 60 * abs(self.read() - setpoint) / self.ramp
        self.log.debug('wait time =  %d' % timeout)
        firststart = started = time.time()
        while 1:
            # XXX read() or read(0)
            value = self.read()
            now = time.time()
            self.log.debug('%7.0f s: current temperature %7.3f %s' %
                           ((now - firststart), value, self.unit))
        #   s = self.status()[0]
        #   if s == status.OK:
        #         return v
        #   elif s == status.ERROR:
        #         raise CommunicationError(self, 'device in error state')
        #   elif s == status.NOTREACHED:
        #         raise TimeoutError(self, 'temperature not reached in %s seconds'
        #                            % self.timeout)
            if abs(value - setpoint) > tolerance:
                # start again
                started = now
            elif now > started + window:
                return value
            if now - firststart > timeout:
                if self.timeoutaction == 'raise':
                    raise TimeoutError(self, 'temperature not reached in '
                                       '%s seconds' % timeout)
                else:
                    self.log.warning('temperature not reached in %s seconds, '
                                     'continuing anyway' % timeout)
                    return
            time.sleep(delay)

    def doReset(self):
        self._taco_guard(self._dev.deviceReset)

    def doPoll(self, n):
        if self.ramp:
            self._pollParam('setpoint', 1)
        if n % 100 == 0:
            self._pollParam('setpoint', 100)
            self._pollParam('p')
            self._pollParam('i')
            self._pollParam('d')

    def doReadSetpoint(self):
        return self._taco_guard(self._dev.setpoint) - self.offset

    def doReadP(self):
        return self._taco_guard(self._dev.pParam)

    def doReadI(self):
        return self._taco_guard(self._dev.iParam)

    def doReadD(self):
        return self._taco_guard(self._dev.dParam)

    def doReadRamp(self):
        return self._taco_guard(self._dev.ramp)

    def doReadTolerance(self):
        return float(self._taco_guard(self._dev.deviceQueryResource,
                                      'tolerance'))

    def doReadWindow(self):
        return float(self._taco_guard(self._dev.deviceQueryResource,
                                      'window')[:-1])

    def doReadTimeout(self):
        return float(self._taco_guard(self._dev.deviceQueryResource,
                                      'timeout')[:-1])

    def doReadControlchannel(self):
        return self._taco_guard(self._dev.deviceQueryResource, 'channel')

    def doReadMode(self):
        modes = {1: 'manual', 2: 'zone', 3: 'openloop'}
        return modes[int(self._taco_guard(
            self._dev.deviceQueryResource, 'defaultmode')[:-1])]

    def doWriteP(self, value):
        self._taco_guard(self._dev.setPParam, value)

    def doWriteI(self, value):
        self._taco_guard(self._dev.setIParam, value)

    def doWriteD(self, value):
        self._taco_guard(self._dev.setDParam, value)

    def doWriteRamp(self, value):
        self._taco_guard(self._dev.setRamp, value)

    def doWriteTolerance(self, value):
        # writing the "tolerance" resource is only allowed when stopped
        self._taco_guard(self._dev.stop)
        self._taco_update_resource('tolerance', str(value))

    def doWriteWindow(self, value):
        # writing the "window" resource is only allowed when stopped
        self._taco_guard(self._dev.stop)
        self._taco_update_resource('window', str(value))

    def doWriteTimeout(self, value):
        # writing the "timeout" resource is only allowed when stopped
        self._taco_guard(self._dev.stop)
        self._taco_update_resource('timeout', str(value))

    def doWriteControlchannel(self, value):
        # writing the "channel" resource is only allowed when stopped
        self._taco_guard(self._dev.stop)
        self._taco_update_resource('channel', value)

    def doWriteMode(self, value):
        modes = {'manual': 1, 'zone': 2, 'openloop': 3}
        # writing the "mode" resource is only allowed when stopped
        self._taco_guard(self._dev.stop)
        self._taco_update_resource('defaultmode', modes[value])
