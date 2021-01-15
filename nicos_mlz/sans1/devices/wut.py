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
#   Andreas Wilhelm <andreas.wilhelm@frm2.tum.de>
#
# *****************************************************************************

"""Show values read out from a w&t web UI.

w&t box shows pressore before and after the filter at the instrument.
"""

import urllib

from nicos.core import Attach, CommunicationError, ConfigurationError, \
    Override, Param, Readable, status


class WutValue(Readable):

    parameters = {
        'hostname':     Param('Host name of the wut site',
                              type=str, mandatory=True),
        'port':         Param('Port of the sensor',
                              type=str, mandatory=True),
    }

    parameter_overrides = {
        'unit':         Override(mandatory=False),
        'pollinterval': Override(default=60),
        'maxage':       Override(default=125),
    }

    def _getRaw(self):
        url = 'http://%s/Single%s' % (self.hostname, self.port)
        try:
            response = urllib.request.urlopen(url)
            html = response.read()
            return str(html)
        except ConfigurationError:  # pass through error raised above
            raise
        except Exception as err:
            raise CommunicationError(
                self, 'wut-box not responding or changed format: %s' % err
            ) from err

    def _extractUnit(self, raw):
        return raw.split(';')[-1].split(' ')[-1]

    def _extractValue(self, raw):
        return float(raw.split(';')[-1].split(' ')[0].replace(',', '.'))

    def doReadUnit(self):
        return self._extractUnit(self._getRaw())

    def doRead(self, maxage=0):
        return self._extractValue(self._getRaw())

    def doStatus(self, maxage=0):
        return status.OK, ''


class WutDiff(Readable):

    attached_devices = {
        'dev1': Attach('1st Device', Readable),
        'dev2': Attach('2nd Device', Readable),
    }

    parameter_overrides = {
        'unit':         Override(mandatory=False),
        'pollinterval': Override(default=60),
        'maxage':       Override(default=125),
    }

    def doReadUnit(self):
        return self._attached_dev1.unit

    def doRead(self, maxage=0):
        return self._attached_dev1.doRead(maxage) - \
            self._attached_dev2.doRead(maxage)

    def doStatus(self, maxage=0):
        return status.OK, ''
