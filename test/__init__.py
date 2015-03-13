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
#   Georg Brandl <georg.brandl@frm2.tum.de>
#
# *****************************************************************************

"""NICOS test suite."""

from __future__ import print_function

import os
import sys


from nicos.core.device import Device
Device._base_loop_delay = 0.002
Device._long_loop_delay = 0.02

from test.utils import cleanup


def setup_package():
    # make the test suite run the same independent of the hostname
    os.environ['INSTRUMENT'] = 'test'
    sys.stderr.write('\nSetting up main test package, cleaning old test dir...\n')
    try:
        cleanup()
    except OSError:
        sys.stderr.write('Failed to clean up old test dir. Check if NICOS '
                         'processes are still running.')
        sys.stderr.write('=' * 80)
        raise
