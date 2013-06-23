#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2013 by the NICOS contributors (see AUTHORS)
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

"""NICOS GUI main window and application startup."""

import os
import sys
import time
import logging
import subprocess
from os import path

from PyQt4.QtGui import QApplication, QMainWindow, QDialog, QMessageBox, \
     QLabel, QSystemTrayIcon, QStyle, QPixmap, QMenu, QIcon, QAction, \
     QFontDialog, QColorDialog
from PyQt4.QtCore import Qt, QTimer, QSize, QVariant, SIGNAL
from PyQt4.QtCore import pyqtSignature as qtsig

from nicos import nicos_version
from nicos.utils import parseConnectionString, importString, enumerate_start
from nicos.utils.loggers import ColoredConsoleHandler, NicosLogfileHandler, \
     NicosLogger, initLoggers
from nicos.clients.gui.data import DataHandler
from nicos.clients.gui.client import NicosGuiClient
from nicos.clients.gui.utils import DlgUtils, SettingGroup, loadUi, \
     loadBasicWindowSettings, loadUserStyle, getXDisplay
from nicos.clients.gui.config import panel_config
from nicos.clients.gui.panels import AuxiliaryWindow, createWindowItem
from nicos.clients.gui.panels.console import ConsolePanel
from nicos.clients.gui.dialogs.auth import ConnectionDialog
from nicos.clients.gui.dialogs.pnp import PnPSetupQuestion
from nicos.clients.gui.dialogs.help import HelpWindow
from nicos.clients.gui.dialogs.settings import SettingsDialog
from nicos.clients.gui.dialogs.watchdog import WatchdogDialog
from nicos.protocols.daemon import DEFAULT_PORT, STATUS_INBREAK, STATUS_IDLE, \
     STATUS_IDLEEXC


class MainWindow(QMainWindow, DlgUtils):
    def __init__(self, log, panel_conf):
        QMainWindow.__init__(self)
        DlgUtils.__init__(self, 'NICOS')
        loadUi(self, 'main.ui')

        # our logger instance
        self.log = log

        # window for displaying errors
        self.errorWindow = None

        # log messages sent by the server
        self.messages = []

        # set-up the initial connection data
        self.connectionData = dict(
            host    = 'localhost',
            port    = 1301,
            login   = '',
            display = getXDisplay(),
        )
        self.lastpasswd = None

        # state members
        self.current_status = None
        self.action_start_time = None

        # connect the client's events
        self.client = NicosGuiClient(self)
        self.connect(self.client, SIGNAL('error'), self.on_client_error)
        self.connect(self.client, SIGNAL('broken'), self.on_client_broken)
        self.connect(self.client, SIGNAL('failed'), self.on_client_failed)
        self.connect(self.client, SIGNAL('connected'), self.on_client_connected)
        self.connect(self.client, SIGNAL('disconnected'),
                     self.on_client_disconnected)
        self.connect(self.client, SIGNAL('status'), self.on_client_status)
        self.connect(self.client, SIGNAL('showhelp'), self.on_client_showhelp)
        self.connect(self.client, SIGNAL('clientexec'), self.on_client_clientexec)
        self.connect(self.client, SIGNAL('plugplay'), self.on_client_plugplay)
        self.connect(self.client, SIGNAL('watchdog'), self.on_client_watchdog)
        self.connect(self.client, SIGNAL('setup'), self.on_client_setup)

        # data handling setup
        self.data = DataHandler(self.client)

        # panel configuration
        self.panel_conf = panel_conf

        # determine if there is an editor window type, because we would like to
        # have a way to open files from a console panel later
        self.editor_wintype = self.panel_conf.find_panel(
            'nicos.clients.gui.panels.editor.EditorPanel')
        self.history_wintype = self.panel_conf.find_panel(
            'nicos.clients.gui.panels.history.HistoryPanel')

        # additional panels
        self.panels = []
        self.splitters = []
        self.windowtypes = []
        self.windows = {}
        self.mainwindow = self

        self.sgroup = SettingGroup('MainWindow')
        with self.sgroup as settings:
            loadUserStyle(self, settings)

        # create panels in the main window
        widget = createWindowItem(self.panel_conf.windows[0], self, self)
        self.centralLayout.addWidget(widget)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        # load saved settings and stored layout for panel config
        with self.sgroup as settings:
            self.loadSettings(settings)

        if len(self.splitstate) == len(self.splitters):
            for sp, st in zip(self.splitters, self.splitstate):
                sp.restoreState(st.toByteArray())

        if not self.panel_conf.windows[1:]:
            self.menuBar().removeAction(self.menuWindows.menuAction())

        for i, wconfig in enumerate_start(self.panel_conf.windows[1:], 1):
            action = QAction(QIcon(':/' + wconfig[1]), wconfig[0], self)
            self.toolBarWindows.addAction(action)
            self.menuWindows.addAction(action)
            def window_callback(on, i=i):
                self.createWindow(i)
            self.connect(action, SIGNAL('triggered(bool)'), window_callback)

        # load tools menu
        for i, tconfig in enumerate(self.panel_conf.tools):
            action = QAction(tconfig[0], self)
            self.menuTools.addAction(action)
            def tool_callback(on, i=i):
                self.runTool(i)
            self.connect(action, SIGNAL('triggered(bool)'), tool_callback)

        # timer for reconnecting
        self.reconnectTimer = QTimer(singleShot=True, timeout=self._reconnect)
        self._reconnecting = False

        # setup tray icon
        self.trayIcon = QSystemTrayIcon(self)
        self.connect(self.trayIcon,
                     SIGNAL('activated(QSystemTrayIcon::ActivationReason)'),
                     self.on_trayIcon_activated)
        self.trayMenu = QMenu(self)
        nameAction = self.trayMenu.addAction(self.instrument)
        nameAction.setEnabled(False)
        self.trayMenu.addSeparator()
        toggleAction = self.trayMenu.addAction('Hide main window')
        toggleAction.setCheckable(True)
        self.connect(toggleAction, SIGNAL('triggered(bool)'),
                     lambda hide: self.setVisible(not hide))
        self.trayIcon.setContextMenu(self.trayMenu)

        self.statusLabel = QLabel('', self, pixmap=QPixmap(':/disconnected'),
                                  margin=5, minimumSize=QSize(30, 10))
        self.toolBarMain.addWidget(self.statusLabel)

        # help window
        self.helpWindow = None
        # watchdog window
        self.watchdogWindow = None
        # plug-n-play notification windows
        self.pnpWindows = {}

        # create initial state
        self.setStatus('disconnected')

    def createWindow(self, wtype):
        try:
            wconfig = self.panel_conf.windows[wtype]
        except IndexError:
            # config outdated, window type doesn't exist
            return
        if wtype in self.windows:
            window = self.windows[wtype]
            window.activateWindow()
            return window
        window = AuxiliaryWindow(self, wtype, wconfig)
        window.setWindowIcon(QIcon(':/' + wconfig[1]))
        self.windows[wtype] = window
        self.connect(window, SIGNAL('closed'), self.on_auxWindow_closed)
        for panel in window.panels:
            panel.updateStatus(self.current_status)
        window.show()
        return window

    def on_auxWindow_closed(self, window):
        del self.windows[window.type]

    def runTool(self, ttype):
        tconfig = self.panel_conf[2][ttype]
        try:
            # either it's a class name
            toolclass = importString(tconfig[1])
        except ImportError:
            # or it's a system command
            subprocess.Popen(tconfig[1], shell=True)
        else:
            dialog = toolclass(self, self.client, **tconfig[2])
            dialog.setWindowModality(Qt.NonModal)
            dialog.show()

    def setConnData(self, login, passwd, host, port):
        self.connectionData['login'] = login
        self.connectionData['host'] = host
        self.connectionData['port'] = port

    def _reconnect(self):
        if self.lastpasswd is not None:
            self.client.connect(self.connectionData, self.lastpasswd)

    def show(self):
        QMainWindow.show(self)
        if self.autoconnect and not self.client.connected:
            self.on_actionConnect_triggered(True)

    def loadSettings(self, settings):
        # geometry and window appearance
        loadBasicWindowSettings(self, settings)

        self.autoconnect = settings.value('autoconnect').toBool()

        self.connpresets = dict((str(k), v) for (k, v) in
            (settings.value('connpresets').toPyObject() or {}).iteritems())
        self.lastpreset = str(settings.value('lastpreset').toString())
        if self.lastpreset in self.connpresets:
            cdata = self.connpresets[self.lastpreset]
            self.connectionData['host']  = str(cdata[0])
            self.connectionData['port']  = int(cdata[1])
            self.connectionData['login'] = str(cdata[2])

        self.instrument = settings.value('instrument').toString()
        self.confirmexit = settings.value('confirmexit',
                                          QVariant(True)).toBool()
        self.showtrayicon = settings.value('showtrayicon',
                                           QVariant(True)).toBool()
        self.autoreconnect = settings.value('autoreconnect',
                                            QVariant(True)).toBool()

        self.update()

        open_wintypes = settings.value('auxwindows').toList()
        for wtype in [x.toInt()[0] for x in open_wintypes]:
            self.createWindow(wtype)

    def saveSettings(self, settings):
        settings.setValue('geometry', QVariant(self.saveGeometry()))
        settings.setValue('windowstate', QVariant(self.saveState()))
        settings.setValue('splitstate',
                          QVariant([sp.saveState() for sp in self.splitters]))
        open_wintypes = self.windows.keys()
        settings.setValue('auxwindows', QVariant(open_wintypes))
        settings.setValue('autoconnect', QVariant(self.client.connected))
        settings.setValue('connpresets', self.connpresets)
        settings.setValue('lastpreset', self.lastpreset)
        settings.setValue('font', QVariant(self.user_font))
        settings.setValue('color', QVariant(self.user_color))

    def closeEvent(self, event):
        if self.confirmexit and QMessageBox.question(
            self, 'Quit', 'Do you really want to quit?',
            QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
            event.ignore()
            return

        for panel in self.panels:
            if not panel.requestClose():
                event.ignore()
                return

        with self.sgroup as settings:
            self.saveSettings(settings)
        for panel in self.panels:
            with panel.sgroup as settings:
                panel.saveSettings(settings)

        for window in self.windows.values():
            if not window.close():
                event.ignore()
                return

        if self.helpWindow:
            self.helpWindow.close()

        if self.client.connected:
            self.client.disconnect()

        event.accept()

    def setTitlebar(self, connected, setups=()):
        inststr = str(self.instrument) or 'NICOS'
        if connected:
            hoststr = '%s at %s:%s' % (self.client.login, self.client.host,
                                       self.client.port)
            self.setWindowTitle('%s [%s] - %s' % (inststr, ', '.join(setups),
                                                  hoststr))
        else:
            self.setWindowTitle('%s - disconnected' % inststr)

    def setStatus(self, status, exception=False):
        if status == self.current_status:
            return
        if self.action_start_time and self.current_status == 'running' and \
           status in ('idle', 'interrupted') and \
           time.time() - self.action_start_time > 20:
            # show a visual indication of what happened
            if status == 'interrupted':
                msg = 'Script is now interrupted.'
            elif exception:
                msg = 'Script has exited with an error.'
            else:
                msg = 'Script has finished.'
            self.trayIcon.showMessage(self.instrument, msg)
            self.action_start_time = None
        self.current_status = status
        isconnected = status != 'disconnected'
        self.actionConnect.setChecked(isconnected)
        if isconnected:
            self.actionConnect.setText('Disconnect')
        else:
            self.actionConnect.setText('Connect to server...')
            self.setTitlebar(False)
        # new status icon
        pixmap = QPixmap(':/' + status + ('exc' if exception else ''))
        self.statusLabel.setPixmap(pixmap)
        self.statusLabel.setToolTip('Script status: %s' % status)
        newicon = QIcon()
        newicon.addPixmap(pixmap, QIcon.Disabled)
        self.trayIcon.setIcon(newicon)
        self.trayIcon.setToolTip('%s status: %s' % (self.instrument, status))
        if self.showtrayicon:
            self.trayIcon.show()
        # propagate to panels
        for panel in self.panels:
            panel.updateStatus(status, exception)
        for window in self.windows.itervalues():
            for panel in window.panels:
                panel.updateStatus(status, exception)

    def on_client_error(self, problem, exc=None):
        if exc is not None:
            self.log.error('Error from daemon', exc=exc)
        problem = time.strftime('[%m-%d %H:%M:%S] ') + problem
        if self.errorWindow is None:
            self.errorWindow = QDialog(self)
            def reset_errorWindow():
                self.errorWindow = None
            self.errorWindow.connect(self.errorWindow, SIGNAL('accepted()'),
                                     reset_errorWindow)
            loadUi(self.errorWindow, 'error.ui')
            self.errorWindow.setWindowTitle('Connection error')
            self.errorWindow.errorText.setText(problem)
            self.errorWindow.iconLabel.setPixmap(
                self.style().standardIcon(QStyle.SP_MessageBoxWarning).
                pixmap(32, 32))
            self.errorWindow.show()
        else:
            self.errorWindow.errorText.setText(
                self.errorWindow.errorText.text() + '\n' + problem)

    def on_client_broken(self, problem):
        self.on_client_error(problem)
        if self.autoreconnect:
            self._reconnecting = True
            self.reconnectTimer.start(500)  # half a second

    def on_client_failed(self, problem):
        if not self._reconnecting:
            self.on_client_error(problem)
        elif self.autoreconnect:
            self.reconnectTimer.start(500)

    def on_client_connected(self):
        self.setStatus('idle')
        self._reconnecting = False

        # get all server status info
        initstatus = self.client.ask('getstatus')
        # handle setups
        self.setTitlebar(True, initstatus['setups'][1])
        # handle initial status
        self.on_client_status(initstatus['status'])
        # propagate info to all components
        self.client.signal('initstatus', initstatus)

        # set focus to command input, if present
        for panel in self.panels:
            if isinstance(panel, ConsolePanel) and panel.hasinput:
                panel.commandInput.setFocus()

    def on_client_setup(self, data):
        self.setTitlebar(True, data[1])

    def on_client_status(self, data):
        status = data[0]
        if status == STATUS_IDLE:
            self.setStatus('idle')
        elif status == STATUS_IDLEEXC:
            self.setStatus('idle', exception=True)
        elif status != STATUS_INBREAK:
            self.setStatus('running')
        else:
            self.setStatus('interrupted')

    def on_client_disconnected(self):
        self.setStatus('disconnected')

    def on_client_showhelp(self, data):
        if self.helpWindow is None:
            self.helpWindow = HelpWindow(self, self.client)
        self.helpWindow.showHelp(data)

    def on_client_clientexec(self, data):
        # currently used for client-side plot using matplotlib; data is
        # (funcname, args, ...)
        plot_func_path = data[0]
        try:
            modname, funcname = plot_func_path.rsplit('.', 1)
            func = getattr(__import__(modname, None, None, [funcname]),
                           funcname)
            func(*data[1:])
        except Exception:
            self.log.exception('Error during clientexec')

    def on_client_plugplay(self, data):
        if data[0] == 'added':
            setup = data[1]
            if setup in self.pnpWindows:
                self.pnpWindows[setup].activateWindow()
            else:
                window = PnPSetupQuestion(self, data, lambda:
                    self.client.tell('queue', '', 'AddSetup(%r)' % setup))
                self.pnpWindows[setup] = window
                self.connect(window, SIGNAL('closed'), self.on_pnpWindow_closed)
                window.show()

    def on_pnpWindow_closed(self, window):
        self.pnpWindows.pop(window.setup, None)

    def on_client_watchdog(self, data):
        if self.watchdogWindow is None:
            self.watchdogWindow = WatchdogDialog(self)
        self.watchdogWindow.addEvent(data)
        self.watchdogWindow.show()

    def on_trayIcon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.activateWindow()

    def on_actionExpert_toggled(self, on):
        for panel in self.panels:
            panel.setExpertMode(on)
        for window in self.windows.values():
            for panel in window.panels:
                panel.setExpertMode(on)

    @qtsig('')
    def on_actionNicosHelp_triggered(self):
        self.client.eval('session.showHelp("index")')

    @qtsig('')
    def on_actionNicosDocu_triggered(self):
        from nicos.clients.gui.tools.website import WebsiteTool
        # XXX: change URL to current release version
        dlg = WebsiteTool(self,
            url='http://trac.frm2.tum.de/nicos/doc/nicos-master/index.html')
        dlg.setWindowModality(Qt.NonModal)
        dlg.show()

    @qtsig('')
    def on_actionAbout_triggered(self):
        QMessageBox.information(
            self, 'About this application', 'NICOS GUI client version %s, '
            'written by Georg Brandl.\n\nServer: ' % nicos_version
            + (self.client.connected and self.client.version or
               'not connected'))

    @qtsig('')
    def on_actionAboutQt_triggered(self):
        QMessageBox.aboutQt(self)

    @qtsig('bool')
    def on_actionConnect_triggered(self, on):
        # connection or disconnection request?
        if not on:
            self.client.disconnect()
            return

        self.actionConnect.setChecked(False)  # gets set by connection event
        new_name, new_data, passwd, save = ConnectionDialog.getConnectionData(
            self, self.connpresets, self.lastpreset, self.connectionData)
        if new_data is None:
            return
        if save:
            self.lastpreset = save
            self.connpresets[save] = \
                [new_data['host'], new_data['port'], new_data['login']]
        else:
            self.lastpreset = new_name
        self.connectionData.update(new_data)
        self.client.connect(self.connectionData, passwd)
        self.lastpasswd = passwd

    @qtsig('')
    def on_actionPreferences_triggered(self):
        dlg = SettingsDialog(self)
        ret = dlg.exec_()
        if ret == QDialog.Accepted:
            dlg.saveSettings()

    @qtsig('')
    def on_actionFont_triggered(self):
        font, ok = QFontDialog.getFont(self.user_font, self)
        if not ok:
            return
        for panel in self.panels:
            panel.setCustomStyle(font, self.user_color)
        self.user_font = font

    @qtsig('')
    def on_actionColor_triggered(self):
        color = QColorDialog.getColor(self.user_color, self)
        if not color.isValid():
            return
        for panel in self.panels:
            panel.setCustomStyle(self.user_font, color)
        self.user_color = color


log = None

def main(argv):
    global log

    # Import the compiled resource file to register resources
    import nicos.guisupport.gui_rc  #pylint: disable=W0612

    userpath = path.join(os.getenv('HOME'), '.config', 'nicos')

    # Set up logging for the GUI instance.
    initLoggers()
    log = NicosLogger('gui')
    log.parent = None
    log.setLevel(logging.INFO)
    log.addHandler(ColoredConsoleHandler())
    log.addHandler(NicosLogfileHandler(path.join(userpath, 'log'), 'gui',
                                       use_subdir=False))

    # set up logging for unhandled exceptions in Qt callbacks
    def log_unhandled(*exc_info):
        log.exception(exc_info=exc_info)
    sys.excepthook = log_unhandled

    app = QApplication(argv, organizationName='nicos', applicationName='gui')

    # XXX implement proper argument parsing
    configfile = path.join(path.dirname(__file__), 'defconfig.py')
    stylefile = path.join(userpath, 'style.qss')
    if '-c' in argv:
        idx = argv.index('-c')
        configfile = argv[idx+1]
        styleRoot = path.splitext(configfile)[0]
        stylefile = styleRoot + ".qss"
        del argv[idx:idx+2]
    else:
        styleRoot = path.splitext(stylefile)[0]

    with open(configfile, 'rb') as fp:
        configcode = fp.read()
    ns = {}
    exec configcode in ns
    if 'default_profile_config' in ns:
        # backward compatibility
        panel_conf = panel_config(ns['default_profile_config'])
    else:
        panel_conf = panel_config(ns['config'])

    # check whether platform specific style file is present
    stylePlatform = styleRoot + '-' + sys.platform + ".qss"
    if path.isfile(stylePlatform):
        stylefile = stylePlatform

    if path.isfile(stylefile):
        try:
            with open(stylefile, 'r') as fd:
                app.setStyleSheet(fd.read())
        except Exception:
            log.warning('Error setting user style sheet from %s' % stylefile,
                        exc=1)

    mainwindow = MainWindow(log, panel_conf)

    if len(argv) > 1:
        cdata = parseConnectionString(argv[1], DEFAULT_PORT)
        if cdata:
            mainwindow.setConnData(*cdata)
            if len(argv) > 2:
                mainwindow.client.connect(mainwindow.connectionData, argv[2])
    mainwindow.show()

    return app.exec_()
