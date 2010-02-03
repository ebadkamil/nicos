#  -*- coding: utf-8 -*-
# *****************************************************************************
# Module:
#   $Id $
#
# Description:
#   NICOS TACO counter/timer definition
#
# Author:
#   Georg Brandl <georg.brandl@frm2.tum.de>
#
#   The basic NICOS methods for the NICOS daemon (http://nicos.sf.net)
#
#   Copyright (C) 2009 Jens Krüger <jens.krueger@frm2.tum.de>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# *****************************************************************************

"""
Implementation of TACO Timer and Counter devices.
"""

__author__  = "$Author $"
__date__    = "$Date $"
__version__ = "$Revision $"

from time import sleep

import IOCommon
import TACOStates
from IO import Timer as IOTimer, Counter as IOCounter

from nicm import status
from nicm.device import Countable
from nicm.errors import ConfigurationError
from taco.base import TacoDevice
from taco.errors import taco_guard


class TacoCountable(TacoDevice, Countable):
    """Base class for TACO countables."""

    parameters = {
        'ismaster': (False, False, 'Whether the device is the master counter.'),
        'preselection': (1, False, 'Default preselection register value.'),
        'mode': (0, False, 'Run mode for the countable.'),
        'loopdelay': (0.3, False, 'Wait loop delay in seconds.'),
    }

    def doInit(self):
        TacoDevice.doInit(self)
        # flag to distinguish pause from stop
        self.__stopped = False

    def doStart(self, preset=None):
        self.__stopped = False
        if preset is not None:
            self.setPreselection(preset)
        taco_guard(self._dev.start)

    def doStop(self):
        self.__stopped = True
        taco_guard(self._dev.stop)

    def doResume(self):
        self.__stopped = False
        taco_guard(self._dev.resume)

    def doWait(self):
        while self.status() == status.BUSY:
            sleep(self.getLoopdelay())

    def doClear(self):
        self.__stopped = False
        taco_guard(self._dev.stop)
        taco_guard(self._dev.clear)

    def doStatus(self):
        state = taco_guard(self._dev.deviceState)
        if state == TACOStates.PRESELECTION_REACHED:
            return status.OK
        elif state == TACOStates.STOPPED:
            if self.__stopped:
                return status.OK
            else:
                return status.PAUSED
        elif state == TACOStates.COUNTING:
            return status.BUSY
        return status.ERROR

    def doGetPreselection(self):
        return taco_guard(self._dev.preselection)

    def doSetPreselection(self, value):
        taco_guard(self._dev.setPreselection, value)

    def doGetIsmaster(self):
        return taco_guard(self._dev.isMaster)

    def doSetIsmaster(self, value):
        taco_guard(self._dev.enableMaster, bool(value))

    def doGetMode(self):
        mode = taco_guard(self._dev.mode)
        return {
            IOCommon.MODE_NORMAL: 'normal',
            IOCommon.MODE_RATEMETER: 'ratemeter',
            IOCommon.MODE_PRESELECTION: 'preselection',
        }[mode]

    def doSetMode(self, value):
        try:
            newmode = {'normal': IOCommon.MODE_NORMAL,
                       'ratemeter': IOCommon.MODE_RATEMETER,
                       'preselection': IOCommon.MODE_PRESELECTION,
                       }[value]
        except KeyError:
            raise ConfigurationError('%s: mode %r invalid' % (self, value))
        taco_guard(self._dev.setMode, newmode)
            

class Timer(TacoCountable):
    taco_class = IOTimer


class Counter(TacoCountable):
    taco_class = IOCounter
