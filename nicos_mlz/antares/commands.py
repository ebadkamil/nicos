#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2021 by the NICOS contributors (see AUTHORS)
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
#   Alexander Lenz <alexander.lenz@frm2.tum.de>
#   Philipp Schmakat <philipp.schmakat@frm2.tum.de>
#
# *****************************************************************************

import os
from os.path import join

from nicos import session
from nicos.commands import helparglist, usercommand
from nicos.commands.device import maw
from nicos.commands.scan import scan

from nicos_mlz.frm2.commands.imaging import darkimage as _darkimage, grtomo, \
    openbeamimage as _openbeamimage, tomo

__all__ = ['tomo', 'openbeamimage', 'darkimage', 'grtomo']


@usercommand
@helparglist('shutter, [nimages], [detectors], [presets]')
# pylint: disable=keyword-arg-before-vararg
def openbeamimage(shutter=None, nimages=1, *detlist, **preset):
    """ANTARES specific openbeam image acquisition.

    Acquires one or more openbeam images and creates link to the last taken
    image.
    """
    exp = session.experiment
    _openbeamimage(shutter, nimages, *detlist, **preset)

    src = join(exp.proposalpath, exp.lastopenbeamimage)
    dst = join(exp.proposalpath, 'currentopenbeamimage.fits')

    try:
        os.remove(dst)
    except OSError as e:
        session.log.warning('Could not remove symlink: %s', e)

    try:
        os.symlink(src, dst)
    except OSError as e:
        session.log.warning('Could not create symlink: %s', e)


@usercommand
@helparglist('shutter, [nimages], [detectors], [presets]')
# pylint: disable=keyword-arg-before-vararg
def darkimage(shutter=None, nimages=1, *detlist, **preset):
    """ANTARES specific dark image acquisition.

    Acquires one or more dark images and creates a link to the last taken
    image.
    """
    exp = session.experiment
    _darkimage(shutter, nimages, *detlist, **preset)
    src = join(exp.proposalpath, exp.lastdarkimage)
    dst = join(exp.proposalpath, 'currentdarkimage.fits')

    try:
        os.remove(dst)
    except OSError as e:
        session.log.warning('Could not remove symlink: %s', e)

    try:
        os.symlink(src, dst)
    except OSError as e:
        session.log.warning('Could not create symlink: %s', e)


@usercommand
@helparglist('n_images, p, angle, [detectors], [presets]')
# pylint: disable=keyword-arg-before-vararg
def nGI_stepping(n_images, p=1, angle=0, *detlist, **preset):
    """Performs a nGI stepping scan of G0 over p periods in n_images-1 steps.

    Calculates the stepping period from the angle of the grating lines to the
    vertical axis *angle*.

    Example:

    >>> nGI_stepping(11,1,0,t=30) # steps G0 over one period from 0 to 1.6 mm
    >>>                           # in 0.16 mm steps and count for 30 s
    """

    import numpy as np

    stepwidth = 1.6 / np.cos(angle*2*np.pi/360) * p / (n_images-1)

    session.log.info('Starting nGI scan.')

    scan('G0tx', 0, stepwidth, n_images, *detlist, **preset)
    maw('fastshutter', 'closed')
    session.log.info('fastshutter closed')
