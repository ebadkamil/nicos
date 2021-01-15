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
#   Georg Brandl <georg.brandl@frm2.tum.de>
#   Christian Felder <c.felder@fz-juelich.de>
#
# *****************************************************************************

"""NICOS GUI main window."""

from time import time as current_time

from nicos.clients.gui.mainwindow import MainWindow as DefaultMainWindow
from nicos.guisupport.qt import QApplication, QFileDialog, QIcon, QLabel, \
    QMenu, QPixmap, QPoint, QSize, QSizePolicy, Qt, QWidget, pyqtSlot

from nicos_ess.gui import uipath
from nicos_ess.gui.panels import get_icon


def decolor_logo(pixmap, color):
    ret_pix = QPixmap(pixmap.size())
    ret_pix.fill(color)
    ret_pix.setMask(pixmap.createMaskFromColor(Qt.transparent))
    return ret_pix


class Spacer(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)


class MainWindow(DefaultMainWindow):
    ui = '%s/main.ui' % uipath

    def __init__(self, log, gui_conf, viewonly=False, tunnel=''):
        DefaultMainWindow.__init__(self, log, gui_conf, viewonly, tunnel)
        self.add_logo()
        self.set_icons()
        self.style_file = gui_conf.stylefile

        # Cheeseburger menu
        dropdown = QMenu('')
        dropdown.addAction(self.actionConnect)
        dropdown.addAction(self.actionViewOnly)
        dropdown.addAction(self.actionPreferences)
        dropdown.addAction(self.actionExpert)
        dropdown.addSeparator()
        dropdown.addAction(self.actionExit)
        self.actionUser.setMenu(dropdown)
        self.actionUser.setIconVisibleInMenu(True)
        self.dropdown = dropdown
        self.actionExpert.setEnabled(self.client.isconnected)
        self.actionEmergencyStop.setEnabled(self.client.isconnected)

        self._init_instrument_name()
        self._init_experiment_name()

    def _init_toolbar(self):
        self.statusLabel = QLabel('', self, pixmap=QPixmap(':/disconnected'),
                                  margin=5, minimumSize=QSize(30, 10))
        self.statusLabel.setStyleSheet('color: white')

        self.toolbar = self.toolBarRight
        self.toolbar.addWidget(self.statusLabel)
        self.setStatus('disconnected')

    def _init_experiment_name(self):
        self.experiment_text = QLabel()
        self.experiment_text.setSizePolicy(QSizePolicy.Expanding,
                                           QSizePolicy.Preferred)
        self.experiment_text.setStyleSheet('font-size: 17pt; font-weight: bold')
        self.toolBarMain.addWidget(self.experiment_text)

        self.experiment_label = QLabel()
        self.experiment_label.setSizePolicy(QSizePolicy.Expanding,
                                            QSizePolicy.Preferred)
        self.experiment_label.setStyleSheet('font-size: 17pt')
        self.toolBarMain.addWidget(self.experiment_label)

    def _init_instrument_name(self):
        self.instrument_text = QLabel()
        self.instrument_text.setSizePolicy(QSizePolicy.Expanding,
                                           QSizePolicy.Preferred)
        self.instrument_text.setStyleSheet('font-size: 17pt; font-weight: bold')
        self.toolBarMain.addWidget(self.instrument_text)

        self.instrument_label = QLabel()
        self.instrument_label.setSizePolicy(QSizePolicy.Expanding,
                                            QSizePolicy.Preferred)
        self.instrument_label.setStyleSheet('font-size: 17pt')
        self.toolBarMain.addWidget(self.instrument_label)

    def set_icons(self):
        self.actionUser.setIcon(
            get_icon('settings_applications-24px.svg'))
        self.actionEmergencyStop.setIcon(get_icon('emergency_stop.svg'))
        self.actionConnect.setIcon(get_icon('power-24px.svg'))
        self.actionExit.setIcon(get_icon('exit_to_app-24px.svg'))
        self.actionViewOnly.setIcon(get_icon('lock-24px.svg'))
        self.actionPreferences.setIcon(get_icon('tune-24px.svg'))
        self.actionExpert.setIcon(get_icon('fingerprint-24px.svg'))

    def add_logo(self):
        logo_label = QLabel()
        pxr = decolor_logo(QPixmap("resources/logo-icon.png"), Qt.white)
        logo_label.setPixmap(pxr.scaledToHeight(self.toolBarMain.height(),
                                                Qt.SmoothTransformation))
        logo_label.setMargin(5)
        self.toolBarMain.insertWidget(self.toolBarMain.actions()[0], logo_label)

        nicos_label = QLabel()
        pxr = decolor_logo(QPixmap("resources/nicos-logo-high.svg"), Qt.white)
        nicos_label.setPixmap(pxr.scaledToHeight(self.toolBarMain.height(),
                                                 Qt.SmoothTransformation))
        self.toolBarMain.insertWidget(self.toolBarMain.actions()[1],
                                      nicos_label)

    def update_instrument_text(self):
        instrument = self.client.eval('session.instrument', None)
        self.instrument_text.setText('Instrument:')
        if instrument:
            logo = decolor_logo(QPixmap(f'resources/{instrument}-logo.svg'),
                                Qt.white)
            if logo.isNull():
                self.instrument_label.setText(instrument.upper())
                return
            self.instrument_label.setPixmap(logo.scaledToHeight(
                self.toolBarMain.height(), Qt.SmoothTransformation))
        else:
            self.instrument_label.setText('UNKNOWN')

    def update_experiment_text(self):
        max_text_length = 50
        experiment = self.client.eval('session.experiment.title', None)
        if experiment is not None:
            self.experiment_text.setText("     Experiment:")
            self.experiment_label.setText(experiment[0:max_text_length])

    def remove_experiment_and_instrument(self):
        self.experiment_label.clear()
        self.experiment_text.clear()
        self.instrument_label.clear()
        self.instrument_text.clear()

    def reloadQSS(self):
        self.setQSS(self.stylefile)

    def selectQSS(self):
        style_file = QFileDialog.getOpenFileName(
            self, filter="Qt Stylesheet Files (*.qss)")[0]
        if style_file:
            self.style_file = style_file
            self.setQSS(self.style_file)

    @staticmethod
    def setQSS(style_file):
        with open(style_file, 'r') as fd:
            try:
                QApplication.instance().setStyleSheet(fd.read())
            except Exception as e:
                print(e)

    def setStatus(self, status, exception=False):
        if status == self.current_status:
            return
        if self.client.last_action_at and \
           self.current_status == 'running' and \
           status in ('idle', 'paused') and \
           current_time() - self.client.last_action_at > 20:
            # show a visual indication of what happened
            if status == 'paused':
                msg = 'Script is now paused.'
            elif exception:
                msg = 'Script has exited with an error.'
            else:
                msg = 'Script has finished.'
            self.trayIcon.showMessage(self.instrument, msg)
            self.client.last_action_at = 0
        self.current_status = status
        is_connected = status != 'disconnected'
        if is_connected:
            self.actionConnect.setText('Disconnect')
            self.statusLabel.setText('\u2713 Connected')
            self.update_instrument_text()
            self.update_experiment_text()
        else:
            self.actionConnect.setText('Connect to server...')
            self.statusLabel.setText('Disconnected')
            self.setTitlebar(False)
        # new status icon
        pixmap = QPixmap(':/' + status + ('exc' if exception else ''))
        new_icon = QIcon()
        new_icon.addPixmap(pixmap, QIcon.Disabled)
        self.trayIcon.setIcon(new_icon)
        self.trayIcon.setToolTip('%s status: %s' % (self.instrument, status))
        if self.showtrayicon:
            self.trayIcon.show()
        if self.promptWindow and status != 'paused':
            self.promptWindow.close()
        # propagate to panels
        for panel in self.panels:
            panel.updateStatus(status, exception)
        for window in self.windows.values():
            for panel in window.panels:
                panel.updateStatus(status, exception)

    def on_client_connected(self):
        DefaultMainWindow.on_client_connected(self)
        self.actionConnect.setIcon(
            QIcon("resources/material/icons/power_off-24px.svg"))
        self.actionExpert.setEnabled(True)
        self.actionEmergencyStop.setEnabled(not self.client.viewonly)

    def on_client_disconnected(self):
        DefaultMainWindow.on_client_disconnected(self)
        self.remove_experiment_and_instrument()
        self.actionConnect.setIcon(
            QIcon("resources/material/icons/power-24px.svg"))
        self.actionExpert.setEnabled(False)
        self.actionExpert.setChecked(False)
        self.actionEmergencyStop.setEnabled(False)

    def on_actionViewOnly_toggled(self, on):
        DefaultMainWindow.on_actionViewOnly_toggled(self, on)
        if self.client.isconnected:
            self.actionEmergencyStop.setEnabled(not self.client.viewonly)
        else:
            self.actionEmergencyStop.setEnabled(False)

    @pyqtSlot(bool)
    def on_actionConnect_triggered(self, _):
        # connection or disconnection request?
        connection_req = self.current_status == "disconnected"
        super().on_actionConnect_triggered(connection_req)

    @pyqtSlot()
    def on_actionUser_triggered(self):
        w = self.toolBarRight.widgetForAction(self.actionUser)
        self.dropdown.popup(w.mapToGlobal(QPoint(0, w.height())))

    @pyqtSlot()
    def on_actionEmergencyStop_triggered(self):
        self.client.tell_action('emergency')
