#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2014 by the NICOS contributors (see AUTHORS)
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
#   Enrico Faulhaber <enrico.faulhaber@frm2.tum.de>
#
# *****************************************************************************

"""Virtual devices for testing."""

import time
import random
import threading
from math import exp, atan

import numpy as np

from nicos import session
from nicos.utils import clamp
from nicos.services.poller.psession import PollerSession
from nicos.core import status, Readable, HasOffset, HasLimits, Param, Override, \
    none_or, oneof, tupleof, floatrange, Measurable, Moveable, Value, \
    ImageProducer, ImageType, SIMULATION, Attach
from nicos.devices.abstract import Motor, Coder
from nicos.devices.generic.detector import Channel


class VirtualMotor(Motor, HasOffset):
    """A virtual motor that can be set to move in finite time using a thread."""

    parameters = {
        'speed':     Param('Virtual speed of the device', settable=True,
                           type=floatrange(0, 1e6), unit='main/s'),
        'jitter':    Param('Jitter of the read value', default=0, unit='main'),
        'curvalue':  Param('Current value', settable=True, unit='main'),
        'curstatus': Param('Current status', type=tupleof(int, str),
                           settable=True, default=(status.OK, 'idle')),
        'ramp':      Param('Virtual speed of the device', settable=True,
                           type=floatrange(0, 1e6), unit='main/min'),
    }

    _thread = None

    def doStart(self, pos):
        pos = float(pos) + self.offset
        if self.speed != 0:
            if self._thread:
                self.stop()
                self._thread.join()
            self.curstatus = (status.BUSY, 'virtual moving')
            self._thread = threading.Thread(target=self.__moving, args=(pos,),
                                            name='virtual motor %s' % self)
            self._thread.daemon = True
            self._thread.start()
        else:
            self.curstatus = (status.BUSY, 'virtual moving')
            self.log.debug('moving to %s' % pos)
            self.curvalue = pos
            self.curstatus = (status.OK, 'idle')

    def doRead(self, maxage=0):
        return (self.curvalue - self.offset) + \
            self.jitter * (0.5 - random.random())

    def doStatus(self, maxage=0):
        return self.curstatus

    def doStop(self):
        if self.speed != 0 and \
           self._thread is not None and self._thread.isAlive():
            self._stop = True
        else:
            self.curstatus = (status.OK, 'idle')

    def doSetPosition(self, pos):
        self.curvalue = pos + self.offset

    def _step(self, start, end, elapsed, speed):
        delta = end - start
        sign = +1 if delta > 0 else -1
        value = start + sign * speed * elapsed
        if (sign == 1 and value >= end) or (sign == -1 and value <= end):
            return end
        return value

    def __moving(self, pos):
        speed = self.speed
        try:
            self._stop = False
            start = self.curvalue
            started = time.time()
            while 1:
                value = self._step(start, pos, time.time() - started, speed)
                if self._stop:
                    self.log.debug('thread stopped')
                    return
                time.sleep(0.2)
                self.log.debug('thread moving to %s' % value)
                self.curvalue = value
                if value == pos:
                    return
        finally:
            self._stop = False
            self.curstatus = (status.OK, 'idle')
            self._thread = None

    def doReadRamp(self):
        return self.speed * 60.

    def doWriteRamp(self, value):
        self.speed = value / 60.


class VirtualCoder(Coder, HasOffset):
    """A virtual coder that just returns the value of a motor, with offset."""

    attached_devices = {
        'motor': (Readable, 'Motor to read out to get coder value')
    }

    def doRead(self, maxage=0):
        val = self._adevs['motor'] and self._adevs['motor'].read(maxage) or 0
        return val - self.offset

    def doStatus(self, maxage=0):
        return status.OK, ''

    def doSetPosition(self, _pos):
        pass


class VirtualTimer(Channel):
    """A virtual timer channel for use together with
    `nicos.devices.generic.detector.MultiChannelDetector`.
    """

    def doInit(self, mode):
        self.__finish = False

    def doStart(self):
        if self.ismaster:
            self.__finish = False
            thr = threading.Thread(target=self.__thread,
                                   name='virtual timer %s' % self)
            thr.daemon = True
            thr.start()

    def doIsCompleted(self):
        return self.__finish

    def __thread(self):
        finish_at = time.time() + self.preselection
        while time.time() < finish_at and not self.__finish:
            time.sleep(0.1)
        self.__finish = True

    def doStop(self):
        self.__finish = True

    def doStatus(self, maxage=0):
        return status.OK, ''

    def doRead(self, maxage=0):
        if self.ismaster:
            return self.preselection
        return random.randint(0, 1000)

    def doSimulate(self, preset):
        return [self.doRead()]

    def doReadUnit(self):
        return 's'

    def valueInfo(self):
        return Value(self.name, unit='s', type='time', fmtstr='%.3f'),

    def doTime(self, preset):
        if self.ismaster:
            return self.preselection
        else:
            return 0


class VirtualCounter(Channel):
    """A virtual counter channel for use together with
    `nicos.devices.generic.detector.MultiChannelDetector`.
    """

    parameters = {
        'countrate':  Param('The maximum countrate', default=1000),
        'type':       Param('Type of channel: monitor or counter',
                            type=oneof('monitor', 'counter'), mandatory=True),
    }

    def doStatus(self, maxage=0):
        return status.OK, ''

    def doRead(self, maxage=0):
        if self.ismaster:
            return self.preselection
        return random.randint(0, self.countrate)

    def doSimulate(self, preset):
        return [self.doRead()]

    def doIsCompleted(self):
        return True

    def doReadUnit(self):
        return 'cts'

    def valueInfo(self):
        return Value(self.name, unit='cts', errors='sqrt', type=self.type,
                     fmtstr='%d'),


class VirtualTemperature(VirtualMotor):
    """A virtual temperature regulation device."""

    parameters = {
        'tolerance': Param('Tolerance for wait()', default=1, settable=True,
                           unit='main', category='general'),
        'setpoint':  Param('Last setpoint', settable=True, unit='main',
                           category='general'),
    }

    parameter_overrides = {
        'unit':      Override(mandatory=False, default='K'),
        'jitter':    Override(default=0.1),
        'curvalue':  Override(default=10),
    }

    def doStart(self, pos):
        self.setpoint = pos
        VirtualMotor.doStart(self, pos)

    def doWait(self):
        while self.curstatus[0] == status.BUSY:
            if abs(self.read(0) - self.setpoint) < self.tolerance:
                break
            time.sleep(0.1)
        # wait returns earlier than status is idle. This violates NICOS philosophy!
        self.curstatus = (status.OK, 'idle')

    def _step(self, start, end, elapsed, speed):
        # calculate an exponential approximation to the setpoint with a time
        # constant given by self.speed
        gamma = speed / 10.
        cval = end + (start - end) * exp(-gamma*elapsed)
        if abs(cval - end) < self.jitter:
            return end
        return cval




class VirtualRealTemperature(HasLimits, Moveable):
    parameters = {
        'jitter':    Param('Jitter of the read-out value', default=0,
                           unit='main'),
        'regulation': Param('Current temperature (regulation)', settable=False,
                           unit='main', default=2.),
        'sample':    Param('Current temperature (sample)', settable=False,
                           unit='main', default=2.),
        'curstatus': Param('Current status', type=tupleof(int, str),
                           settable=True, default=(status.OK, 'idle')),
        'ramp':      Param('Ramping speed of the setpoint', settable=True,
                           type=none_or(floatrange(0, 1000)), unit='main/min'),
        'tolerance': Param('Tolerance for wait()', default=1, settable=True,
                           unit='main', category='general'),
        'window':    Param('Window for wait()', default=60, settable=True,
                           unit='s', category='general'),
        'loopdelay': Param('Cycle time for internal thread', default=1,
                           settable=True, unit='s', type=floatrange(0.2, 10)),
        'timeout':   Param('Timeout for wait()', default=900, settable=True,
                           unit='s', category='general'),
        'setpoint':  Param('Current setpoint', settable=True, unit='main',
                           category='general', default=2.),
        'heater':    Param('Simulated heater output power in percent',
                           settable=True, unit='%'),
        'heaterpower': Param('Simulated heater output power in Watt',
                           settable=False, unit='W'),
        'maxpower':  Param('Max heater power in W', settable=True, unit='W',
                           default=100),
        'p':         Param('P-value for regulation', settable=True,
                           default=100, unit='%/main'),
        'i':         Param('I-value for regulation', settable=True,
                           default=10, unit='%/mains'),
        'd':         Param('D-value for regulation', settable=True,
                           default=1, unit='%s/main'),
        'mode' :     Param('PID control or open loop heater mode',
                           settable=True, default='manualpid',
                           type=oneof('manualpid', 'manual', 'openloop')),
        'speedup' :  Param('speed up simulation by a factor', settable=True,
                           default=1, unit='', type=floatrange(0.01, 100)),
    }

    parameter_overrides = {
        'unit':      Override(mandatory=False, default='K'),
    }

    _thread = None
    _window = None
    _starttime = 0

    def doInit(self, mode):
        if mode == SIMULATION:
            return
        if not isinstance(session, PollerSession): # dont run in the poller!
            self._window = []
            self._statusLock = threading.Lock()
            self._thread = threading.Thread(target=self.__run,
                                        name='Cryo simulator %s' % self)
            self._thread.daemon = True
            self._thread.start()

    def doStart(self, pos):
        # do nothing more, its handled in the thread...
        with self._statusLock:
            # insert target position into history
            # if target is far away -> loop goes busy
            # else loop sets to stable again....
            self._setROParam('target', pos)
            currtime = time.time()
            self._window.append( (currtime, pos))
            self._starttime = currtime
            self.curstatus = status.BUSY, 'moving'

    def doRead(self, maxage=0):
        return self.regulation + self.jitter * (0.5 - random.random())

    def doStatus(self, maxage=0):
        return self.curstatus

    def doStop(self):
        self.start(self.setpoint)

    def doPoll(self, nr):
        self._pollParam('setpoint', 1)
        self._pollParam('curvalue', 1)
        self._pollParam('curstatus', 1)

    #
    # Parameters
    #
    def doWriteMaxpower(self, newpower):
        self.heater = clamp(self.heater * self.maxpower / float(newpower), 0, 100)

    #
    # calculation helpers
    #
    def __coolerPower(self, temp):
        """returns cooling power in W at given temperature"""
        # quadratic up to 42K, is linear from 40W@42K to 100W@600K
        #~ return clamp((temp-2)**2 / 32., 0., 40.) + temp * 0.1
        return clamp(15 * atan(temp * 0.01) ** 3, 0., 40.) + temp * 0.1 - 0.2

    def __coolerCP(self, temp):
        """heat capacity of cooler at given temp"""
        return 75 * atan(temp / 50)**2 + 1

    def __heatLink(self, coolertemp, sampletemp):
        """heatflow from sample to cooler. may be negative..."""
        flow = (sampletemp - coolertemp) * ((coolertemp + sampletemp) ** 2)/400.
        cp = clamp(self.__coolerCP(coolertemp)*self.__sampleCP(sampletemp), 1, 10)
        return clamp(flow, -cp, cp)

    def __sampleCP(self, temp):
        return 3 * atan(temp / 30) + \
                12 * temp / ((temp - 12.)**2 + 10) + 0.5

    def __sampleLeak(self, temp):
        return 0.02/temp

    #
    # Model is a cooling source with __coolingPower and __coolerCP capacity
    # here we have THE heater and the regulation thermometer
    # this is connected via a __heatLink to a sample with __heatCapacity and
    # here we have the sample thermometer
    #
    def __run(self):
        try:
            self.__moving()
        except Exception as e:
            self.log.exception(e)
            self.curstatus = status.ERROR, str(e)

    def __moving(self):
        # complex thread handling:
        # a) simulation of cryo (heat flow, thermal masses,....)
        # b) optional PID temperature controller with windup control
        # c) generating status+updated value+ramp
        # this thread is not supposed to exit!

        # local state keeping:
        regulation = self.regulation
        sample = self.sample
        timestamp = time.time()
        stable = False
        heater = 0
        lastflow = 0
        last_heaters = (0, 0)
        delta = 0
        I = D = 0
        lastD = 0
        damper = 1
        lastmode = self.mode
        while True:
            t = time.time()
            h = t - timestamp
            if h < self.loopdelay / damper:
                time.sleep(clamp(self.loopdelay / damper - h, 0.1, 60))
                continue
            h *= self.speedup
            # a)
            sample = self.sample
            regulation = self.regulation
            heater = self.heater

            heatflow = self.__heatLink(regulation, sample)
            self.log.debug('sample = %.5f, regulation = %.5f, heatflow = %.5g'
                           % (sample, regulation, heatflow))
            newsample = max(0, sample + (self.__sampleLeak(sample) - heatflow) / self.__sampleCP(sample) * h)
            newsample = clamp(newsample, sample, regulation) # avoid instabilities due to too small CP
            newregulation = max(0, regulation + (heater * 0.01 * self.maxpower
                + heatflow - self.__coolerPower(regulation)) /
                self.__coolerCP(regulation) * h)

            # b) see
            # http://brettbeauregard.com/blog/2011/04/improving-the-beginners-pid-introduction/
            if self.mode !='openloop':
                # fix artefacts due to too big timesteps
                # actually i would prefer reducing loopdelay, but i have no good idea on when to increase it back again
                if heatflow * lastflow != -100:
                    if (newregulation - newsample) * (regulation - sample) < 0:
                        #~ newregulation = (newregulation + regulation) / 2
                        #~ newsample = (newsample + sample) / 2
                        damper +=1
                lastflow = heatflow

                error = self.setpoint - newregulation
                #~ # use a simple filter to smooth delta a little
                delta = (delta + regulation - newregulation) / 2.


                kp = self.p / 10.        # LakeShore P = 10*k_p
                ki = kp * abs(self.i) / 500.  # LakeShore I = 500/T_i
                kd = kp * abs(self.d) / 2.    # LakeShore D = 2*T_d

                P = kp * error
                I += ki * error * h
                D = kd * delta / h

                # avoid reset windup
                I = clamp(I, 0., 100.) # I is in %

                # avoid jumping heaterpower if switching back to pid mode
                if lastmode != self.mode:
                    # adjust some values upon switching back on
                    I = self.heater - P - D

                v = P + I + D
                # in damping mode, use a weighted sum of old + new heaterpower
                if damper > 1:
                    v = ((damper ** 2 - 1) * self.heater + v) / damper ** 2

                # damp oscillations due to D switching signs
                if D * lastD < -0.2:
                    v = (v + heater) / 2.
                # clamp new heater power to 0..100%
                heater = clamp(v, 0., 100.)
                lastD = D

                self.log.debug('PID: P = %.2f, I = %.2f, D = %.2f, heater = %.2f' %
                               (P, I, D, heater))

                # check for turn-around points to detect oscillations -> increase damper
                x,y = last_heaters
                if (x + 0.1 < y and y > heater + 0.1) or (x > y + 0.1 and y + 0.1 < heater):
                    damper += 1
                last_heaters = (y, heater)

            else:
                # self.heaterpower is set manually, not by pid
                heater = self.heater
                last_heaters = (0, 0)

            heater = round(heater, 3)
            sample = newsample
            regulation = newregulation
            lastmode = self.mode

            # c)
            if self.setpoint != self.target:
                if self.ramp == 0:
                    maxdelta = 10000
                else:
                    maxdelta = self.ramp / 60. * h
                try:
                    self.setpoint = round(self.setpoint +
                                          clamp(self.target - self.setpoint,
                                         -maxdelta, maxdelta), 3)
                    self.log.debug('setpoint changes to %r' % self.setpoint)
                except (TypeError, ValueError):
                    # self.target might be None
                    pass

            # keep max self.window seconds long history
            self._window.append((t, regulation))
            while t - self._window[0][0] > self.window:
                self._window.pop(0)

            # temperature is stable when all recorded values in the window
            # differ from setpoint by less than tolerance
            with self._statusLock:
                stable = max(abs(x - self.setpoint) for _, x in self._window) \
                    <= self.tolerance
                fullwindow = len(self._window) >= self.window / float(self.loopdelay)
                # but status is only OK if setpoint is already at target
                if stable and fullwindow and (self.setpoint == self.target):
                    # XXX TODO: timeout
                    self.curstatus = status.OK, 'stable'
                    damper -= (damper - 1) / 10. # max value for damper is 11
                    self._starttime = 0
                else:
                    if self._starttime + self.timeout >= t:
                        self.curstatus = status.BUSY, 'moving'
                    elif self._starttime > 0:
                        self.curstatus = status.NOTREACHED, 'timeout'
                    else:
                        # unstable: BUSY, or NOTREACHED ???
                        self.curstatus = status.BUSY, 'unstable'
            damper -= (damper - 1) / 20.
            self._setROParam('regulation', round(regulation, 3))
            self._setROParam('sample', round(sample, 3))
            self._setROParam('heaterpower', round(heater * self.maxpower * 0.01, 3))
            self.heater = heater
            timestamp = t


class Virtual2DDetector(ImageProducer, Measurable):
    """A virtual 2-dimensional detector that generates a direct beam and
    four peaks of scattering intensity."""

    attached_devices = {
        'distance':    Attach('The detector distance for simulation', Moveable,
                              optional=True),
        'collimation': Attach('The collimation', Readable, optional=True),
    }

    parameters = {
        'lastcounts': Param('Current total number of counts', settable=True,
                            type=int),
    }

    imagetype = ImageType((128, 128), '<u4')
    _buf = None
    _mythread = None
    _stopflag = False

    def doSetPreset(self, **preset):
        self._lastpreset = preset

    def doStart(self):
        t = self._lastpreset.get('t', 1)
        if self._mythread:
            self._stopflag = True
            self._mythread.join()
        self._mythread = threading.Thread(target=self._run,  args=(t, ))
        self._mythread.start()

    def _run(self,  maxtime):
        try:
            starttime = now = time.time()
            while True:
                array = self._generate(now - starttime).astype('<u4')
                self._buf = array
                self.lastcounts = array.sum()
                self.updateImage(array)
                if self._stopflag or now > (starttime + maxtime):
                    break
                time.sleep(min(1, maxtime - now + starttime))
                now = time.time()
        finally:
            self._stopflag = False
            self._mythread = None

    def doStop(self):
        self._stopflag = True

    def doStatus(self,  maxage=0):
        if self._stopflag or self._mythread:
            return status.BUSY,  'busy'
        return status.OK,  'idle'

    def readImage(self):
        return self._buf

    def readFinalImage(self):
        return self._buf

    def clearImage(self):
        self._buf = self._generate(0).astype('<u4')
        self.lastcounts = 0

    def doRead(self, maxage=0):
        return [self.lastcounts, self.lastfilename]

    def valueInfo(self):
        return (Value(self.name + '.sum', unit='cts', type='counter',
                      errors='sqrt', fmtstr='%d'),
                Value(self.name + '.file', type='info', fmtstr='%s'))

    def doIsCompleted(self):
        return not self._mythread

    def _generate(self, t):
        dst = (self._adevs['distance'].read() * 5) if self._adevs['distance'] \
              else 5
        coll = self._adevs['collimation'].read() if self._adevs['collimation'] \
              else '15m'
        xx, yy = np.meshgrid(np.linspace(-64, 63, 128), np.linspace(-64, 63, 128))
        beam = (t * 100 * np.exp(-xx**2/50) * np.exp(-yy**2/50)).astype(int)
        sigma2 = coll == '10m' and 200 or (coll == '15m' and 150 or 100)
        beam += t * 30 * np.exp(-(xx-dst)**2/sigma2) * np.exp(-yy**2/sigma2) + \
            t * 30 * np.exp(-(xx+dst)**2/sigma2) * np.exp(-yy**2/sigma2) + \
            t * 20 * np.exp(-xx**2/sigma2) * np.exp(-(yy-dst)**2/sigma2) + \
            t * 20 * np.exp(-xx**2/sigma2) * np.exp(-(yy+dst)**2/sigma2)
        return np.random.poisson(beam)
