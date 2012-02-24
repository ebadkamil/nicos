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
#   Björn Pedersen <bjoern.pedersen@frm2.tum.de>
#
# *****************************************************************************

"""
Created on 30.05.2011

@author: pedersen
"""

__version__ = "$Revision$"

import sys
sys.path.append('/home/pedersen/Eclispe_projects_git/singlecounter')
sys.path.append('/home/pedersen/Eclispe_projects/nonius_new/app')
from nicos.core import Moveable, Param #@UnusedImport  pylint: disable=W0611
from sc_scan_new import HuberScan #pylint: disable=F0401
from goniometer import position

class ResiPositionProxy(object):
    """
    proxy class to make  position objects really picklable

    see: http://code.activestate.com/recipes/252151-generalized-delegates-and-proxies/
    """
    __hardware = None
    pos = None

    def __init__(self,pos):
        #super(ResiPositionProxy, self).__init__(pos)
        self.pos = pos

    @classmethod
    def SetHardware(cls,hw):
        ResiPositionProxy.__hardware = hw

    def __getattr__(self,name):
        return getattr(self.pos,name)
    def __setattr__(self,name,value):
        if name == 'pos':
            self.__dict__[name]=value
        elif self.pos:
            return setattr(self.pos,name,value)

    def __repr__(self):
        return self.pos.__repr__()

    def __getstate__(self):
        return self.pos.storable()
    def __setstate__(self,state):
        self.pos = position.PositionFromStorage(ResiPositionProxy.__hardware, state)

class ResiDevice(Moveable):
    '''
    classdocs
    '''
    name = None

    def doPreinit(self):
        '''
        Constructor
        '''

        self._hardware = HuberScan()
        self._hardware.LoadRmat()
        #    self._hardware.SetCellParam(a=4.9287, b=4.9287, c=5.3788, alpha=90.000, beta=90.000, gamma=120.000)
        self._hardware.cell.conventionalsystem = 'triclinic'
        self._hardware.cell.standardize = 0
        self._hardware.cell.pointgroup = '1'
        self._hardware.bisect.cell = self._hardware.cell
        ResiPositionProxy.SetHardware(self._hardware)
        #self.loglevel='debug'

    def doRead(self):
        return ResiPositionProxy(self._hardware.GetPosition())

    def doMove(self, *kw, **args):
        return self._hardware.Goto(*kw, **args)

    def doStart(self,*kw, **args):
        self._hardware.Goto(*kw, **args)

    def doInfo(self):
        info = list()
        info.append(('experiment', 'position',  ResiPositionProxy(self._hardware.GetPosition())))
        info.append(('experiment', 'reflex', self._hardware.current_reflex))
        info.append(('sample', 'cell', self._hardware.cell))
        return info

