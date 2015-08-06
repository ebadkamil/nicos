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
#
# *****************************************************************************

"""NICOS GUI experiment setup window."""

from PyQt4.QtGui import QDialogButtonBox, QListWidgetItem, QMessageBox, \
    QFrame, QHBoxLayout, QLabel, QComboBox
from PyQt4.QtCore import SIGNAL, Qt, pyqtSignature as qtsig

from nicos.utils import decodeAny
from nicos.guisupport.widget import NicosWidget
from nicos.clients.gui.panels import Panel
from nicos.clients.gui.utils import loadUi, DlgUtils
from nicos.pycompat import iteritems
from nicos.core.params import mailaddress
from nicos.core import ConfigurationError


def iterChecked(listwidget):
    """Yield checked items in a QListWidget"""
    for i in range(listwidget.count()):
        item = listwidget.item(i)
        if item.checkState() == Qt.Checked:
            yield item


class ExpPanel(Panel, DlgUtils):
    panelName = 'Experiment setup'

    def __init__(self, parent, client):
        Panel.__init__(self, parent, client)
        DlgUtils.__init__(self, 'Setup')
        loadUi(self, 'setup_exp.ui', 'panels')
        self.propdbInfo.setVisible(False)
        self._orig_proposal = None

        if self.client.connected:
            self.on_client_connected()
        self.connect(self.client, SIGNAL('connected'), self.on_client_connected)
        self.connect(self.client, SIGNAL('experiment'), self.on_client_experiment)

    def _update_proposal_info(self):
        values = self.client.eval('session.experiment.proposal, '
                                  'session.experiment.title, '
                                  'session.experiment.users, '
                                  'session.experiment.localcontact, '
                                  'session.experiment.sample.samplename', None)
        if values:
            self._orig_proposal_info = values
            self.proposalNum.setText(values[0])
            self.expTitle.setText(decodeAny(values[1]))
            self.users.setText(decodeAny(values[2]))
            self.localContact.setText(decodeAny(values[3]))
            self.sampleName.setText(decodeAny(values[4]))
        emails = self.client.eval('[e.receivers for e in session.notifiers '
            'if "nicos.devices.notifiers.Mailer" in e.classes]', [])
        self._orig_email = sum(emails, [])
        self.notifEmails.setPlainText(decodeAny('\n'.join(self._orig_email)))

    def on_client_connected(self):
        # fill proposal
        self._update_proposal_info()
        # check for new or finish
        if self.client.eval('session.experiment.mustFinish', False):
            self.finishBox.setVisible(True)
            self.newBox.setVisible(False)
        else:
            self.finishBox.setVisible(False)
            self.newBox.setVisible(True)
            self.proposalNum.setText('')  # do not offer "service"
        # check for capability to ask proposal database
        if self.client.eval('getattr(session.experiment, "propdb", "")', None):
            self.propdbInfo.setVisible(True)
            self.queryDBButton.setVisible(True)
        else:
            self.queryDBButton.setVisible(False)

    def on_client_experiment(self, data):
        # just reinitialize
        self.on_client_connected()

    def _getProposalInput(self):
        prop = self.proposalNum.text()
        title = self.expTitle.text().encode('utf-8')
        users = self.users.text().encode('utf-8')
        try:
            local = mailaddress(self.localContact.text().encode('utf-8'))
        except ValueError:
            QMessageBox.critical(self, 'Error', 'The local contact entry is not'
                                 ' a valid email address')
            raise ConfigurationError('')
        emails = self.notifEmails.toPlainText().encode('utf-8').split(b'\n')
        return prop, title, users, local, emails

    @qtsig('')
    def on_finishButton_clicked(self):
        self.client.run('FinishExperiment()')

    @qtsig('')
    def on_queryDBButton_clicked(self):
        try:
            prop, title, users, _, emails = self._getProposalInput()
        except ConfigurationError:
            return
        sample = self.sampleName.text().encode('utf-8')

        # read all values from propdb
        try:
            result = self.client.eval('session.experiment._fillProposal(%s, {})'
                                      % prop, None)

            if result:
                if result['wrong_instrument']:
                    self.showError('Proposal is not for this instrument, '
                                   'please check the proposal number!')
                # now transfer it into gui
                # XXX check: is the result bytes or str on Python 3?
                self.expTitle.setText(decodeAny(result.get('title', title)))
                self.users.setText(decodeAny(result.get('user', users)))
                # XXX: local contact must be email, but proposal db returns
                # only a name
                # self.localContact.setText(decodeAny(result.get('localcontact',
                #                                                local)))
                self.sampleName.setText(decodeAny(result.get('sample', sample)))
                self.notifEmails.setPlainText(
                    decodeAny(result.get('user_email', emails)))
                # check permissions:
                failed = []
                if result.get('permission_security', 'no') != 'yes':
                    failed.append('* Security (Tel. 12699)')
                if result.get('permission_radiation_protection', 'no') != 'yes':
                    failed.append('* Radiation protection (Tel. 14955)')
                if failed and not result['wrong_instrument']:
                    self.showError('Proposal lacks sufficient permissions '
                                   'to be performed!\n\n' + '\n'.join(failed))
            else:
                self.showInfo('Reading proposaldb failed for an unknown reason.'
                              ' Please check logfiles for hints.')
        except Exception as e:
            self.log.warning(e, exc=1)
            self.showInfo('Reading proposaldb failed for an unknown reason. '
                          'Please check logfiles....\n' + repr(e))

    def on_buttonBox_clicked(self, button):
        if self.buttonBox.buttonRole(button) == QDialogButtonBox.ApplyRole:
            self.applyChanges()
        else:
            # Only the next interesting widget title isn't empty
            parent = self.parentWidget()
            while not parent.windowTitle():
                parent = parent.parentWidget()
            parent.close()

    def applyChanges(self):
        done = []

        # proposal settings
        try:
            prop, title, users, local, email = self._getProposalInput()
        except ConfigurationError:
            return
        email = [_f for _f in email if _f]  # remove empty lines

        # check conditions
        if self.client.eval('session.experiment.serviceexp', True) and \
            self.client.eval('session.experiment.proptype', 'user') == 'user' and \
            self.client.eval('session.experiment.proposal', '') != prop:
            self.showError('Can not directly switch experiments, please use '
                           'FinishExperiment first!')
            return

        # do some work
        if prop != self._orig_proposal_info[0]:
            args = {'proposal': prop}
            if local:
                args['localcontact'] = local
            if title:
                args['title'] = title
            if users:
                args['user'] = users
            code = 'NewExperiment(%s)' % ', '.join('%s=%r' % i
                                                   for i in args.items())
            self.client.run(code)
            done.append('New experiment started.')
        else:
            if title != self._orig_proposal_info[1]:
                self.client.run('Exp.title = %r' % title)
                done.append('New experiment title set.')
            if users != self._orig_proposal_info[2]:
                self.client.run('Exp.users = %r' % users)
                done.append('New users set.')
            if local != self._orig_proposal_info[3]:
                self.client.run('Exp.localcontact = %r' % local)
                done.append('New local contact set.')
        sample = self.sampleName.text().encode('utf-8')
        if sample != self._orig_proposal_info[4]:
            self.client.run('NewSample(%r)' % sample)
            done.append('New sample name set.')
        if email != self._orig_email:
            self.client.run('SetMailReceivers(%s)' % ', '.join(map(repr, email)))
            done.append('New mail receivers set.')

        # tell user about everything we did
        if done:
            self.showInfo('\n'.join(done))
        self._update_proposal_info()


class AliasWidget(QFrame):
    def __init__(self, parent, name, selections):
        QFrame.__init__(self, parent)
        self.name = name
        self.selections = selections
        layout = QHBoxLayout()
        layout.addWidget(QLabel(name, self))
        self.combo = QComboBox(self)
        self.combo.addItems(selections)
        self.combo.setCurrentIndex(0)
        layout.addWidget(self.combo)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def setSelections(self, selections):
        if selections != self.selections:
            self.selections = selections
            self.combo.clear()
            self.combo.addItems(selections)
            self.combo.setCurrentIndex(0)

    def getSelection(self):
        return self.combo.currentText()


class SetupsPanel(Panel, DlgUtils):
    panelName = 'Setup selection'

    def __init__(self, parent, client):
        Panel.__init__(self, parent, client)
        DlgUtils.__init__(self, 'Setup')
        loadUi(self, 'setup_setups.ui', 'panels')

        self.aliasGroup.hide()
        self._aliasWidgets = {}

        self._setupinfo = {}
        self._loaded = set()
        self._loaded_basic = None

        self.buttonBox.addButton('Reload current setup',
                                 QDialogButtonBox.ResetRole)
        if self.client.connected:
            self.on_client_connected()
        self.connect(self.client, SIGNAL('connected'), self.on_client_connected)
        self.connect(self.client, SIGNAL('setup'), self.on_client_setup)

    def on_client_connected(self):
        # fill setups
        self._setupinfo = self.client.eval('session.readSetupInfo()', {})
        all_loaded = self.client.eval('session.loaded_setups', set())
        self._loaded = set()
        self._loaded_basic = None
        self.basicSetup.clear()
        self.optSetups.clear()
        default_flags = Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | \
            Qt.ItemIsEnabled
        keep = QListWidgetItem('<keep current>', self.basicSetup)
        if self._setupinfo is not None:
            for name, info in sorted(self._setupinfo.items()):
                if info is None:
                    continue
                if info['group'] == 'basic':
                    QListWidgetItem(name, self.basicSetup)
                    if name in all_loaded:
                        self._loaded_basic = name
                        self._loaded.add(name)
                elif info['group'] == 'optional':
                    item = QListWidgetItem(name, self.optSetups)
                    item.setFlags(default_flags)
                    item.setData(Qt.UserRole, 0)
                    if name in all_loaded:
                        self._loaded.add(name)
                    item.setCheckState(Qt.Checked if name in all_loaded
                                       else Qt.Unchecked)
                elif info['group'] == 'plugplay':
                    item = QListWidgetItem(name, self.optSetups)
                    item.setFlags(default_flags)
                    item.setData(Qt.UserRole, 1)
                    if name in all_loaded:
                        self._loaded.add(name)
                    elif not self.showPnpBox.isChecked():
                        item.setHidden(True)
                    item.setCheckState(Qt.Checked if name in all_loaded
                                       else Qt.Unchecked)
        self.basicSetup.setCurrentItem(keep)

    def on_client_setup(self, data):
        self.on_client_connected()

    def on_basicSetup_currentItemChanged(self, item, old):
        if item and item.text() != '<keep current>':
            self.showSetupInfo(item.text())
        self.updateAliasList()

    def on_basicSetup_itemClicked(self, item):
        if item.text() != '<keep current>':
            self.showSetupInfo(item.text())
        self.updateAliasList()

    def on_optSetups_currentItemChanged(self, item, old):
        if item:
            self.showSetupInfo(item.text())

    def on_optSetups_itemClicked(self, item):
        self.showSetupInfo(item.text())
        self.updateAliasList()

    def on_showPnpBox_stateChanged(self, state):
        for i in range(self.optSetups.count()):
            item = self.optSetups.item(i)
            if item.data(Qt.UserRole) == 1:
                item.setHidden(item.checkState() == Qt.Unchecked and
                               not self.showPnpBox.isChecked())

    def on_buttonBox_clicked(self, button):
        if self.buttonBox.buttonRole(button) == QDialogButtonBox.ResetRole:
            self.client.run('NewSetup()')
            self.showInfo('Current setups reloaded.')
            # fall through to the close case
        if self.buttonBox.buttonRole(button) == QDialogButtonBox.ApplyRole:
            self.applyChanges()
        # Only the next interesting widget title isn't empty
        parent = self.parentWidget()
        while not parent.windowTitle():
            parent = parent.parentWidget()
        parent.close()

    def showSetupInfo(self, setup):
        info = self._setupinfo[str(setup)]
        devs = []
        for devname, devconfig in iteritems(info['devices']):
            if not devconfig[1].get('lowlevel'):
                devs.append(devname)
        devs = ', '.join(sorted(devs))
        self.setupDescription.setText(
            '<b>%s</b><br/>%s<br/><br/>'
            'Devices: %s<br/>' % (setup, info['description'], devs))

    def _calculateSetups(self):
        cur = self.basicSetup.currentItem()
        if cur:
            basic = cur.text()
        else:
            basic = '<keep current>'
        # calculate the new setups
        setups = set()
        new_basic = False
        if basic == '<keep current>':
            if self._loaded_basic:
                setups.add(self._loaded_basic)
        else:
            setups.add(basic)
            new_basic = True
        for item in iterChecked(self.optSetups):
            setups.add(item.text())
        return setups, new_basic

    def updateAliasList(self):
        setups, _ = self._calculateSetups()
        # get includes as well
        seen = set()
        def add_includes(s):
            if s in seen or s not in self._setupinfo:
                return
            seen.add(s)
            for inc in self._setupinfo[s]['includes']:
                add_includes(inc)
                setups.add(inc)
        for setup in setups.copy():
            add_includes(setup)
        # now collect alias config
        alias_config = {}
        for setup in setups:
            aliasconfig = self._setupinfo[setup]['alias_config']
            for (aliasname, target, prio) in aliasconfig:
                alias_config.setdefault(aliasname, []).append((target, prio))
        # sort by priority
        for aliasname in alias_config:
            alias_config[aliasname].sort(key=lambda x: -x[1])
        # create/update widgets
        layout = self.aliasGroup.layout()
        for aliasname in sorted(alias_config):
            selections = [x[0] for x in alias_config[aliasname]]
            if aliasname in self._aliasWidgets:
                self._aliasWidgets[aliasname].setSelections(selections)
            else:
                wid = self._aliasWidgets[aliasname] = AliasWidget(self, aliasname,
                                                                  selections)
                layout.addWidget(wid)
        for name, wid in self._aliasWidgets.items():
            if name not in alias_config:
                layout.takeAt(layout.indexOf(wid)).widget().deleteLater()
                del self._aliasWidgets[name]
        if alias_config:
            self.aliasGroup.show()
        else:
            self.aliasGroup.hide()

    def applyChanges(self):
        cmd = 'NewSetup'
        setups, new_basic = self._calculateSetups()

        to_add = setups - self._loaded
        to_remove = self._loaded - setups
        # new setups only and no basic setup change?
        if to_add and not to_remove and not new_basic:
            cmd = 'AddSetup'
            setups = to_add
        else:
            cmd = 'NewSetup'
        if setups:
            self.client.run('%s(%s)' % (cmd, ', '.join(map(repr, setups))))
        for name, wid in self._aliasWidgets.items():
            self.client.run('%s.alias = %s' % (name, wid.getSelection()))
        if setups or self._aliasWidgets:
            self.showInfo('New setups loaded.')


class DetEnvPanel(Panel, DlgUtils):
    panelName = 'Det/Env setup'

    def __init__(self, parent, client):
        Panel.__init__(self, parent, client)
        DlgUtils.__init__(self, 'Setup')
        loadUi(self, 'setup_detenv.ui', 'panels')

        if self.client.connected:
            self.on_client_connected()
        self.connect(self.client, SIGNAL('connected'), self.on_client_connected)

    def on_client_connected(self):
        default_flags = Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | \
            Qt.ItemIsEnabled

        # fill detectors
        detectors = self.client.getDeviceList('nicos.core.device.Measurable')
        self._orig_detlist = self.client.eval('session.experiment.detlist', [])
        for detname in detectors:
            item = QListWidgetItem(detname, self.detectors)
            item.setFlags(default_flags)
            item.setCheckState(Qt.Checked if detname in self._orig_detlist
                               else Qt.Unchecked)

        # fill environment
        envdevs = self.client.getDeviceList(
            'nicos.core.device.Readable',
            exclude_class='nicos.core.device.Measurable')
        self._orig_envlist = self.client.eval('session.experiment.envlist', [])
        for devname in envdevs:
            item = QListWidgetItem(devname, self.sampleenv)
            item.setFlags(default_flags)
            item.setCheckState(Qt.Checked if devname in self._orig_envlist
                               else Qt.Unchecked)

    def on_buttonBox_clicked(self, button):
        if self.buttonBox.buttonRole(button) == QDialogButtonBox.ApplyRole:
            self.applyChanges()
        else:
            # Only the next interesting widget title isn't empty
            parent = self.parentWidget()
            while not parent.windowTitle():
                parent = parent.parentWidget()
            parent.close()

    def applyChanges(self):
        done = []

        # detectors
        new_detlist = [item.text() for item in iterChecked(self.detectors)]
        if set(new_detlist) != set(self._orig_detlist):
            self.client.run('SetDetectors(%s)' % ', '.join(new_detlist))
            done.append('New standard detectors applied.')
            self._orig_detlist = new_detlist

        # sample env
        new_envlist = [item.text() for item in iterChecked(self.sampleenv)]
        if set(new_envlist) != set(self._orig_envlist):
            self.client.run('SetEnvironment(%s)' % ', '.join(new_envlist))
            done.append('New standard environment devices applied.')
            self._orig_envlist = new_envlist

        if done:
            self.showInfo('\n'.join(done))


class GenericSamplePanel(Panel, DlgUtils):
    panelName = 'Sample setup'
    uiName = 'setup_sample.ui'

    def __init__(self, parent, client):
        Panel.__init__(self, parent, client)
        DlgUtils.__init__(self, 'Setup')
        loadUi(self, self.uiName, 'panels')
        for ch in self.findChildren(NicosWidget):
            ch.setClient(self.client)

    def on_buttonBox_clicked(self, button):
        if self.buttonBox.buttonRole(button) == QDialogButtonBox.ApplyRole:
            self.applyChanges()
        else:
            # Only the next interesting widget title isn't empty
            parent = self.parentWidget()
            while not parent.windowTitle():
                parent = parent.parentWidget()
            parent.close()

    def getEditBoxes(self):
        return [self.samplenameEdit]

    def applyChanges(self):
        code = ''
        for edit in self.getEditBoxes():
            if edit.param == 'samplename':
                code += 'NewSample(%r)\n' % edit.getValue()
            else:
                code += 'Sample.%s = %r\n' % (edit.param, edit.getValue())

        self.client.run(code.rstrip())
        self.showInfo('Sample parameters changed.')


class TasSamplePanel(GenericSamplePanel):
    panelName = 'TAS sample setup'
    uiName = 'setup_tassample.ui'

    def getEditBoxes(self):
        return [self.samplenameEdit, self.latticeEdit, self.anglesEdit,
                self.orient1Edit, self.orient2Edit, self.psi0Edit,
                self.spacegroupEdit, self.mosaicEdit]
