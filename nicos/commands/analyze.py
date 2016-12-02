#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2016 by the NICOS contributors (see AUTHORS)
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

"""Module for data analyzing user commands."""

from __future__ import division

from math import sqrt

import numpy as np

from nicos import session
from nicos.core import NicosError, UsageError
from nicos.utils import printTable
from nicos.utils.fitting import Fit, GaussFit, PolyFit
from nicos.utils.analyze import estimateFWHM
from nicos.pycompat import string_types
from nicos.pycompat import xrange as range  # pylint: disable=W0622
from nicos.commands import usercommand, helparglist
from nicos.commands.scan import cscan
from nicos.commands.device import maw


__all__ = [
    'center_of_mass', 'fwhm', 'root_mean_square', 'poly', 'gauss',
    'center', 'checkoffset', 'findpeaks',
]


def _getData(columns=None):
    if not session.data._last_scans:
        raise NicosError('no latest dataset has been stored')
    dataset = session.data._last_scans[-1]

    # append data from previous scans if this is a continuation
    i = -1
    xresults = dataset.devvaluelists
    yresults = dataset.detvaluelists
    while dataset.continuation:
        i -= 1
        dataset = session.data._last_scans[i]
        xresults = dataset.devvaluelists + xresults
        yresults = dataset.detvaluelists + yresults

    # xcol/ycol are 1-indexed here
    if not columns:
        xcol = dataset.xindex + 1
        ycol = -1
    elif len(columns) == 1:
        xcol, ycol = dataset.xindex + 1, columns[0]
    elif len(columns) == 2:
        xcol, ycol = columns[0], columns[1]
    else:
        raise UsageError('you can give none, one or two columns names or '
                         'numbers')

    if isinstance(xcol, string_types):
        try:
            xcol = [v.name for v in dataset.devvalueinfo].index(xcol) + 1
        except ValueError:
            raise NicosError('no such X column name: %r' % xcol)

    if isinstance(ycol, string_types):
        try:
            ycol = [v.name for v in dataset.detvalueinfo].index(ycol) + 1
        except ValueError:
            raise NicosError('no such Y column name: %r' % ycol)
    elif ycol < 0:
        try:
            ycol = [j for (j, info) in enumerate(dataset.detvalueinfo)
                    if info.type == 'counter'][0] + 1
        except IndexError:
            raise NicosError('no Y column of type "counter"')

    # now make them 0-indexed
    xcol -= 1
    ycol -= 1

    names = [dataset.devvalueinfo[xcol].name, dataset.detvalueinfo[ycol].name]

    try:
        xs = np.array([p[xcol] for p in xresults])
    except IndexError:
        raise NicosError('no such X column: %r' % xcol)
    try:
        ys = np.array([p[ycol] for p in yresults])
    except IndexError:
        raise NicosError('no such Y column: %r' % ycol)

    if dataset.detvalueinfo[ycol].errors == 'sqrt':
        dys = np.sqrt(ys)
    elif dataset.detvalueinfo[ycol].errors == 'next':
        try:
            dys = np.array([p[ycol+1] for p in yresults])
        except IndexError:
            dys = np.array([1] * len(ys))
    else:
        dys = np.array([1] * len(ys))

    return xs, ys, dys, names, dataset


COLHELP = """
    The data columns to use can be given by the arguments: either only the Y
    column, or both X and Y columns.  If they are not given, then the default X
    column is the first, and the default Y column is the first column of type
    "counter".  Examples:

    >>> func()     # use first X column and first counter Y column
    >>> func(2)    # use first X column and second Y column
    >>> func(2, 3) # use second X column and third Y column

    It is also possible to give columns by name, for example:

    >>> func('om', 'ctr1')
"""


@usercommand
@helparglist('[[xcol, ]ycol]')
def center_of_mass(*columns):
    """Calculate the center of mass x-coordinate of the last scan."""
    xs, ys = _getData(columns)[:2]
    cm = (xs * ys).sum() / ys.sum()
    return float(cm)

center_of_mass.__doc__ += COLHELP.replace('func(', 'center_of_mass(')


@usercommand
@helparglist('[[xcol, ]ycol]')
def fwhm(*columns):
    """Calculate an estimate of full width at half maximum.

    The search starts a the 'left' end of the data.

    Returns a tuple ``(fwhm, xpeak, ymax, ymin)``:

    * fwhm - full width half maximum
    * xpeak - x value at y = ymax
    * ymax - maximum y-value
    * ymin - minimum y-value
    """
    xs, ys = _getData(columns)[:2]
    return estimateFWHM(xs, ys)

fwhm.__doc__ += COLHELP.replace('func(', 'fwhm(')


@usercommand
@helparglist('[ycol]')
def root_mean_square(col=None):
    """Calculate the root-mean-square of the last scan.

    The data column to use can be given by an argument (by name or number); the
    default is the first Y column of type "counter".
    """
    ys = _getData(col and (0, col) or ())[1]
    return sqrt((ys**2).sum() / len(ys))


class FitResult(tuple):
    __display__ = False


@usercommand
@helparglist('n, [[xcol, ]ycol]')
def poly(n, *columns):
    """Fit a polynomial of degree *n* through the last scan.

    The return value is a pair of tuples::

        (coefficients, coeff_errors)

    where both *coefficients* and *coeff_errors* are tuples of *n+1* elements.
    """
    xs, ys, dys, _, ds = _getData(columns)
    fit = PolyFit(n, [1] * (n+1))
    res = fit.run(xs, ys, dys)
    if res._failed:
        session.log.info('Fit failed.')
        return FitResult((None, None))
    session.notifyFitCurve(ds, 'poly(%d)' % n, res.curve_x, res.curve_y)
    descrs = ['a_%d' % i for i in range(n+1)]
    vals = []
    for par, err, descr in zip(res._pars[1], res._pars[2], descrs):
        vals.append((descr, '%.5g' % par, '+/- %.5g' % err))
    printTable(('parameter', 'value', 'error'), vals, session.log.info)
    return FitResult((tuple(res._pars[1]), tuple(res._pars[2])))

poly.__doc__ += COLHELP.replace('func(', 'poly(2, ')


@usercommand
@helparglist('[[xcol, ]ycol]')
def gauss(*columns):
    """Fit a Gaussian through the data of the last scan.

    The return value is a pair of tuples::

        ((x0, ampl, sigma, background), (d_x0, d_ampl, d_sigma, d_back))

    where the elements of the second tuple are the estimated standard errors of
    the fit parameters.  The fit parameters are:

    * x0 - center of the Gaussian
    * ampl - amplitude
    * fwhm - FWHM
    * background

    If the fit failed, the result is ``(None, None)``.

    Example::

        qscan(...)
        values, stderr = gauss('h', 'det2')
        if values:  # if the fit was successful
            center = values[0]
            # now work with fitted peak center
    """
    xs, ys, dys, _, ds = _getData(columns)
    fit = GaussFit([0.5*(xs[0]+xs[-1]), ys.max(), (xs[1]-xs[0])*5, 0])
    res = fit.run(xs, ys, dys)
    if res._failed:
        return None, None
    session.notifyFitCurve(ds, 'gauss', res.curve_x, res.curve_y)
    descrs = ['center', 'amplitude', 'FWHM', 'background']
    vals = []
    for par, err, descr in zip(res._pars[1], res._pars[2], descrs):
        vals.append((descr, '%.4f' % par, '%.4f' % err))
    printTable(('parameter', 'value', 'error'), vals, session.log.info)
    return FitResult((tuple(res._pars[1]), tuple(res._pars[2])))

gauss.__doc__ += COLHELP.replace('func(', 'gauss(')


@usercommand
@helparglist('dev, center, step, numpoints, ...')
def center(dev, center, step, numpoints, *args, **kwargs):
    """Move the given device to the maximum of a Gaussian fit through a scan.

    The scan is performed around *center* with the given parameters.

    This supports all arguments and keyword arguments that `cscan()` supports,
    and additionally a keyword "ycol" that gives the Y column of the dataset to
    use for the Gaussian fit (see the help for `gauss()` for the meaning of
    this parameter).
    """
    ycol = kwargs.pop('ycol', -1)
    cscan(dev, center, step, numpoints, 'centering', *args, **kwargs)
    params, _ = gauss(ycol)
    # do not allow moving outside of the scanned region
    minvalue = center - step*numpoints
    maxvalue = center + step*numpoints
    if params is None:
        session.log.warning('Gaussian fit failed, no centering done')
    elif not minvalue <= params[0] <= maxvalue:
        session.log.warning('Gaussian fit resulted in center outside scanning '
                            'area, no centering done')
    else:
        session.log.info('centered peak for %s', dev)
        maw(dev, params[0])


@usercommand
@helparglist('dev, center, step, numpoints, ...')
def checkoffset(dev, center, step, numpoints, *args, **kwargs):
    """Readjust offset of the given device to the center of a scan.

    The adjustment is done so that afterwards, the given *center* coincides
    with the center of a Gaussian fit through the scan performed with the given
    stepsize and number of points.

    This supports all arguments and keyword arguments that `cscan()` supports,
    and additionally a keyword "ycol" that gives the Y column of the dataset to
    use for the Gaussian fit (see the help for `gauss()` for the meaning of
    this parameter).
    """
    ycol = kwargs.pop('ycol', -1)
    cscan(dev, center, step, numpoints, 'offset check', *args, **kwargs)
    params, _ = gauss(ycol)
    # do not allow moving outside of the scanned region
    minvalue = center - step*numpoints
    maxvalue = center + step*numpoints
    if params is None:
        session.log.warning('Gaussian fit failed, offset unchanged')
    elif not minvalue <= params[0] <= maxvalue:
        session.log.warning('Gaussian fit resulted in center outside scanning '
                            'area, offset unchanged')
    else:
        diff = params[0] - center
        session.log.info('center of Gaussian fit at %s',
                         dev.format(params[0], True))
        session.log.info('adjusting offset of %s by %s',
                         dev, dev.format(diff, True))
        dev.offset += diff


@usercommand
@helparglist('[[xcol, ]ycol][, npoints=n]')
def findpeaks(*columns, **kwds):
    """Find peaks the data of the last scan.

    Peaks are determined by the property that a data point is bigger than some
    neighbors (by default 2) on every side.  Then a parabola is fitted to these
    points, which gives a good approximation to the peak center position.

    The return value is a list of possible X values of peaks.

    The following keyword arguments are accepted:

    * *npoints* -- number of neighbors (default 2) per side of peak to be
      considered: if the scan is very fine, this must be increased
    """
    # parabola model
    def model(x, b, s, c):
        return b + s*(x-c)**2
    xs, ys, dys = _getData(columns)[:3]
    np = kwds.get('npoints', 2)
    peaks = []
    # peak has to be different from background
    minpeakheight = (ys.max() - ys.min()) * 0.1 + ys.min()
    for i in range(len(xs) - 2*np):
        subys = ys[i:i+2*np+1]
        subdys = dys[i:i+2*np+1]
        # need a peak of at least minpeakheight
        if subys.max() < minpeakheight:
            continue
        # peak must be bigger than sides - including errors!
        miny = subys[np] - subdys[np]
        if (subys[0] + subdys[0] > miny) or \
           (subys[2*np] + subdys[2*np] > miny):
            continue
        # values must rise to peak and fall down
        for v in range(np):
            if subys[v] > subys[v+1] or subys[v+np] < subys[v+np+1]:
                break
        else:
            # we (probably) have a peak
            subxs = xs[i:i+2*np+1]
            b = subys[np]
            s = (subys[0] - subys[np])/(subxs[0] - subxs[np])**2
            c = subxs[np]
            fit = Fit('parabola', model, ['b', 's', 'c'], [b, s, c])
            res = fit.run(subxs, subys, subdys)
            if not res._failed:
                peaks.append(res._pars[1][2])

    return peaks

findpeaks.__doc__ += COLHELP.replace('func(', 'findpeaks(')
