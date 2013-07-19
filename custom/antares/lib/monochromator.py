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
#
# *****************************************************************************

"""Antares Monochromator"""

from math import asin, sin, tan, radians, degrees

from nicos.utils import lazy_property
from nicos.core import floatrange, PositionError, HasLimits, Moveable, Param, \
     Override, status, none_or
from nicos.core.utils import multiStatus

class Monochromator(HasLimits):
    ''' monochromator device of antares.

    used to tune the double monochromator to a wavelength between 2.7 and 6.5 Angstroms.
    can be moved to None to get a white beam

    Experimental version.
    CHECK THE FORMULAS!
    '''
    attached_devices = {
                  'phi1'        : (Moveable, 'monochromator rotation 1'),
                  'phi2'        : (Moveable, 'monochromator rotation 2'),
                  'translation' : (Moveable, 'monochromator translation'),
                  'inout'       : (Moveable, 'monochromator inout device'),
    }

    parameters = {
        'dvalue1' : Param('lattice constant of Mono1', type=float,
                           settable=True, mandatory=True),
        'dvalue2' : Param('lattice constant of Mono2', type=float,
                           settable=True, mandatory=True),
        'distance' : Param('parallactic distance of monos', type=float,
                           settable=True, mandatory=True),
        'tolphi'   : Param('max deviation of phi1 or phi2 from calculated value',
                           type=float, settable=True, default=0.01),
        'toltrans' : Param('max deviation of translation from calculated value',
                           type=float, settable=True, default=0.01),
    }

    parameter_overrides = {
        'unit' : Override(mandatory=False, default='Angstrom'),
    }

    valuetype = none_or(floatrange(2.7, 6.5))

    hardware_access = False

    @lazy_property
    def devices(self):
        return list(self._adevs[i] for i in 'inout phi1 phi2 translation'.split())

    def _from_lambda(self, lam):
        ''' returns 3 values used for phi1, phi2 and translation '''
        phi1  = 180. - 2 * degrees(asin(lam / float(2 * self.dvalue1)))
        phi2  =        2 * degrees(asin(lam / float(2 * self.dvalue2)))
        trans = self.distance / tan(radians(phi1))
        return phi1, phi2, trans

    def _to_lambda(self, phi1, phi2, trans):
        ''' calculates lambda from phi1, phi2, trans. May raise a PositionError
        not necessarily all arguments are used.

        next iteration could evaluate all 3 args and return an average value...'''
        try:
            return abs(2 * self.distance * sin(radians(phi1 * 0.5)))
        except Exception:
            raise PositionError('can not determine lambda!')

    def doStart(self, target):
        if self.devices[0].read() == 'out':
            self.log.debug('moving monochromator into beam')

        for d, v in zip(self.devices, ['in'] + list(self._from_lambda(target))):
            self.log.debug('sending %r to %r' % (d.name, v))
            d.start(v)

    def doStatus(self, maxage=0):
        st = multiStatus(self.devices, maxage)
        if st[0] == status.OK:
            # check position
            try:
                _ = self.doRead(maxage)
            except PositionError, e:
                return status.NOTREACHED, str(e)
        return st

    def doRead(self, maxage=0):
        pos = [d.read(maxage) for d in self.devices]

        # Are we in the beam?
        if pos[0] == 'out':
            return None

        # calculate lambda from phi1 and then check the other positions for consistency...
        lam = self._to_lambda(*pos[1:])
        self.log.debug('lambda seems to be %.4f Angstroms' % lam)
        compare_pos = self._from_lambda(lam)
        for d, p, t, c in zip(self.devices[1:], pos[1:], [self.tolphi, self.tolphi, self.toltrans], compare_pos):
            self.log.debug('%r is at %r and should be at %r for %.4f Angstroms' %(d, d.format(p), d.format(c), lam))
            if abs(p-c) > t:
                raise PositionError('%r is too far away for %.4f Angstroms'% (d, lam))
        return lam

    def doWait(self):
        for d in self.devices:
            self.log.debug('Waiting for %r' % d.name)
            d.wait()
