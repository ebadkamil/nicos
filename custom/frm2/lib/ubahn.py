#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2012 by the NICOS contributors (see AUTHORS)
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

"""Show next U-Bahn departure from Garching Forschungszentrum."""

__version__ = "$Revision$"

from nicos.core import Readable, Override, NicosError, status

URL = ('http://www.mvg-live.de/ims/dfiStaticAnzeige.svc?'
       'haltestelle=Garching-Forschungszentrum')

try:
    from lxml.html import parse
except ImportError:
    parse = None


class UBahn(Readable):

    parameter_overrides = {
        'unit':         Override(mandatory=False, default='min'),
        'fmtstr':       Override(default='%d'),
        'pollinterval': Override(default=60),
        'maxage':       Override(default=120),
    }

    def doRead(self, maxage=0):
        if parse is None:
            raise NicosError(self, 'cannot parse web page, lxml is not '
                             'installed on this system')
        try:
            tree = parse(URL)
            return int(tree.find('//td[@class="inMinColumn"]').text)
        except Exception, err:
            raise NicosError(self, 'MVG site not responding or changed format: '
                             '%s' % err)

    def doStatus(self, maxage=0):
        return status.OK, ''
