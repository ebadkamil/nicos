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
#   AÜC Hardal <umit.hardal@ess.eu>
#
# *****************************************************************************
from nicos import session
from nicos.commands import usercommand
from nicos_ess.devices.datasinks.file_writer import FileWriterControl


@usercommand
def start_writing():
    dev = _find_filewriter_device()
    if dev:
        dev.doStart()
        return
    session.log.error("Could not find file-writer control device")


@usercommand
def stop_writing():
    dev = _find_filewriter_device()
    if dev:
        dev.doStop()
        return
    session.log.error("Could not find file-writer control device")


def _find_filewriter_device():
    for dev in session.devices.values():
        if isinstance(dev, FileWriterControl):
            # Should be only one
            return dev
    return None



