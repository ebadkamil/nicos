#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2017 by the NICOS contributors (see AUTHORS)
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

"""Generic device classes using hardware-specific attached devices."""

# backwards compatibility for config files
from nicos.core.device import DeviceAlias, NoDevice

from nicos.devices.generic.axis import Axis
from nicos.devices.generic.cache import CacheReader, CacheWriter
from nicos.devices.generic.detector import ActiveChannel, CounterChannelMixin,\
    Detector, DetectorForecast, GatedDetector, ImageChannelMixin, \
    PassiveChannel, RectROIChannel, TimerChannelMixin, ScanningDetector
from nicos.devices.generic.magnet import BipolarSwitchingMagnet, \
    CalibratedMagnet
from nicos.devices.generic.manual import ManualMove, ManualSwitch
from nicos.devices.generic.oscillator import Oscillator
from nicos.devices.generic.paramdev import ParamDevice, ReadonlyParamDevice
from nicos.devices.generic.pulse import Pulse
from nicos.devices.generic.sequence import BaseSequencer, LockedDevice
from nicos.devices.generic.slit import Slit, TwoAxisSlit
from nicos.devices.generic.switcher import MultiSwitcher, ReadonlySwitcher, \
    Switcher
from nicos.devices.generic.system import FreeSpace
from nicos.devices.generic.virtual import VirtualCoder, VirtualCounter, \
    VirtualImage, VirtualMotor, VirtualRealTemperature, \
    VirtualScanningDetector, VirtualTemperature, VirtualTimer
