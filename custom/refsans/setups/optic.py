#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2015 by the NICOS contributors (see AUTHORS)
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
#   Matthias Pomm <matthias.pomm@hzg.de>
#
# **************************************************************************

description = 'NOK Devices for REFSANS, main file including all'

group = 'lowlevel'

includes = ['nok1', 'nok2', 'nok3', 'nok4',
            # beckhoff 'b1',
            'disc3','disc4',
            # beckhoff 'nok5a', 'nok5b',
            # beckhoff 'zb0', 'zb1',
            'nok6', 'nok7', 'nok8', 'nok9',
            'sc2',
            'zb2', 'bs1', 'zb3',]
