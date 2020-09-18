#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2020 by the NICOS contributors (see AUTHORS)
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

"""Refsans specific sample implementation."""

from nicos.core.params import Param, floatrange
from nicos.devices.sample import Sample as BaseSample


class Sample(BaseSample):
    """Refsans specific sample."""

    parameters = {
        'width': Param('width of sample lateral',
                       type=floatrange(0, 100), settable=True, default=100,
                       unit='mm', fmtstr='%.1f', category='sample'),
        'length': Param('length of sample in beam',
                        type=floatrange(0, 100), settable=True, default=100,
                        unit='mm', fmtstr='%.1f', category='sample'),
    }
