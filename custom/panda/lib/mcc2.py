#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2013 by the NICOS contributors (see AUTHORS)
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
#   Enrico Faulhaber <enrico.faulhaber@frm2.tum.de>
#   Petr Cermak <p.cermak@fz-juelich.de>
#
# *****************************************************************************

"""PANDA MCC2 Interface for foci control and support for mono-changer"""

from IO import StringIO

from nicos.core import status, intrange, floatrange, oneofdict, oneof, \
     usermethod, Param, CommunicationError, HardwareError, \
     Device, Readable
from nicos.utils import lazy_property
from nicos.devices.abstract import Motor as NicosMotor, Coder as NicosCoder
from nicos.devices.taco import TacoDevice


class TacoSerial(TacoDevice, Device):
    taco_class = StringIO
    def communicate(self, what):
        return self._taco_guard(self._dev.communicate, what)


class MCC2core(Device):
    """Class for comunication with MCC"""
    attached_devices = {
        'bus' : (TacoSerial, 'The Serial connection to the phytron Box'),
    }
    parameters = {
        'channel'       : Param('Channel of MCC2 to use (X or Y)',
                            type = oneof('X', 'Y'), default = 'Y',
                            prefercache = False),
        'addr'          : Param('address of MCC2 to use (0 to 15)',
                            type = intrange(0, 15), default = 0,
                            prefercache = False),
        'temperature'   : Param('temperature of MCC-2 unit in °C',
                            type = int, settable=False, volatile=True),
    }

    @lazy_property
    def bus(self):
        return self._adevs['bus']

    def comm(self, cmd, forcechannel=True):
        if forcechannel:
            cmd = cmd.replace('X', self.channel).replace('Y', self.channel)
        self.log.debug('comm: %r' % cmd)
        temp = self.bus.communicate('\x02' + hex(self.addr)[-1] + cmd + '\x03')
        if len(temp) >= 2 and temp[0] == '\x02':   #strip beginning STX
            temp = temp[1:]
            if temp[-1] == '\x03': #strip optional ending stx
                temp = temp[:-1]
            if temp[0] == '\x06':
                self.log.debug('  ->: %r' % temp)
                return temp[1:]
            else:
                self.log.debug('  ->: None')
                return None     # no ACK means nothing good!
        raise CommunicationError(self, 'Response timed out')

    def doInit(self, mode):
        if mode != 'simulation':
            if not self.comm('IVR').startswith('MCC'):
                raise CommunicationError(self, 'No Response from Phytron, please check!')
            self._pushParams()
            self.doReset()

    def doReadTemperature(self):
        return int(self.comm('XP49R'))

    @usermethod
    def store(self):
        return self.comm('SA')

    def _pushParams(self):
        """Pushes configured params from the setup files to the hardware"""
        t = self._config
        for k,v in t.iteritems():
            m = getattr(self, 'doWrite' + k.title(), None)
            if m:
                self.log.debug(self, 'Setting %r to %r'%(k, v))
                m(v)

    def doReset(self):
        pass


class MCC2Monoframe(MCC2core, Readable):
    """Class for the readout of a Mcc2 unit

    Wiring info:
    8 inputs are connected as follows:
    E1 = mono_id1_h     E5 = mono_id1_v
    E2 = mono_id2_h     E6 = mono_id2_v
    E3 = mono_id3_h     E7 = mono_id3_v
    E4 = <unused>       E8 = <unused>

    8 outputs are connected as follows:
    A1 = LED_Cu         A5 = <unused>
    A2 = LED_Si         A6 = <unused>
    A3 = LED_Heusler    A7 = <unused>
    A4 = LED_PG         A8 = connected to Motor_driver_enable via inhibit box

    """
    parameters = {
        'driverenable' : Param('Enable pin (Output 8)', type = bool,
                                mandatory = False, settable = True, default = False,
                                prefercache = False),
    }

    monocodes = {   # input triple : (led_num, name)
             '000' : (None, 'empty'),
             '111' : (1,    'Cu'),
             '011' : (2,    'Si'),
             '101' : (3,    'Heusler'),
             '110' : (4,    'PG'),
    }

    def doRead(self, maxage=0):
        self.comm('A1R2R3R4R') #all LEDs off

        monoh = self.comm('ER1;2;3')
        self.log.debug(self, 'mono_h code is ' + monoh)

        monov = self.comm('ER5;6;7')
        self.log.debug(self, 'mono_v code is ' + monov)

        if monoh != monov:
            raise HardwareError(self, 'monocodes from MFV and MFH are different!')

        if monoh in self.monocodes:
            #set LED
            led = self.monocodes[monoh][0]
            if led:
                self.comm('A%dS' % led)
            else:
                self.comm('A1S2S3S4S') # set all to indicate empty to distinguish from no power....
            return self.monocodes[monoh][1]
        else:
            raise HardwareError(self, 'unknown monochromator or wires broken')

    def doStatus(self, maxage=0):
        try:
            _ = self.doRead(maxage)
            return (status.OK, 'idle')
        except HardwareError, e:
            return (status.ERROR, str(e))

    # following activates only half of enable switch,
    # second part is connected to inhibit box
    def doReadDriverenable(self):
        return bool(self.comm('AR8'))

    def doWritedriverenable(self, value):
        if value:
            self.comm('A8S')
        else:
            self.comm('A8R')

    def doReset(self):
        self.comm('XMD')     # disable output
        self.comm('A08R')    # disable enable_pin



class MCC2Coder(MCC2core, NicosCoder):
    """Class for the readout of a MCC2-coder"""

    codertypes = ('none', 'incremental', 'ssi-binary', 'ssi-gray')

    parameters = {
        'slope'     : Param('coder units per degree of rotation', type = float,
                             default = 1, settable = True, unit = '1/main', prefercache = False),
        'zerosteps' : Param('coder steps at physical zero',type = int,
                             default = 0, settable = True, prefercache = False),
        'codertype' : Param('type of encoder', type = oneof(*codertypes),
                             default = 'none', settable = True, prefercache = False),
        'coderbits' : Param('number of bits of ssi-encoder', default = 0,
                             type = intrange(0, 31), settable = True, prefercache = False),
    }


    def doReset(self):
        self.comm('XP39S1') #encoder conversion factor set to 1

    def doReadCoderbits(self):
        return int(self.comm('XP35R'))

    def doWriteCoderbits(self, value):
        return self.comm('XP35S%d' % int(value))

    def doReadCodertype(self):
        return self.codertypes[int(self.comm('XP34R'))]

    def doWriteCodertype(self, value):
        return self.comm('XP34S%d' % self.codertypes.index(value))

    def doRead(self, maxage=0):
        return (float(self.comm('XP22R')) - self.zerosteps) / self.slope

    def doSetPosition(self,pos):
        self.comm('XP22S%d'%int(float(pos)*self.slope+self.zerosteps))
        return self.doRead()



class MCC2Poti(MCC2core, NicosCoder):
    """Class for the readout of a MCC2-A/D converter"""

    parameters = {
        'slope'     : Param('coder units per degree of rotation', type = float,
                             default = 1, settable = True, unit = '1/main', prefercache = False),
        'zerosteps' : Param('coder steps at physical zero',type = int,
                             default = 0, settable = True, prefercache = False),
        'coderbits' : Param('number of bits of ssi-encoder', default = 10,
                             type = int, settable = False, mandatory = False, prefercache = False),
    }

    def doRead(self, maxage=0):
        r = 'AD1R' if self.channel == 'X' else 'AD2R'
        return (float(self.comm(r)) - self.zerosteps) / self.slope

    def doSetPosition(self, pos):
        self.log.warning(self, 'No setPosition available! Request ignored....')
        return self.doRead(0)



class MCC2Motor(MCC2core, NicosMotor):
    """Class for the control of the MCC2-Stepper"""

    movementTypes = ('rotational', 'linear')

    parameters = {
        'mccmovement' : Param('Type of movement, change behaviour of limit switches',
                               type = oneof(*movementTypes), default = 'linear',
                               settable = True, prefercache = False),
        'slope'       : Param('Full motor steps per physical unit',
                               type = float, default = 1, unit = '1/main', prefercache = False),
        'power'       : Param('Internal power stage switch', default = 'on',
                               type = oneofdict({0: 'off', 1: 'on'}),
                               settable = True, volatile = True),
        'steps'       : Param('Last position in steps', settable = True,
                               type = int, prefercache = False),
        'accel'       : Param('Motor acceleration in physical units', prefercache = False,
                               type = float, settable = True, unit = '1/main**2'),
        'microstep'   : Param('Microstepping mode', unit = 'microsteps/fullstep',
                               type = intrange(1, 255), settable = True, prefercache = False),
        'idlecurrent' : Param('Current whenever motor is Idle', unit = 'A',
                               type = floatrange(0, 2.5), settable = True, prefercache = False),
        'rampcurrent' : Param('Current whenever motor is Ramping', unit = 'A',
                               type = floatrange(0, 2.5), settable = True, prefercache = False),
        'movecurrent' : Param('Current whenever motor is moving at speed',
                               type = floatrange(0, 2.5), unit = 'A', prefercache = False,
                               settable = True),
        'linear'      : Param('linear stage (as opposed to choppered stage)',
                               type = bool, settable=False, volatile = True),
    }

    def doReset( self ):
        self.comm('XP02S1')  # unit = steps
        self.comm('XP03S1')  # unity slope
        self.comm('XP04S20') # lowest frequency which is Ok whithout ramp
        self.comm('XP17S2') # ramping uses boostcurrent
        self.comm('XP25S0') # no backlash correction, this is done in the axis code
        self.comm('XP27S0') # Limit switches are openers (normally closed=n.c.)

    def doReadMccmovement(self):
        return self.movementTypes[int(self.comm('XP01R'))]

    def doWriteMccmovement(self, value):
        return self.comm('XP01S%d' % (self.movementTypes.index(value)))

    def doReadLinear(self):
        return int(self.comm('XP48R')) == 1

    def doReadIdlecurrent(self):
        if self.linear:
            return 0.05 * float(self.comm('XP40R'))
        else:
            return 0.1 * float(self.comm('XP40R'))

    def doWriteIdlecurrent(self, value):
        if self.linear:
            self.comm('XP40S%d' % max(0, min(25, round(value / 0.05))))
        else:
            self.comm('XP40S%d' % max(0, min(25, round(value / 0.1))))
        return self.doReadIdlecurrent()

    def doReadMovecurrent(self):
        if self.linear:
            return 0.05 * float(self.comm('XP41R'))
        else:
            return 0.1 * float(self.comm('XP41R'))

    def doWriteMovecurrent(self, value):
        if self.linear:
            self.comm('XP41S%d' % max(0, min(25, round(value / 0.05))))
        else:
            self.comm('XP41S%d' % max(0, min(25, round(value / 0.1))))
        return self.doReadMovecurrent()

    def doReadRampcurrent(self):
        if self.linear:
            return 0.05 * float(self.comm('XP42R'))
        else:
            return 0.1 * float(self.comm('XP42R'))

    def doWriteRampcurrent(self, value):
        if self.linear:
            self.comm('XP42S%d' % max(0, min(25, round(value / 0.05))))
        else:
            self.comm('XP42S%d' % max(0, min(25, round(value / 0.1))))
        return self.doReadRampcurrent()

    def doRead(self, maxage=0):
        return float(self.comm('XP21R')) / (self.slope * self.microstep)

    def _readSE(self):
        temp = self.comm('SE')
        i = ['X', 'Y', 'Z', 'W'].index(self.channel)
        temp = temp[4 * i:4 * i + 4]
        return int(temp, 16)

    def doReadPower(self):
        if self._readSE() & (1 << 3):
            return 'on'
        else:
            return 'off'

    def doWritePower(self, value):
        if value in ['on', 1, True]:
            self.comm('XMA')
        else:
            self.comm('XMD')
        return self.doReadPower()

    def doReadMicrostep(self):
        return int(self.comm('XP45R'))

    def doWriteMicrostep(self, value):
        self.comm('XP45S%d' % int(value))
        return self.doReadMicrostep()

    def doReadSpeed(self):
        return float(self.comm('XP14R')) / float(self.microstep * abs( self.slope ))

    def doWriteSpeed(self, value):
        f = max(0, min(40000, value * abs( self.slope ) * self.microstep))
        self.comm('XP14S%d' % int(f))
        return self.doReadSpeed()

    def doReadAccel(self):
        return float(self.comm('XP15R')) / float(self.microstep * abs( self.slope )) ** 2

    def doWriteAccel(self, value):
        f = max(4000, min(500000, 4000 * round((value * (abs(self.slope) * self.microstep) ** 2) / 4000)))
        self.comm('XP15S%d' % int(f))
        return self.doReadAccel()

    def doStart(self, pos):
        """go to a absolute postition"""
        pos = int(pos * self.slope * self.microstep)
        self.comm('XE%d' % pos)

    def doStop(self):
        ''' send the stop command '''
        for _i in range(5):
            if self.comm('XS') == '':
                return
        self.log.error(self, 'Stopping failed! no ACK!')

    def doSetPosition(self, newpos):
        ''' set current position to given value'''
        d = int(newpos * self.slope * self.microstep)
        self.comm('XP20S%d XP21S%d XP19S%d' % (d, d, d)) # set all counters

    def doStatus(self, maxage=0):
        sui = self.comm('SUI')[ ['X', 'Y', 'Z', 'W'].index(self.channel) ]
        st = int(self.comm('ST')) #for reading enable switch
        t = self._readSE()
        sl = ['Overcurrent', 'Undervoltage', 'Overtemperature', 'Driver enabled',
            'Limit switch - active', 'Limit switch + active', 'stepping error',
            'Encoder error', 'Motor halted', 'referenced']
        s = ''

        if sui in ['+', '2']:
            s = s + 'Limit switch + active, '
        if sui in ['-', '2']:
            s = s + 'Limit switch - active, '

        for i in range(len(sl)):
            if t & (1 << i):
                s = s + sl[i] + ', '

        if (t & 0x100) == 0:
            s = s + 'Motor moving, '

        if st & (1 << 5):
            s = s + 'Driver enabled externally, '
        else:
            s = s + 'Driver disabled externally, '

        if s:
            s = s[:-2]

        if (t & 0x100) == 0:
            return status.BUSY, s

        if (t & 0b1000111) != 0:
            return status.ERROR, s

        return status.OK, s
