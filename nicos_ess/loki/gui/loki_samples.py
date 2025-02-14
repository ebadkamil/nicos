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
#
#  AÜC Hardal <ümit.hardal@ess.eu>
#
# *****************************************************************************

"""LoKI Samples Panel."""

from nicos.clients.gui.utils import loadUi
from nicos.utils import findResource
from nicos_ess.loki.gui.loki_data_model import LokiDataModel
from nicos_ess.loki.gui.loki_panel import LokiPanelBase
from nicos.guisupport.qt import QHeaderView, QTableView, QDialog, \
    QStandardItemModel, QStandardItem, Qt

TABLE_QSS = 'alternate-background-color: aliceblue;'


class UserSampleDataDialog(QDialog):

    def __init__(self, parent, client):
        QDialog.__init__(self, parent)
        self.client = client
        loadUi(self, findResource('nicos_ess/loki/gui/'
                                  'ui_files/'
                                  'loki_create_sample_data.ui'))


class OptionalSampleDataDialog(QDialog):

    def __init__(self, parent, client, optional_data, checked):
        QDialog.__init__(self, parent)
        self.client = client
        loadUi(self, findResource('nicos_ess/loki/gui/'
                                  'ui_files/'
                                  'loki_samples_optional_data.ui'))

        self.model = QStandardItemModel()
        self.items_checked = checked

        self.set_list_view(optional_data)

        self.dialogButtonBox.rejected.connect(self.reject)

    def set_list_view(self, optional_data):
        for data in optional_data:
            item = QStandardItem(data)
            item.setCheckable(True)
            item.setEditable(False)
            # Make sure already checked items stays checked upon re-loading
            # the dialog.
            if item.text() in self.items_checked:
                item.setCheckState(Qt.Checked)
            self.model.appendRow(item)
        self.listView.setModel(self.model)

    def clear_list(self):
        self.model.removeRows(0, self.model.rowCount())


class LokiSamplePanel(LokiPanelBase):
    def __init__(self, parent, client, options):
        LokiPanelBase.__init__(self, parent, client, options)
        loadUi(self,
               findResource('nicos_ess/loki/gui/ui_files/loki_samples.ui')
               )
        self.window = parent
        self.initialise_connection_status_listeners()

        self.permanent_columns = {
            'sample_name': 'Sample Name',
            'chemical_formula': 'Chemical Formula',
            'concentration': 'Concentration'
        }

        self.optional_columns = {
            'background': 'Background',
            'comments': 'Comments',
        }

        self.columns_in_order = list(self.permanent_columns.keys())
        self.addOptionalDataButton.clicked.connect(
            self._activate_optional_data_selection
        )

        self.headers = [
            self.permanent_columns[name]
            for name in self.columns_in_order
        ]

        self.checked_items = []
        self.new_column_added = False

        self._init_table_panel()

    def setViewOnly(self, viewonly):
        self.addOptionalDataButton.setEnabled(not viewonly)
        self.samplesTableView.setEnabled(not viewonly)

    def _init_table_panel(self):
        self.model = LokiDataModel(self.headers)
        self.samplesTableView.setModel(self.model)
        self._init_tableview_markups()

    def _init_tableview_markups(self):
        self.samplesTableView.setSelectionMode(QTableView.ContiguousSelection)
        self.samplesTableView.horizontalHeader().setStretchLastSection(True)
        self.samplesTableView.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.samplesTableView.resizeColumnsToContents()
        self.samplesTableView.setAlternatingRowColors(True)
        self.samplesTableView.setStyleSheet(TABLE_QSS)

    def _activate_optional_data_selection(self):
        optional_data_dialog = OptionalSampleDataDialog(
            self, self.client, self.optional_columns.values(),
            self.checked_items
        )

        optional_data_dialog.createDataButton.clicked.connect(
            lambda: self._activate_create_sample_data(optional_data_dialog)
        )
        optional_data_dialog.listView.clicked.connect(
            lambda: self.list_view_check_changed(optional_data_dialog)
        )
        optional_data_dialog.dialogButtonBox.accepted.connect(
            lambda: self._update_table_view(optional_data_dialog)
        )

        if not optional_data_dialog.exec_():
            return

    def list_view_check_changed(self, dialog):
        model = dialog.listView.model()
        items = [model.item(index) for index in range(model.rowCount())]
        for item in items:
            if item.checkState() == Qt.Checked and \
                    item.text() not in self.checked_items:
                self.checked_items.append(item.text())
            if item.checkState() == Qt.Unchecked and \
                    item.text() in self.checked_items:
                self.checked_items.remove(item.text())

    def _activate_create_sample_data(self, dialog):
        create_data_dialog = UserSampleDataDialog(self, self.client)

        create_data_dialog.createButtonBox.rejected.connect(
            create_data_dialog.reject
        )
        create_data_dialog.createButtonBox.accepted.connect(
            lambda: self._update_optional_data(create_data_dialog, dialog)
        )

        if not create_data_dialog.exec_():
            return

    def _update_optional_data(self, dialog, parent_dialog):
        if not dialog.nameCreatedData.text():
            return

        column_name = dialog.nameCreatedData.text()
        column_unit = dialog.unitCreatedData.text()
        if column_unit:
            column_name = column_name + f' ({column_unit})'

        created_data_dict = {
            "_" + column_name: column_name
        }

        self.optional_columns.update(created_data_dict)
        dialog.accept()
        parent_dialog.set_list_view(
            created_data_dict.values()
        )

    def _update_table_view(self, dialog):
        # Cache current data and headers so that that can be preserved if
        # when we add or remove new column to the table.
        table_data = self.model.table_data
        table_headers = len(self.headers)

        self._add_optional_data()
        self._partially_remove_optional_data()
        self._remove_optional_data()

        # Check if the table modified.
        if len(table_data[0]) != len(self.model.table_data[0]):
            self._preserve_data(self.model.table_data, table_headers)
        else:
            self._preserve_data(table_data, table_headers)

        dialog.accept()

    def _preserve_data(self, table_data, _headers):
        if self.new_column_added:
            # We need to keep track of the net change in checked items to avoid
            # duplication, i.e., if there are already checked items, they should
            # not be count when a new addition has been made.
            net_change = len(self.headers) - _headers
            self.model.table_data = [
                data + [''] * net_change for data in table_data
            ]
            self.new_column_added = False
        self.model.layoutChanged.emit()

    def _remove_optional_data(self):
        if not self.checked_items:
            for item in self.headers:
                if item not in self.permanent_columns.values():
                    self._delete_optional_data_entries(self.headers.index(item))
                    self.headers.remove(item)

    def _partially_remove_optional_data(self):
        for item in self.headers:
            if item not in list(self.permanent_columns.values()) \
                    + self.checked_items:
                self._delete_optional_data_entries(self.headers.index(item))
                self.headers.remove(item)

    def _add_optional_data(self):
        for item in self.checked_items:
            if item not in self.headers:
                self.headers.append(item)
                self.new_column_added = True

    def _delete_optional_data_entries(self, column_index):
        table = self.model.table_data
        for index, _ in enumerate(self.model.table_data):
            _data = table[index][column_index]
            table[index].remove(_data)
        self.model.table_data = table
