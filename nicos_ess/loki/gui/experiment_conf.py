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

"""LoKI Experiment Configuration dialog."""
from nicos.guisupport.qt import QMessageBox, Qt

from nicos.clients.gui.utils import loadUi
from nicos.utils import findResource

from nicos_ess.loki.gui.loki_panel import LokiPanelBase
from nicos_ess.loki.gui.sample_environment import SampleEnvironmentBase


class LokiExperimentPanel(LokiPanelBase, SampleEnvironmentBase):
    panelName = 'LoKI Instrument Setup'

    def __init__(self, parent, client, options):
        LokiPanelBase.__init__(self, parent, client, options)
        SampleEnvironmentBase.__init__(self)
        loadUi(self, findResource('nicos_ess/loki/gui/ui_files/exp_config.ui'))

        self.window = parent

        self.holder_info = options.get('holder_info', [])
        self.instrument = options.get('instrument', 'loki')
        self.initialise_connection_status_listeners()
        self.initialise_environments()
        self.initialise_markups()

        self.envComboBox.addItems(self.get_environment_names())
        # Start with a "no item", ie, empty selection.
        self.envComboBox.setCurrentIndex(-1)

        # Hide read-only properties and hide and disable reference cell
        # positions until a sample environment is chosen by the user.
        self.propertiesGroupBox.setVisible(False)

        # Hide and disable cell position properties which shall be only
        # available for sample environments that holds them.
        self.refPosGroupBox.setVisible(False)

        self.envComboBox.activated.connect(self._activate_environment_settings)

        # Listen to changes in Aperture and Detector Offset values
        self.apXBox.textChanged.connect(self.set_apt_pos_x)
        self.apYBox.textChanged.connect(self.set_apt_pos_y)
        self.apWBox.textChanged.connect(self.set_apt_width)
        self.apHBox.textChanged.connect(self.set_apt_height)
        self.offsetBox.textChanged.connect(self.set_det_offset)

        # Listen to changes in environments
        self.refPosXBox.textChanged.connect(self.set_ref_pos_x)
        self.refPosYBox.textChanged.connect(self.set_ref_pos_y)

        # Disable apply buttons in both settings until an action taken by the
        # user.
        self.sampleSetApply.setEnabled(False)
        self.instSetApply.setEnabled(False)

        # Required for the dynamic validation
        self.invalid_sample_settings = []
        self.invalid_instrument_settings = []

    def initialise_environments(self):
        self.add_environment('SampleChanger',
                             {
                                'name': 'Tumbler Sample Changer',
                                'number_of_cells': '4',
                                'cell_type': 'Titanium',
                                'can_rotate_samples': 'Yes',
                                'has_temperature_control': 'No',
                                'has_pressure_control': 'No'
                             }
                             )
        self.add_environment('SampleChanger',
                             {
                                'name': 'Peltier Sample Changer',
                                'number_of_cells': '12',
                                'cell_type': 'Copper',
                                'can_rotate_samples': 'No',
                                'has_temperature_control': 'Yes',
                                'has_pressure_control': 'No'
                             }
                             )
        self.add_environment('SampleChanger',
                             {
                                'name': 'Dome Cell Sample Changer',
                                'number_of_cells': '4',
                                'cell_type': 'Aluminium/Titanium',
                                'can_rotate_samples': 'No',
                                'has_temperature_control': 'Yes',
                                'has_pressure_control': 'Yes'
                             }
                             )

    def initialise_markups(self):
        setting_boxes = [
            self.apXBox, self.apYBox, self.apWBox, self.apHBox,
            self.offsetBox, self.refPosXBox, self.refPosYBox
        ]
        for box in setting_boxes:
            box.setAlignment(Qt.AlignRight)
            box.setPlaceholderText('0.0')

    def setViewOnly(self, viewonly):
        self.sampleSetGroupBox.setEnabled(not viewonly)
        self.instSetGroupBox.setEnabled(not viewonly)

    def _activate_environment_settings(self):
        # Fill the read-only fields.
        environment_type, environment = self._get_selected_environment()
        self._map_environment_fields_to_properties(environment_type,
                                                   environment)

        # Enable sample environments
        self.propertiesGroupBox.setVisible(True)

        if environment_type == "SampleChanger":
            self.refPosGroupBox.setVisible(True)
            self.refPosGroupBox.setEnabled(True)
            self.refCellSpinBox.setFocus()

    def _get_selected_environment(self):
        for environment in self.environment_list:
            if environment[1].name == self.envComboBox.currentText():
                return environment

    def _map_environment_fields_to_properties(self, environment_type,
                                              environment):
        _sample_changer = {
            'first_property': [
                (self.firstPropertyLabel, "Number of Cells:"),
                (self.firstPropertyBox, environment.number_of_cells)
            ],
            'second_property': [
                (self.secondPropertyLabel, "Cell Type:"),
                (self.secondPropertyBox, environment.cell_type)
            ],
            'third_property': [
                (self.thirdPropertyLabel, "Rotate Samples:"),
                (self.thirdPropertyBox, environment.can_rotate_samples)
            ],
            'fourth_property': [
                (self.fourthPropertyLabel, "Temperature Control:"),
                (self.fourthPropertyBox, environment.has_temperature_control)
            ],
            'fifth_property': [
                (self.fifthPropertyLabel, "Pressure Control:"),
                (self.fifthPropertyBox, environment.has_pressure_control)
            ]
        }
        if environment_type == 'SampleChanger':
            for k in _sample_changer:
                _sample_changer[k][0][0].setText(_sample_changer[k][0][1])
                _sample_changer[k][1][0].setText(_sample_changer[k][1][1])

    def set_det_offset(self, value):
        value_type = 'det_offset'
        self._set_instrument_settings(value, value_type)

    def set_apt_pos_x(self, value):
        value_type = 'apt_pos_x'
        self._set_instrument_settings(value, value_type)

    def set_apt_pos_y(self, value):
        value_type = 'apt_pos_y'
        self._set_instrument_settings(value, value_type)

    def set_apt_width(self, value):
        value_type = 'apt_width'
        self._set_instrument_settings(value, value_type)

    def set_apt_height(self, value):
        value_type = 'apt_height'
        self._set_instrument_settings(value, value_type)

    def set_ref_pos_x(self, value):
        value_type = 'ref_pos_x'
        self._set_instrument_settings(value, value_type)

    def set_ref_pos_y(self, value):
        value_type = 'ref_pos_y'
        self._set_instrument_settings(value, value_type)

    def _set_instrument_settings(self, value, value_type):
        if not value:
            return
        map_value_type_to_settings = {
            'sample': ['ref_pos_x', 'ref_pos_y'],
            'instrument': ['apt_pos_x', 'apt_pos_y',
                           'apt_width', 'apt_height', 'det_offset']
        }
        # Get settings type from value type
        for key, values in map_value_type_to_settings.items():
            if value_type in values:
                settings_type = key
                # Validate wrt settings type
                self._validate_instrument_settings(value, value_type,
                                                   settings_type)

    def _validate_instrument_settings(self, value, value_type, settings_type):
        # The entered value to any of the settings should be float-able.
        # If not, this is caught by the Python runtime during casting
        # and raises an error. We would like to warn to user without raising.
        map_settings = {
            'sample': (self.sampleSetApply.setEnabled,
                       self.invalid_sample_settings),
            'instrument': (self.instSetApply.setEnabled,
                           self.invalid_instrument_settings)
        }
        map_value_type_to_setting = {
            'apt_pos_x': self.apXBox,
            'apt_pos_y': self.apYBox,
            'apt_width': self.apWBox,
            'apt_height': self.apHBox,
            'det_offset': self.offsetBox,
            'ref_pos_x': self.refPosXBox,
            'ref_pos_y': self.refPosYBox
        }
        try:
            float(value)
            if value_type in map_settings[settings_type][1]:
                map_settings[settings_type][1].remove(value_type)
                map_value_type_to_setting[value_type]. \
                    setClearButtonEnabled(False)
            # Enable apply button upon validation here to prevent repetition
            # of the code and/or misbehaviour due to multiple edits.
            if len(map_settings[settings_type][1]) == 0:
                map_settings[settings_type][0](True)
            return
        except ValueError:
            if value_type not in map_settings[settings_type][1]:
                QMessageBox.warning(self, 'Error',
                                    'A value should be a number.')
                map_settings[settings_type][1].append(value_type)
                map_value_type_to_setting[value_type].\
                    setClearButtonEnabled(True)
            map_settings[settings_type][0](False)

