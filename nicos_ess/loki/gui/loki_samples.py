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
from nicos.guisupport.qt import QHeaderView, QTableView, QDialog,\
    QStandardItemModel, QStandardItem, Qt

TABLE_QSS = 'alternate-background-color: aliceblue;'


class CreateSampleData(QDialog):

    def __init__(self, parent, client):
        QDialog.__init__(self, parent)
        self.client = client
        loadUi(self, findResource('nicos_ess/loki/gui/'
                                  'ui_files/'
                                  'loki_create_sample_data.ui'))


class OptionalSampleData(QDialog):

    def __init__(self, parent, client, optional_data, checked=False):
        QDialog.__init__(self, parent)
        self.client = client
        loadUi(self, findResource('nicos_ess/loki/gui/'
                                  'ui_files/'
                                  'loki_samples_optional_data.ui'))

        self.model = QStandardItemModel()

        self.set_list_view(optional_data, checked)

        self.dialogButtonBox.rejected.connect(self.reject)
        self.dialogButtonBox.accepted.connect(self.accept)

    def set_list_view(self, optional_data, checked):
        for data in optional_data:
            item = QStandardItem(data)
            item.setCheckable(True)
            check = Qt.Checked if checked else Qt.Unchecked
            item.setCheckState(check)
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
        self._init_table_panel()

    def _init_table_panel(self):
        headers = [
            self.permanent_columns[name]
            for name in self.columns_in_order
        ]

        self.model = LokiDataModel(headers)
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
        optional_data_dialog = OptionalSampleData(
            self, self.client, self.optional_columns.values()
        )

        optional_data_dialog.createDataButton.clicked.connect(
            lambda: self._activate_create_sample_data(optional_data_dialog)
        )
        if not optional_data_dialog.exec_():
            return

    def _activate_create_sample_data(self, dialog):
        create_data_dialog = CreateSampleData(self, self.client)

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
        else:
            column_name = column_name

        _key = "_" + column_name
        _value = column_name
        created_data_dict = {
            _key: _value
        }

        self.optional_columns.update(created_data_dict)
        dialog.accept()
        parent_dialog.clear_list()
        parent_dialog.set_list_view(
            self.optional_columns.values(), checked=False
        )
