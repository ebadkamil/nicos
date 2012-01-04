#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS-NG, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2011 by the NICOS-NG contributors (see AUTHORS)
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

"""NICOS commands tests."""

from nicos import session
from nicos.core import UsageError, LimitError, ModeError, Value

from nicos.commands.scan import scan
from nicos.commands.measure import count
from nicos.commands.device import move, maw

from nicos.commands.analyze import fwhm, center_of_mass, root_mean_square, \
     poly, gauss

from nicos.commands.scan import scan, cscan, timescan, twodscan, contscan, \
     manualscan

from test.utils import raises

def setup_module():
    session.loadSetup('axis')
    session.loadSetup('detector')
    session.setMode('master')
    session.experiment.detlist = [session.getDevice('det')]

def teardown_module():
    session.experiment.detlist = []
    session.unloadSetup()

def test_commands():
    motor = session.getDevice('motor')

    session.setMode('slave')
    assert raises(ModeError, scan, motor, [0, 1, 2, 10])

    session.setMode('master')
    scan(motor, [0, 1, 2, 10])

    assert raises(UsageError, count, motor)
    count()

    assert raises(LimitError, move, motor, max(motor.abslimits)+1)

    positions = (min(motor.abslimits), 0, max(motor.abslimits))
    for pos in positions:
        move(motor, pos)
        motor.wait()
        assert motor.curvalue == pos

    for pos in positions:
        maw(motor, pos)
        assert motor.curvalue == pos


# tests for the nicos.commands.scan module

def test_scan():
    m = session.getDevice('motor')
    m2 = session.getDevice('motor2')
    c = session.getDevice('coder')
    ctr = session.getDevice('ctr1')
    mm = session.getDevice('manual')
    mm.move(0)

    # plain scan, with some extras: infostring, firstmove
    scan(m, 0, 1, 5, 0., 'test scan', manual=1)
    dataset = session.experiment._last_datasets[-1]
    assert dataset.xnames == ['motor']
    assert dataset.xunits == ['mm']
    assert dataset.xresults == [[float(i)] for i in range(5)]
    assert dataset.ynames == ['timer', 'mon1', 'ctr1', 'ctr2']
    assert dataset.yunits == ['s', 'cts', 'cts', 'cts']
    assert dataset.scaninfo.startswith('test scan')
    assert len(dataset.yresults) == 5
    assert mm.read() == 1

    # scan with second basic syntax
    scan(m, [0, 4, 5], 0.)
    dataset = session.experiment._last_datasets[-1]
    assert dataset.xresults == [[float(i)] for i in [0, 4, 5]]

    # scan with multiple devices
    scan([m, m2], [0, 0], [1, 2], 3, t=0.)
    dataset = session.experiment._last_datasets[-1]
    assert dataset.xresults == [[float(i), float(i*2)] for i in [0, 1, 2]]

    # scan with multiple devices and second basic syntax
    scan([m, m2], [[0, 0, 1], [4, 2, 1]], t=0.)
    dataset = session.experiment._last_datasets[-1]
    assert dataset.xresults == [[0., 4.], [0., 2.], [1., 1.]]

    # scan with different detectors
    scan(m, [0, 1], ctr)
    dataset = session.experiment._last_datasets[-1]
    assert dataset.xresults == [[0.], [1.]]
    assert len(dataset.yresults) == 2 and len(dataset.yresults[0]) == 1
    assert dataset.ynames == ['ctr1']

    # scan with different environment
    scan(m, [0, 1], c)
    dataset = session.experiment._last_datasets[-1]
    assert dataset.xresults == [[0., 0.], [1., 1.]]
    assert dataset.xnames == ['motor', 'coder']
    assert dataset.xunits == ['mm', 'mm']

    # scan with multistep
    scan(m, [0, 1], ctr, manual=[3, 4])
    dataset = session.experiment._last_datasets[-1]
    assert dataset.xresults == [[0.], [1.]]
    assert dataset.ynames == ['ctr1_manual_3', 'ctr1_manual_4']

def test_cscan():
    m = session.getDevice('motor')


# tests for the nicos.commands.analyze module

def generate_dataset():
    """Generate a dataset as if a scan has been run."""
    import numpy
    data = numpy.array((1, 2, 1, 2, 2, 2, 5, 20, 30, 20, 10, 2, 3, 1, 2, 1, 1, 1))
    xpoints = numpy.arange(-9, 9)
    assert len(data) == len(xpoints)
    dataset = session.experiment.createDataset(None)
    dataset.xvalueinfo = [Value('x', 'other')]
    dataset.yvalueinfo = [Value('y1', 'counter'), Value('y2', 'counter')]
    dataset.xresults = [[x] for x in xpoints]
    dataset.yresults = [[y, y*2] for y in data]
    session.experiment._last_datasets.append(dataset)

def test_fwhm():
    generate_dataset()
    result = fwhm(1,1)
    print result
    assert result == (2.75, -1, 30, 1)

def test_center_of_mass():
    generate_dataset()
    result1 = center_of_mass()
    print result1   # ~ -0.839622641509
    assert -0.840 < result1 < -0.839
    result2 = center_of_mass(2)  # center of mass from values*2 should be same
    assert result1 == result2

def test_root_mean_square():
    generate_dataset()
    result = root_mean_square()
    print result   # ~ 10.1488915651
    assert 10.148 < result < 10.149

def test_poly():
    generate_dataset()
    result1 = poly(1)
    assert len(result1) == 2 and len(result1[0]) == 2
    assert 5.851 < result1[0][0] < 5.852
    result2 = poly(2)
    assert -0.203 < result2[0][2] < -0.202
    result3 = poly(2, 2)
    assert -0.405 < result3[0][2] < -0.404
    result4 = poly(2, 1, 2)
    assert result4 == result3

def test_gauss():
    generate_dataset()
    result = gauss()
    assert len(result) == 2 and len(result[0]) == 4
    assert -0.927 < result[0][0] < -0.926
