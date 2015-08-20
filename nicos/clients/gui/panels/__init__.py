#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2015 by the NICOS contributors (see AUTHORS)
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

"""Support for "auxiliary" windows containing panels."""

from time import time as currenttime

from PyQt4.QtGui import QWidget, QMainWindow, QSplitter, QFontDialog, \
    QColorDialog, QHBoxLayout, QVBoxLayout, QDockWidget, QDialog, QPalette, \
    QTabWidget
from PyQt4.QtCore import Qt, SIGNAL, pyqtSignature as qtsig, pyqtSignal

from nicos.clients.gui.panels.tabwidget import TearOffTabWidget

from nicos.utils import importString
from nicos.utils.loggers import NicosLogger
from nicos.clients.gui.utils import DlgUtils, SettingGroup, loadUi, \
    loadBasicWindowSettings, loadUserStyle
from nicos.clients.gui.config import hsplit, vsplit, tabbed, panel, docked
from nicos.guisupport.utils import checkSetupSpec


class AuxiliaryWindow(QMainWindow):

    def __init__(self, parent, wintype, config):
        QMainWindow.__init__(self, parent)
        loadUi(self, 'auxwindow.ui')
        self.mainwindow = parent
        self.client = parent.client

        self.type = wintype
        self.panels = []
        self.splitters = []

        self.sgroup = SettingGroup(config.name)
        with self.sgroup as settings:
            loadUserStyle(self, settings)

        self.setWindowTitle(config.name)
        widget = createWindowItem(config.contents, self, self, self)
        self.centralLayout.addWidget(widget)
        self.centralLayout.setContentsMargins(6, 6, 6, 6)

        with self.sgroup as settings:
            loadBasicWindowSettings(self, settings)

        if len(self.splitstate) == len(self.splitters):
            for sp, st in zip(self.splitters, self.splitstate):
                sp.restoreState(st)

    def getPanel(self, panelName):
        for panelobj in self.panels:
            if panelobj.panelName == panelName:
                return panelobj

    def saveWindowLayout(self):
        with self.sgroup as settings:
            settings.setValue('geometry', self.saveGeometry())
            settings.setValue('windowstate', self.saveState())
            settings.setValue('splitstate',
                              [sp.saveState() for sp in self.splitters])
            settings.setValue('font', self.user_font)
            settings.setValue('color', self.user_color)

    def closeEvent(self, event):
        for pnl in self.panels:
            if not pnl.requestClose():
                event.ignore()
                return
        if self.mainwindow.autosavelayout:
            self.saveWindowLayout()
        for pnl in self.panels:
            with pnl.sgroup as settings:
                pnl.saveSettings(settings)
        event.accept()
        self.emit(SIGNAL('closed'), self)
        del self.panels[:]  # this is necessary to get the Qt objects destroyed

    @qtsig('')
    def on_actionFont_triggered(self):
        font, ok = QFontDialog.getFont(self.user_font, self)
        if not ok:
            return
        for pnl in self.panels:
            pnl.setCustomStyle(font, self.user_color)
        self.user_font = font

    @qtsig('')
    def on_actionColor_triggered(self):
        color = QColorDialog.getColor(self.user_color, self)
        if not color.isValid():
            return
        for pnl in self.panels:
            pnl.setCustomStyle(self.user_font, color)
        self.user_color = color


class PanelDialog(QDialog):
    def __init__(self, parent, client, panelcfg, title):
        self.panels = []
        QDialog.__init__(self, parent)
        self.mainwindow = parent.mainwindow
        self.client = client
        self.user_color = self.palette().color(QPalette.Base)
        self.user_font = self.font()
        if isinstance(panelcfg, type) and issubclass(panelcfg, Panel):
            panelcfg = panel('%s.%s' % (panelcfg.__module__,
                                        panelcfg.__name__))
        elif isinstance(panelcfg, str):
            panelcfg = panel(panelcfg)
        pnl = createWindowItem(panelcfg, self, self, self.mainwindow)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(pnl)
        self.setLayout(hbox)
        self.setWindowTitle(title)

        if self.client._reg_keys:
            values = self.client.ask('getcachekeys',
                                     ','.join(self.client._reg_keys))
            if values is not None:
                for key, value in values:
                    if key in self.client._reg_keys and \
                       key == 'session/mastersetup':
                        for widget in self.client._reg_keys[key]:
                            if widget():
                                widget().on_keyChange(key, value,
                                                      currenttime(), False)


class AuxiliarySubWindow(QMainWindow):
    def __init__(self, parent):
        QMainWindow.__init__(self, parent)
        self.mainwindow = parent

        self.panels = []

    def getPanel(self, panelName):
        for panelobj in self.panels:
            if panelobj.panelName == panelName:
                return panelobj


class Panel(QWidget, DlgUtils):
    panelName = ''
    setupSpec = ()

    setWidgetVisible = pyqtSignal(QWidget, bool, name='setWidgetVisible')

    def __init__(self, parent, client):
        QWidget.__init__(self, parent)
        DlgUtils.__init__(self, self.panelName)
        self.parentwindow = parent
        self.client = client
        self.mainwindow = parent.mainwindow
        self.actions = set()
        self.log = NicosLogger(self.panelName)
        self.log.parent = self.mainwindow.log
        self.sgroup = SettingGroup(self.panelName)
        with self.sgroup as settings:
            self.loadSettings(settings)

    def postInit(self):
        """This method can be implemented to perform actions after all panels
        has been instantiated. It will be automatically called after all panels
        has been created. This can be useful e.g. for accessing other panels
        using their unique ``panelName``.

        """

    def setOptions(self, options):
        setups = options.get('setups', ())
        if isinstance(setups, str):
            setups = (setups,)
        self.setSetups(list(setups))

    def setSetups(self, setupSpec):
        self.setupSpec = setupSpec
        self.log.info('Setups are : %r' % self.setupSpec)

    def setExpertMode(self, expert):
        pass

    def loadSettings(self, settings):
        pass

    def saveSettings(self, settings):
        pass

    def setCustomStyle(self, font, back):
        pass

    def getToolbars(self):
        return []

    def getMenus(self):
        return []

    def hideTitle(self):
        """Called when the panel is shown in a dock or tab widget, which
        provides its own place for the panel title.

        If the panel has a title widget, it should hide it in this method.
        """
        pass

    def requestClose(self):
        return True

    def updateStatus(self, status, exception=False):
        pass

    def on_keyChange(self, key, value, time, expired):
        if key == 'session/mastersetup' and self.setupSpec:
            enabled = checkSetupSpec(self.setupSpec, value, log=self.log)
            self.setWidgetVisible.emit(self, enabled)


def createPanel(item, window, menuwindow, topwindow):
    prefixes = ('nicos.clients.gui.panels.',)
    cls = importString(item.clsname, prefixes=prefixes)
    p = cls(menuwindow, window.client)
    p.setOptions(item.options)
    window.panels.append(p)
    window.client.register(p, 'session/mastersetup')
    if p not in topwindow.panels:
        topwindow.panels.append(p)

    for toolbar in p.getToolbars():
        # this helps for serializing window state
        toolbar.setObjectName(toolbar.windowTitle())
        if hasattr(menuwindow, 'toolBarWindows'):
            menuwindow.insertToolBar(menuwindow.toolBarWindows, toolbar)
        else:
            menuwindow.addToolBar(toolbar)
    for menu in p.getMenus():
        if hasattr(menuwindow, 'menuWindows'):
            p.actions.update((menuwindow.menuBar().insertMenu(
                              menuwindow.menuWindows.menuAction(),
                              menu),))
        else:
            p.actions.update((menuwindow.menuBar().addMenu(menu),))

    p.setCustomStyle(window.user_font, window.user_color)
    return p


def createVerticalSplitter(item, window, menuwindow, topwindow):
    sp = QSplitter(Qt.Vertical)
    window.splitters.append(sp)
    for subitem in item:
        sub = createWindowItem(subitem, window, menuwindow, topwindow)
        sp.addWidget(sub)
    return sp


def createHorizontalSplitter(item, window, menuwindow, topwindow):
    sp = QSplitter(Qt.Horizontal)
    window.splitters.append(sp)
    for subitem in item:
        sub = createWindowItem(subitem, window, menuwindow, topwindow)
        sp.addWidget(sub)
    return sp


def createDockedWidget(item, window, menuwindow, topwindow):
    dockPosMap = {'left':   Qt.LeftDockWidgetArea,
                  'right':  Qt.RightDockWidgetArea,
                  'top':    Qt.TopDockWidgetArea,
                  'bottom': Qt.BottomDockWidgetArea}

    mainitem, dockitems = item
    main = createWindowItem(mainitem, window, menuwindow, topwindow)
    for title, item in dockitems:
        dw = QDockWidget(title, window)
        # prevent closing the dock widget
        dw.setFeatures(QDockWidget.DockWidgetMovable |
                       QDockWidget.DockWidgetFloatable)
        # make the dock title bold
        dw.setStyleSheet('QDockWidget { font-weight: bold; }')
        dw.setObjectName(title)
        sub = createWindowItem(item, window, menuwindow, topwindow)
        if isinstance(sub, Panel):
            sub.hideTitle()
        dw.setWidget(sub)
        dw.setContentsMargins(6, 6, 6, 6)
        dockPos = item.options.get('dockpos', 'left')
        if dockPos not in dockPosMap:
            menuwindow.log.warn('Illegal dockpos specification %s for panel %r'
                                % (dockPos, title))
            dockPos = 'left'
        menuwindow.addDockWidget(dockPosMap[dockPos], dw)
    return main


def createTabWidget(item, window, menuwindow, topwindow):
    tw = TearOffTabWidget(menuwindow)
    tw.setStyleSheet('QTabWidget:tab:disabled{width:0;height:0;margin:0;'
                     'padding:0;border:none}')
    # don't draw a frame around the tab contents
    tw.setDocumentMode(True)
    for entry in item:
        subwindow = AuxiliarySubWindow(tw)
        subwindow.mainwindow = window.mainwindow
        subwindow.user_color = window.user_color
        # we have to nest one step to get consistent layout spacing
        # around the central widget
        central = QWidget(subwindow)
        layout = QVBoxLayout()
        # only keep margin at the top (below the tabs)
        layout.setContentsMargins(0, 6, 0, 0)
        if len(entry) == 2:
            (title, subitem, setupSpec) = entry + (None,)
        else:
            (title, subitem, setupSpec) = entry
        it = createWindowItem(subitem, window, menuwindow, subwindow)
        if isinstance(it, Panel):
            it.hideTitle()
            # if tab has its own setups overwrite panels setups
            if setupSpec:
                it.setSetups(setupSpec)
            it.setWidgetVisible.connect(tw.setWidgetVisible)
        layout.addWidget(it)
        central.setLayout(layout)
        subwindow.setCentralWidget(central)
        tw.addTab(subwindow, title)
    return tw


def createWindowItem(item, window, menuwindow, topwindow):

    if isinstance(item, panel):
        return createPanel(item, window, menuwindow, topwindow)
    elif isinstance(item, hsplit):
        return createHorizontalSplitter(item, window, menuwindow, topwindow)
    elif isinstance(item, vsplit):
        return createVerticalSplitter(item, window, menuwindow, topwindow)
    elif isinstance(item, tabbed):
        return createTabWidget(item, window, menuwindow, topwindow)
    elif isinstance(item, docked):
        return createDockedWidget(item, window, menuwindow, topwindow)


def showPanel(panel):
    """Ensure that the given panel is visible in its window."""
    widget = panel
    parents = []
    while 1:
        parent = widget.parent()
        if parent is None:
            # reached toplevel!
            break
        elif isinstance(parent, QTabWidget):
            # tab widget: select tab (it is wrapped in a QStackedWidget)
            index = parent.indexOf(parents[-2])
            parent.setCurrentIndex(index)
        elif isinstance(parent, QSplitter):
            # splitter: make sure the widget is not collapsed
            index = parent.indexOf(widget)
            sizes = parent.sizes()
            if sizes[index] == 0:
                sizes[index] = sum(sizes)
                parent.setSizes(sizes)
        parents.append(parent)
        widget = parent
    panel.activateWindow()


def findTab(tab, w):
    widget = w
    while True:
        parent = widget.parent()
        if not parent:
            return False
        widget = parent
        if isinstance(widget, AuxiliarySubWindow) and tab == widget:
            return True
    return False


def findTabIndex(tabwidget, w):
    for i in range(len(tabwidget)):
        if findTab(tabwidget.widget(i), w):
            return i
    return None
