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
#   Georg Brandl <g.brandl@fz-juelich.de>
#   Artem Feoktystov <a.feoktystov@fz-juelich.de>
#
# *****************************************************************************

"""KWS sample configuration dialog."""

from __future__ import absolute_import, division, print_function

import math
import time

from nicos.clients.gui.panels import Panel
from nicos.clients.gui.utils import dialogFromUi, loadUi
from nicos.guisupport import typedvalue
from nicos.guisupport.qt import QDialog, QDialogButtonBox, QFileDialog, \
    QFrame, QLineEdit, QListWidgetItem, QMenu, QMessageBox, QRadioButton, \
    QTableWidgetItem, QVBoxLayout, pyqtSlot
from nicos.guisupport.utils import DoubleValidator
from nicos.pycompat import builtins, exec_, iteritems
from nicos.utils import findResource

SAMPLE_KEYS = ['aperture', 'position', 'timefactor',
               'thickness', 'detoffset', 'comment']


def configToFrame(frame, config):
    frame.nameBox.setText(config['name'])
    frame.commentBox.setText(config['comment'])
    frame.offsetBox.setText(str(config['detoffset']))
    frame.thickBox.setText(str(config['thickness']))
    frame.factorBox.setText(str(config['timefactor']))
    frame.posTbl.setRowCount(len(config['position']))
    frame.apXBox.setText(str(config['aperture'][0]))
    frame.apYBox.setText(str(config['aperture'][1]))
    frame.apWBox.setText(str(config['aperture'][2]))
    frame.apHBox.setText(str(config['aperture'][3]))
    for i, (devname, position) in enumerate(iteritems(config['position'])):
        frame.posTbl.setItem(i, 0, QTableWidgetItem(devname))
        frame.posTbl.setItem(i, 1, QTableWidgetItem(str(position)))
    frame.posTbl.resizeRowsToContents()
    frame.posTbl.resizeColumnsToContents()


def configFromFrame(frame):
    position = {}
    for i in range(frame.posTbl.rowCount()):
        devname = frame.posTbl.item(i, 0).text()
        devpos = float(frame.posTbl.item(i, 1).text())
        position[devname] = devpos
    return {
        'name': frame.nameBox.text(),
        'comment': frame.commentBox.text(),
        'detoffset': float(frame.offsetBox.text()),
        'thickness': float(frame.thickBox.text()),
        'timefactor': float(frame.factorBox.text()),
        'aperture': (float(frame.apXBox.text()),
                     float(frame.apYBox.text()),
                     float(frame.apWBox.text()),
                     float(frame.apHBox.text())),
        'position': position,
    }


class ConfigEditDialog(QDialog):

    def __init__(self, parent, client, instrument, configs, config=None):
        QDialog.__init__(self, parent)
        self.instrument = instrument
        self.configs = configs
        self.client = client
        self.setWindowTitle('Sample configuration')
        layout = QVBoxLayout()
        self.frm = QFrame(self)
        loadUi(self.frm, findResource('nicos_ess/loki/gui/sampleconf_one.ui'))
        self.frm.addDevBtn.clicked.connect(self.on_addDevBtn_clicked)
        self.frm.delDevBtn.clicked.connect(self.on_delDevBtn_clicked)
        self.frm.readDevsBtn.clicked.connect(self.on_readDevsBtn_clicked)
        self.frm.readApBtn.clicked.connect(self.on_readApBtn_clicked)
        box = QDialogButtonBox(self)
        box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.accepted.connect(self.maybeAccept)
        box.rejected.connect(self.reject)
        layout.addWidget(self.frm)
        layout.addWidget(box)
        self.setLayout(layout)
        for box in [self.frm.offsetBox, self.frm.thickBox, self.frm.factorBox,
                    self.frm.apXBox, self.frm.apYBox, self.frm.apWBox,
                    self.frm.apHBox]:
            box.setValidator(DoubleValidator(self))
        # List of properties that are going to be enabled on place for edit,
        # thus should not be visible here.
        relevant_list = [self.frm.offsetBox, self.frm.apXBox, self.frm.apYBox,
                         self.frm.apWBox, self.frm.apHBox, self.frm.readApBtn]
        for box in relevant_list:
            box.setVisible(False)
        if config is not None:
            configToFrame(self.frm, config)

    def maybeAccept(self):
        if not self.frm.nameBox.text():
            QMessageBox.warning(self, 'Error', 'Please enter a sample name.')
            self.frm.nameBox.setFocus()
            return
        name = self.frm.nameBox.text()
        if name in [config['name'] for config in self.configs]:
            QMessageBox.warning(self, 'Error', 'This sample name is already '
                                'used, please use a different one.')
            self.frm.nameBox.setFocus()
            return
        for box in [self.frm.offsetBox, self.frm.thickBox, self.frm.factorBox,
                    self.frm.apXBox, self.frm.apYBox, self.frm.apWBox,
                    self.frm.apHBox]:
            if not box.text():
                QMessageBox.warning(self, 'Error', 'Please enter valid values '
                                    'for all input fields.')
                return
        for i in range(self.frm.posTbl.rowCount()):
            devname = self.frm.posTbl.item(i, 0).text()
            devpos = self.frm.posTbl.item(i, 1).text()
            if not devname or devname.startswith('<'):
                QMessageBox.warning(self, 'Error', '%r is not a valid device '
                                    'name.' % devname)
                return
            try:
                devpos = float(devpos)
            except ValueError:
                QMessageBox.warning(self, 'Error', '%r is not a valid position'
                                    ' for device %r.' % (devpos, devname))
                return
        self.accept()

    def _addRow(self, name, value):
        rc = self.frm.posTbl.rowCount()
        self.frm.posTbl.setRowCount(rc + 1)
        self.frm.posTbl.setItem(rc, 0, QTableWidgetItem(name))
        self.frm.posTbl.setItem(rc, 1, QTableWidgetItem(value))
        self.frm.posTbl.resizeColumnsToContents()
        self.frm.posTbl.resizeRowsToContents()

    def on_addDevBtn_clicked(self):
        devlist = self.client.getDeviceList(
            'nicos.core.device.Moveable', only_explicit=False)
        # Only get the sample changer related motors
        devlist = [item for item in devlist
                   if item.startswith('sc_') and 'motor' in item]
        dlg = dialogFromUi(self, findResource(
            'nicos_ess/loki/gui/sampleconf_adddev.ui'))
        dlg.widget = None

        def callback(index):
            devname = devlist[index]
            if dlg.widget:
                dlg.widget.deleteLater()
                dlg.valueFrame.layout().takeAt(0)
            dlg.widget = typedvalue.DeviceValueEdit(dlg, dev=devname)
            dlg.widget.setClient(self.client)
            dlg.valueFrame.layout().insertWidget(0, dlg.widget)
        dlg.devBox.currentIndexChanged.connect(callback)
        dlg.devBox.addItems(devlist)
        if not dlg.exec_():
            return
        self._addRow(dlg.devBox.currentText(), str(dlg.widget.getValue()))

    def on_delDevBtn_clicked(self):
        srow = self.frm.posTbl.currentRow()
        if srow < 0:
            return
        self.frm.posTbl.removeRow(srow)

    def _readDev(self, name):
        rv = self.client.eval('%s.format(%s.read())' % (name, name), None)
        if rv is None:
            QMessageBox.warning(self, 'Error', 'Could not read device %s!' %
                                name)
            return '0'
        return rv

    def on_readDevsBtn_clicked(self):
        dlg = dialogFromUi(self, findResource(
            'nicos_ess/loki/gui/sampleconf_readpos.ui'))
        if self.instrument == 'kws1':
            dlg.kws3Box.hide()
        elif self.instrument == 'kws2':
            dlg.kws3Box.hide()
            dlg.hexaBox.hide()
        elif self.instrument == 'kws3':
            dlg.rotBox.hide()
            dlg.transBox.hide()
            dlg.hexaBox.hide()
            dlg.kws3Box.setChecked(True)
        if not dlg.exec_():
            return
        if dlg.rotBox.isChecked():
            self._addRow('sam_rot', self._readDev('sam_rot'))
        if dlg.transBox.isChecked():
            self._addRow('sam_trans_x', self._readDev('sam_trans_x'))
            self._addRow('sam_trans_y', self._readDev('sam_trans_y'))
        if dlg.hexaBox.isChecked():
            for axis in ('dt', 'tx', 'ty', 'tz', 'rx', 'ry', 'rz'):
                self._addRow('hexapod_' + axis,
                             self._readDev('hexapod_' + axis))
        if dlg.kws3Box.isChecked():
            self._addRow('sam_x', self._readDev('sam_x'))
            self._addRow('sam_y', self._readDev('sam_y'))

    def on_readApBtn_clicked(self):
        if self.instrument != 'kws3':
            rv = self.client.eval('ap_sam.read()', None)
        else:
            rv = self.client.eval('sam_ap.read()', None)
        if rv is None:
            QMessageBox.warning(self, 'Error', 'Could not read aperture!')
            return
        self.frm.apXBox.setText('%.2f' % rv[0])
        self.frm.apYBox.setText('%.2f' % rv[1])
        self.frm.apWBox.setText('%.2f' % rv[2])
        self.frm.apHBox.setText('%.2f' % rv[3])


class KWSSamplePanel(Panel):
    panelName = 'KWS sample setup'

    def __init__(self, parent, client, options):
        Panel.__init__(self, parent, client, options)
        loadUi(self, findResource('nicos_ess/loki/gui/sampleconf.ui'))
        self.sampleGroup.setEnabled(False)
        self.frame.setLayout(QVBoxLayout())

        menu = QMenu(self)
        menu.addSeparator()

        menu = QMenu(self)
        menu.addAction(self.actionEmpty)
        menu.addAction(self.actionGenerate)
        self.createBtn.setMenu(menu)

        self.configs = []
        self.dirty = False
        self.filename = None
        self.holder_info = options.get('holder_info', [])
        self.instrument = options.get('instrument', 'kws1')

    @pyqtSlot()
    def on_actionEmpty_triggered(self):
        self.fileGroup.setEnabled(False)
        self.sampleGroup.setEnabled(True)
        self.dirty = True

    @pyqtSlot()
    def on_actionGenerate_triggered(self):
        def read_axes():
            ax1, ax2 = dlg._info[2], dlg._info[4]
            for (ax, box) in [(ax1, dlg.ax1Box), (ax2, dlg.ax2Box)]:
                if not ax:
                    continue
                x = self.client.eval('%s.read()' % ax, None)
                if x is None:
                    QMessageBox.warning(dlg, 'Error',
                                        'Could not read %s.' % ax)
                    return
                box.setText('%.1f' % x)

        def btn_toggled(checked):
            if checked:
                dlg._info = dlg.sender()._info
                ax1, ax2 = dlg._info[2], dlg._info[4]
                for ax, lbl, box, revbox in [
                        (ax1, dlg.ax1Lbl, dlg.ax1Box, dlg.ax1RevBox),
                        (ax2, dlg.ax2Lbl, dlg.ax2Box, None)
                ]:
                    if ax:
                        lbl.setText(ax)
                        lbl.show()
                        box.show()
                        if revbox:
                            revbox.show()
                            revbox.setText('%s starts at far end' % ax)
                    else:
                        lbl.hide()
                        box.hide()
                        if revbox:
                            revbox.hide()

        dlg = dialogFromUi(self, findResource(
            'nicos_ess/loki/gui/sampleconf_gen.ui'))
        dlg.ax1Box.setValidator(DoubleValidator(self))
        dlg.ax2Box.setValidator(DoubleValidator(self))
        dlg.readBtn.clicked.connect(read_axes)
        nrows = int(math.ceil(len(self.holder_info) / 2.0))
        row, col = 0, 0
        for name, info in self.holder_info:
            btn = QRadioButton(name, dlg)
            btn._info = info
            btn.toggled.connect(btn_toggled)
            dlg.optionFrame.layout().addWidget(btn, row, col)
            if (row, col) == (0, 0):
                btn.setChecked(True)
            row += 1
            if row == nrows:
                row = 0
                col += 1
        if not dlg.exec_():
            return
        rows, levels, ax1, dax1, ax2, dax2 = dlg._info
        sax1 = float(dlg.ax1Box.text()) if ax1 else 0
        sax2 = float(dlg.ax2Box.text()) if ax2 else 0
        if dlg.ax1RevBox.isChecked():
            dax1 = -dax1

        n = 0
        for i in range(levels):
            for j in range(rows):
                n += 1
                position = {}
                if ax1:
                    position[ax1] = round(sax1 + j * dax1, 1)
                if ax2:
                    position[ax2] = round(sax2 + i * dax2, 1)
                config = dict(
                    name=str(n),
                    comment='',
                    detoffset=-335.0,
                    thickness=1.0,
                    timefactor=1.0,
                    aperture=(0, 0, 10, 10),
                    position=position,
                )
                self.configs.append(config)
        firstitem = None
        for config in self.configs:
            newitem = QListWidgetItem(config['name'], self.list)
            firstitem = firstitem or newitem
        # select the first item
        self.list.setCurrentItem(firstitem)
        self.on_list_itemClicked(firstitem)

        self.fileGroup.setEnabled(False)
        self.sampleGroup.setEnabled(True)
        self.dirty = True

    @pyqtSlot()
    def on_retrieveBtn_clicked(self):
        sampleconf = self.client.eval('Exp.sample.samples', [])
        sampleconf = sorted(sampleconf.items())
        self.configs = [dict(c[1]) for c in sampleconf if 'thickness' in c[1]]
        # convert readonlydict to normal dict
        for config in self.configs:
            config['position'] = dict(config['position'].items())
        newitem = None
        for config in self.configs:
            newitem = QListWidgetItem(config['name'], self.list)
        # select the last item
        if newitem:
            self.list.setCurrentItem(newitem)
            self.on_list_itemClicked(newitem)

        self.fileGroup.setEnabled(False)
        self.sampleGroup.setEnabled(True)

    @pyqtSlot()
    def on_openFileBtn_clicked(self):
        initialdir = self.client.eval('session.experiment.scriptpath', '')
        fn = QFileDialog.getOpenFileName(self, 'Open sample file', initialdir,
                                         'Sample files (*.py)')[0]
        if not fn:
            return
        try:
            self.configs = parse_sampleconf(fn)
        except Exception as err:
            self.showError('Could not read file: %s\n\n'
                           'Are you sure this is a sample file?' % err)
        else:
            self.fileGroup.setEnabled(False)
            self.sampleGroup.setEnabled(True)
            newitem = None
            for config in self.configs:
                newitem = QListWidgetItem(config['name'], self.list)
            # select the last item
            if newitem:
                self.list.setCurrentItem(newitem)
            self.on_list_itemClicked(newitem)
            self.filename = fn

    def on_buttonBox_clicked(self, button):
        role = self.buttonBox.buttonRole(button)
        if role == QDialogButtonBox.RejectRole:
            return
        do_apply = role == QDialogButtonBox.ApplyRole
        if self.dirty:
            initialdir = self.client.eval('session.experiment.scriptpath', '')
            fn = QFileDialog.getSaveFileName(self, 'Save sample file',
                                             initialdir, 'Sample files (*.py)')[0]
            if not fn:
                return False
            if not fn.endswith('.py'):
                fn += '.py'
            self.filename = fn
        try:
            script = self._generate(self.filename)
        except Exception as err:
            self.showError('Could not write file: %s' % err)
        else:
            if do_apply:
                self.client.run(script, self.filename)
                self.showInfo('Sample info has been transferred to the daemon.')
            self.closeWindow()

    def on_buttonBox_rejected(self):
        self.closeWindow()

    def _clearDisplay(self):
        item = self.frame.layout().takeAt(0)
        if item:
            item.widget().deleteLater()

    def on_list_currentItemChanged(self, item):
        self.on_list_itemClicked(item)

    def on_list_itemClicked(self, item):
        self._clearDisplay()
        index = self.list.row(item)
        frm = QFrame(self)
        loadUi(frm, findResource('nicos_ess/loki/gui/sampleconf_offap.ui'))
        frm.whatLbl.setText('Sample configuration')
        configToFrame(frm, self.configs[index])
        frm.addDevBtn.setVisible(False)
        frm.delDevBtn.setVisible(False)
        frm.readApBtn.setVisible(True)
        frm.readDevsBtn.setVisible(False)
        frm.posTbl.setEnabled(False)
        relevant_list = [frm.offsetBox, frm.apXBox, frm.apYBox, frm.apWBox,
                         frm.apHBox]
        for box in frm.findChildren(QLineEdit):
            if box in relevant_list:
                box.setEnabled(True)
            else:
                box.setEnabled(False)
        layout = self.frame.layout()
        layout.addWidget(frm)

        # Enable users the change the offset and aperture values at will
        # without the need of opening any dialog window.
        frm.offsetBox.returnPressed.connect(lambda: self.set_offset(index,
                                            frm.offsetBox.displayText()))
        frm.apXBox.returnPressed.connect(lambda: self.set_aperture(index,
                                         frm.apXBox.displayText(), 0))
        frm.apYBox.returnPressed.connect(lambda: self.set_aperture(index,
                                         frm.apYBox.displayText(), 1))
        frm.apWBox.returnPressed.connect(lambda: self.set_aperture(index,
                                         frm.apWBox.displayText(), 2))
        frm.apHBox.returnPressed.connect(lambda: self.set_aperture(index,
                                         frm.apHBox.displayText(), 3))

        # Re-validate the values
        for box in [frm.offsetBox, frm.apXBox, frm.apYBox, frm.apWBox,
                    frm.apHBox]:
            box.setValidator(DoubleValidator(self))

    def set_offset(self, i, val):
        self.dirty = True
        self.configs[i]['detoffset'] = val
        item = self.list.item(i)
        self._copy_key('detoffset')
        self.on_list_itemClicked(item)

    def set_aperture(self, i, val, key):
        self.dirty = True
        # The following implementation is required as "aperture" has been
        # implemented as a tuple rather then a simple list.
        x = self.configs[i]['aperture'][0]
        y = self.configs[i]['aperture'][1]
        w = self.configs[i]['aperture'][2]
        h = self.configs[i]['aperture'][3]
        aperture_switch = {
            0: (float(val), y, w, h),
            1: (x, float(val), w, h),
            2: (x, y, float(val), h),
            3: (x, y, w, float(val))
        }
        self.configs[i]['aperture'] = aperture_switch[key]
        item = self.list.item(i)
        self._copy_key('aperture')
        self.on_list_itemClicked(item)

    def on_list_itemDoubleClicked(self):
        self.on_editBtn_clicked()

    @pyqtSlot()
    def on_newBtn_clicked(self):
        dlg = ConfigEditDialog(self, self.client, self.instrument,
                               self.configs)
        if not dlg.exec_():
            return
        self.dirty = True
        config = configFromFrame(dlg.frm)
        dlg.frm.whatLbl.setText('New sample configuration')
        self.configs.append(config)
        newitem = QListWidgetItem(config['name'], self.list)
        self.list.setCurrentItem(newitem)
        self.on_list_itemClicked(newitem)

    @pyqtSlot()
    def on_editBtn_clicked(self):
        index = self.list.currentRow()
        if index < 0:
            return
        dlg = ConfigEditDialog(self, self.client, self.instrument,
                               [config for (i, config) in
                                enumerate(self.configs) if i != index],
                               self.configs[index])
        if not dlg.exec_():
            return
        self.dirty = True
        config = configFromFrame(dlg.frm)
        self.configs[index] = config
        listitem = self.list.item(index)
        listitem.setText(config['name'])
        self.on_list_itemClicked(listitem)

    @pyqtSlot()
    def on_delBtn_clicked(self):
        index = self.list.currentRow()
        if index < 0:
            return
        self.dirty = True
        self.list.takeItem(index)
        del self.configs[index]
        if self.list.currentRow() != -1:
            self.on_list_itemClicked(self.list.item(self.list.currentRow()))
        else:
            self._clearDisplay()

    def _copy_key(self, key):
        index = self.list.currentRow()
        if index < 0:
            return
        self.dirty = True
        template = self.configs[index][key]
        for config in self.configs:
            config[key] = template

    def _generate(self, filename):
        script = ['# KWS sample file for NICOS\n',
                  '# Written: %s\n\n' % time.asctime(),
                  'ClearSamples()\n']
        for (i, config) in enumerate(self.configs, start=1):
            script.append('SetSample(%d, %r, ' % (i, config['name']))
            for key in SAMPLE_KEYS:
                script.append('%s=%r' % (key, config[key]))
                script.append(', ')
            del script[-1]  # remove last comma
            script.append(')\n')
        if filename is not None:
            with open(filename, 'w') as fp:
                fp.writelines(script)
        return ''.join(script)


class MockSample(object):
    def __init__(self):
        self.reset_called = False
        self.configs = []

    def reset(self):
        self.reset_called = True
        self.configs = []

    def define(self, _num, name, **entry):
        entry['name'] = name
        for key in SAMPLE_KEYS:
            if key not in entry:
                raise ValueError('missing key %r in sample entry' % key)
        self.configs.append(entry)


def parse_sampleconf(filename):
    builtin_ns = vars(builtins).copy()
    for name in ('__import__', 'open', 'exec', 'execfile'):
        builtin_ns.pop(name, None)
    mocksample = MockSample()
    ns = {'__builtins__': builtin_ns,
          'ClearSamples': mocksample.reset,
          'SetSample': mocksample.define}
    with open(filename, 'r') as fp:
        exec_(fp, ns)
    # The script needs to call this, if it doesn't it is not a sample file.
    if not mocksample.reset_called:
        raise ValueError('the script never calls ClearSamples()')
    return mocksample.configs
