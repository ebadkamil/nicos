#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2019 by the NICOS contributors (see AUTHORS)
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
#
# *****************************************************************************

"""NICOS demo class displaying the CPU load"""

from __future__ import absolute_import, division, print_function

import psutil

from nicos import session
from nicos.core import POLLER, SIMULATION, Param, Readable, status
from nicos.core.params import floatrange
from nicos.utils import createThread


class CPULoad(Readable):

    parameters = {
        'interval':  Param('Interval for load detection',
                           type=floatrange(0.1, 60),
                           default=0.1, settable=False,),
        'lastvalue': Param('Last obtained value', type=float,
                           userparam=False, mandatory=False, default=0.0),
    }

    def doInit(self, mode):
        if mode == SIMULATION:
            return
        # create only run ONE thread: in the poller
        # it may look stupid, as the poller already has a thread polling read()
        # now imagine several such devices in a setup.... not so stupid anymore
        if session.sessiontype == POLLER:
            self._thread = createThread('measure cpuload', self._run)

    def doWriteInterval(self, value):
        self.pollinterval = max(1, 2 * value)
        self.maxage = max(3, 5 * value)

    def doRead(self, maxage=0):
        return self.lastvalue

    def doStatus(self, maxage=0):
        return status.OK, ''

    def _run(self):
        while True:
            self._setROParam('lastvalue', psutil.cpu_percent(self.interval))
