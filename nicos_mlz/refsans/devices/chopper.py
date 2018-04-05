#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2018 by the NICOS contributors (see AUTHORS)
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
#   Jens Krüger <jens.krueger@frm2.tum.de>
#   Matthias Pomm <matthias.pomm@hzg.de>
#
# *****************************************************************************
"""Chopper related devices."""

from IO import StringIO

from nicos import session

from nicos.core import HasLimits, HasPrecision, Moveable, Override, Param, \
    dictwith, floatrange, intrange, listof, status
from nicos.core.errors import NicosError
from nicos.core.params import Attach, oneof
from nicos.devices.abstract import CanReference
from nicos.devices.taco.core import TacoDevice


class ChopperBase(TacoDevice, Moveable):

    taco_class = StringIO

    parameter_overrides = {
        'comtries': Override(default=1),
    }

    def _read_controller(self, mvalue):
        what = mvalue % self.chopper
        self.log.debug('_read_controller what: %s', what)
        res = self._taco_guard(self._dev.communicate, what)
        res = res.replace('\x06', '')
        self.log.debug('_read_controller res for %s: %s', what, res)
        return res

    def _write_controller(self, mvalue, *values):
        # TODO: fix formatting for single values and lists
        what = mvalue % ((self.chopper,) + values)
        self.log.debug('_read_controller what: %s', what)
        self._taco_guard(self._dev.writeLine, what)


class ChopperMaster(ChopperBase):

    valuetype = dictwith(rpm=float, disk2_Pos=intrange(1, 6),
                         angles=listof(float), wl_min=float, wl_max=float,
                         D=float)

    # attached_devices = {
    #    'choppers': Attach('Chopper chopper', ChopperDisc, multiple=6),
    # }

    parameters = {
        'mode': Param('Chopper operation mode (normal, virtual6)',
                      type=oneof('normal_mode', 'virtual_disc2_pos_6'),
                      settable=False, volatile=True)
    }

    _max_disks = 6
    attached_devices = {
        'chopper1': Attach('chopper1 speed', Moveable),
        'chopper2': Attach('chopper2 phase', Moveable),
        'chopper2_pos': Attach('chopper2 pos', Moveable),
        'chopper3': Attach('chopper3 phase also height', Moveable),
        'chopper4': Attach('chopper4 phase also height', Moveable),
        'chopper5': Attach('chopper5 phase half speed', Moveable),
        'chopper6': Attach('chopper6 phase half speed', Moveable),
        'chopper_mode': Attach('Modus Disc2_ pos, normal or '
                               'virtual_disc2_pos_6', Moveable),
        'shutter': Attach('Shutter device', Moveable),
    }

    def doInit(self, mode):
        self._devices_phase = (None, self._attached_chopper2,
                               self._attached_chopper3,
                               self._attached_chopper4,
                               self._attached_chopper5,
                               self._attached_chopper6)

    def doStart(self, target):
        if target['disk2_Pos'] == 6:
            self._attached_chopper_mode.move('virtual_disc2_pos_6')
            # self._attached_chopper_mode.move('virtual_pos_6')
        else:
            self._attached_chopper_mode.move('normal_mode')
            # chopper2_pos_akt = self._attached_choppers[2].pos.read()
            chopper2_pos_akt = self._attached_chopper2_pos.read()
            # TODO: Sequencer!
            if chopper2_pos_akt != target['disk2_Pos']:
                self.log.info('Stop chopper and move Disc2_pos from %d to %d!',
                              chopper2_pos_akt, target['disk2_Pos'])
                if self._attached_shutter.read(0) == 'open':
                    self._attached_shutter.maw('closed')
                if self._attached_chopper1.read(0) > 0:
                    self._attached_chopper1.maw(0)
                self.log.info('chopper stopped')
                self._attached_chopper2_pos.maw(target['disk2_Pos'])
                self.log.info('Disc2_pos %d reached!', target['disk2_Pos'])

        self.log.debug('angles %s', target['angles'])
        # TODO: Sequencer, because of needed wait time in doWritePhase
        for i, (dev, t) in enumerate(zip(self._devices_phase,
                                         target['angles'])):
            if dev:
                self.log.info('%d angle %.2f %s', i, t, dev)
                dev.phase = -t  # sign by history
        # self._attached_choppers[1].move(target['rpm'])
        self._attached_chopper1.move(target['rpm'])

    def doReadMode(self):
        return self._attached_chopper_mode.read(0)

    def doRead(self, maxage=0):
        try:
            value = self.target.copy()
        except AttributeError:
            value = {
                'D': None,
                'wl_min': None,
                'wl_max': None
            }
        value['disk2_Pos'] = self._attached_chopper2_pos.read(maxage)
        value['rpm'] = self._attached_chopper1.read(maxage)
        value['angles'] = [0]
        for i, dev in enumerate(self._devices_phase):
            if dev:
                angle = dev.read(maxage)
                self.log.debug('%d angle %.2f %s', i, angle, dev)
                value['angles'].append(angle)
        self.log.debug('value chopper %s', value)
        return value

    def doStatus(self, maxage=0):
        # TODO implement other possible states
        return self._attached_chopper1.status(maxage)
        # return status.OK, 'idle'


class ChopperDisc(HasPrecision, HasLimits, ChopperBase):

    parameters = {
        'phase': Param('Phase of chopper',
                       type=floatrange(-180, 180),
                       settable=True,
                       volatile=True, userparam=True),
        'current': Param('motor current',
                         settable=False,
                         volatile=True,
                         userparam=True),
        'mode': Param('Internal mode',
                      type=int,
                      settable=False,
                      volatile=True,
                      userparam=True),
        'chopper': Param('chopper number inside controller',
                         type=intrange(1, 6),
                         settable=False,
                         userparam=True,
                         default=2),
        'reference': Param('reference to Disc one',
                           type=floatrange(-360, 360),
                           settable=False,
                           userparam=True),
        'gear': Param('Chopper ratio',
                      type=intrange(-6, 6),
                      settable=False,
                      userparam=True,
                      default=0),
        'edge': Param('Chopper edge of neutron window',
                      type=oneof('open', 'close'),
                      settable=False,
                      userparam=True),
    }

    parameter_overrides = {
        'unit': Override(default='rpm'),
        'precision': Override(default=2),
        'abslimits': Override(default=(0, 6000), mandatory=False),
    }

    def doStart(self, target):
        if self.chopper == 1 and self.gear == 0:
            self._write_controller('m4073=%d m4074=%d m4075=0 m4076=0 m4070=7',
                                   int(round(target)))
        else:
            self.log.debug('target %d', target)
            self.log.warning('nothing changed chopper:%d gear:%d edge:%s',
                             self.chopper, self.gear, self.edge)

    def doRead(self, maxage=0):
        return self._current_speed()

    def doReadCurrent(self):
        # res = int(self._read_controller('m%s68'))  # peak current
        res = int(self._read_controller('m420%s'))  # averaged current
        res /= 1000.0
        self.log.debug('current: %d', res)
        return res

    def doReadMode(self):
        res = int(self._read_controller('m414%s'))
        self.log.debug('mode: %d', res)
        return res

    def doReadPhase(self):
        res = int(self._read_controller('m410%s'))
        self.log.debug('phase: %d', res)
        if res == 99999:
            return 0
        return res / 100.

    def doWritePhase(self, value):
        # off = self.offsets[disk] - self.offsets[1]
        set_to = value + self.reference
        self.log.info('Disk %d angle %0.2f Phase %0.2f gear %d ref %.2f',
                      self.chopper, value, set_to, self.gear, self.reference)
        set_to = int(round(set_to * 100))
        while set_to > +18000:
            set_to -= 36000
        while set_to < -18000:
            set_to += 36000
        self.log.info('Disk %d Phase %d gear %d', self.chopper, set_to,
                      self.gear)
        # TODO: Check the following lines
        self._write_controller('m4073=%d m4074=0 m4075=%d m4076=%d m4070=7',
                               value, self.gear)
        session.delay(10)  # time needed to take over the phase!!!

    def doStatus(self, maxage=0):
        if self.doIsAtTarget(self.doRead(0)) or self.chopper != 1:
            return status.OK, ''
        return status.BUSY, 'moving'

    def _current_speed(self):
        res = float(self._read_controller('m408%s'))
        self.log.debug('speed: %f', res)
        return res


class ChopperDisc2Pos(CanReference, ChopperBase):
    """Position of chopper disc 2 along the x axis"""

    valuetype = oneof(0, 1, 2, 3, 4, 5, 99)

    def doRead(self, maxage=0):
        what = 'm4078'
        self.log.debug('what: %s', what)
        res = self._taco_guard(self._dev.communicate, what)
        res = int(res.replace('\x06', ''))
        self.log.debug('pos: %d', res)
        return res

    def doStart(self, value):
        value = intrange(1, 5)(value)
        self.log.info('requested position %d', value)
        what = 'm4077=%d' % value
        self.log.debug('doWritePos what: %s', what)
        res = self._taco_guard(self._dev.writeLine, what)
        self.log.debug('doWritePos res: %d', res)

    def doStatus(self, maxage=0):
        try:
            res = self.doRead(maxage)
            if res != 99:
                self.log.info('doStatus: %d', res)
            if res == 0:
                return status.ALARM, 'device not referenced'
            elif res == 99:
                self.log.debug('doStatus: %d', res)
                return status.BUSY, 'moving'
            elif 1 <= res <= 5:
                return status.OK, ''
            return status.ERROR, 'Unknown status from read(): %d' % res
        except NicosError as e:
            return status.ERROR, '%s' % e

    def doReference(self, *args):
        self.doStart(1)
