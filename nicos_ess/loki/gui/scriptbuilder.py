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
#   Georg Brandl <georg.brandl@frm2.tum.de>
#
# *****************************************************************************

"""NICOS GUI multiple cmdlet script-builder input."""

from nicos.clients.gui.cmdlets import all_categories, all_cmdlets
from nicos.clients.gui.utils import loadUi
from nicos.guisupport.qt import QAction, QMenu, QToolButton, pyqtSlot
from nicos.utils import importString, findResource

from nicos_ess.loki.gui.loki_panel import LokiPanelBase


class CommandsPanel(LokiPanelBase):
    """Provides a panel to create via click-and-choose multiple NICOS commands.

    This panel allows the user to create a series of NICOS commands with
    cmdlets (similar to the `.cmdbuilder.CommandPanel` but for multiple
    commands).

    Options:

    * ``modules`` (default [ ]) -- list of additional Python modules that
      contain cmdlets and should be loaded.
    """
    panelName = 'Commands'

    def __init__(self, parent, client, options):
        LokiPanelBase.__init__(self, parent, client, options)
        loadUi(self,
               findResource('nicos_ess/loki/gui/ui_files/scriptbuilder.ui'))

        self.window = parent
        self.runBtn.setVisible(False)
        self.mapping = {}
        self.expertmode = self.mainwindow.expertmode

        self._cmdlet = self.sender()
        self._layout = self.frame.layout()
        self.index = self._layout.indexOf(self._cmdlet)

        self.initialise_connection_status_listeners()

        modules = options.get('modules', [])
        for module in modules:
            importString(module)  # should register cmdlets

        for cmdlet in all_cmdlets:
            def callback(on, cmdlet=cmdlet):
                inst = cmdlet(self, self.client)
                inst.cmdletUp.connect(self.on_cmdletUp)
                inst.cmdletDown.connect(self.on_cmdletDown)
                inst.cmdletRemove.connect(self.on_cmdletRemove)
                self.runBtn.setVisible(True)
                self.frame.layout().insertWidget(
                    self.frame.layout().count() - 2, inst)
            action = QAction(cmdlet.name, self)
            action.triggered.connect(callback)
            self.mapping.setdefault(cmdlet.category, []).append(action)

        for category in all_categories[::-1]:
            if category not in self.mapping:
                return
            toolbtn = QToolButton(self)
            toolbtn.setText(category)
            toolbtn.setPopupMode(QToolButton.InstantPopup)
            menu = QMenu(self)
            menu.addActions(self.mapping[category])
            toolbtn.setMenu(menu)
            self.btnLayout.insertWidget(1, toolbtn)

    def setExpertMode(self, expert):
        self.expertmode = expert

    def setViewOnly(self, viewonly):
        """
        While the commands still be visible, they will be disabled.
        They can be made un-visible but the UI frame is not dynamically adjust
        itself thus leading a big gray area which is not pleasing.

        Disabling each cmdlet seems not possible via direct call to them, thus
        we disable the frame.
        """
        self.frame.setEnabled(not viewonly)

    def on_client_connected(self):
        self.frame.setEnabled(True)

    def on_client_disconnected(self):
        self.frame.setEnabled(False)

    def on_cmdletRemove(self):
        self._layout.removeWidget(self._cmdlet)
        self._cmdlet.hide()

        if self._layout.count() < 3:
            self.runBtn.setVisible(False)

    def on_cmdletUp(self):
        if not self.index:
            return

        self._layout.removeWidget(self._cmdlet)
        self._layout.insertWidget(self.index - 1, self._cmdlet)

    def on_cmdletDown(self):
        if self.index >= (self._layout.count() - 3):
            return

        self._layout.removeWidget(self._cmdlet)
        self._layout.insertWidget(self.index + 1, self._cmdlet)

    @pyqtSlot()
    def on_runBtn_clicked(self):
        code = ''
        valid = True
        mode = 'python'
        if self.client.eval('session.spMode', False):
            mode = 'simple'
        for i in range(self._layout.count() - 2):
            cmdlet = self._layout.itemAt(i).widget()
            valid = valid and cmdlet.isValid()
            generated = cmdlet.generate(mode)
            if not generated.endswith('\n'):
                generated += '\n'
            code += generated
        if not valid:
            return
        self.mainwindow.codeGenerated.emit(code)
