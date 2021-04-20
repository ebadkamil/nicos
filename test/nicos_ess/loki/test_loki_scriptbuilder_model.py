import copy
import numpy as np
import pytest

from nicos_ess.loki.gui.loki_scriptbuilder_model import LokiScriptModel


NUM_ROWS = 20

HEADERS = ["COLUMN_1", "COLUMN_2", "COLUMN_3",
           "COLUMN_4", "COLUMN_5", "COLUMN_6"]

DATA = [["00", "01", "02", "03", "04", "05"],
        ["10", "11", "12", "13", "14", "15"],
        ["20", "21", "22", "23", "24", "25"],
        ["30", "31", "32", "33", "34", "35"],
        ["40", "41", "42", "43", "44", "45"]]

CLIPBOARD_DATA = [["a", "b", "c",],
                  ["e", "f", "g",],
                  ["i", "j", "k",]]


def create_empty_list(rows, columns):
    return [[""] * columns for _ in range(rows)]


class TestLokiScriptModel:

    @pytest.fixture(autouse=True)
    def prepare(self):
        self.model = LokiScriptModel(HEADERS, NUM_ROWS)
        self.model.table_data = copy.deepcopy(DATA)

    def test_initialization_done_correctly(self):
        # check shape of the table_data
        assert len(self.model.table_data) == NUM_ROWS
        assert all(
            [len(data) == len(HEADERS) for data in self.model.table_data])
        # check if (NUM_ROWS - len(DATA)) number of empty rows are created
        assert self.model.table_data == DATA + create_empty_list(
            NUM_ROWS - len(DATA), len(HEADERS))

    def test_row_inserted_at_position(self):
        position = 2
        self.model.insertRow(position)
        assert len(self.model.table_data) == NUM_ROWS + 1

        assert self.model.table_data[position-1] == DATA[position-1]
        assert self.model.table_data[position] == [""] * len(HEADERS)
        assert self.model.table_data[position+1] == DATA[position]

    def test_data_selected_for_selected_indices(self):
        # TODO: Improve this test
        selected_indices = [(0, 0), (0, 1), (0, 2),
                            (1, 0), (1, 1), (1, 2)]
        selected_data = self.model.select_data(selected_indices)
        assert selected_data == ["\t".join(DATA[0][:3]),
                                 "\t".join(DATA[1][:3])]

    def test_clipboard_data_gets_pasted_correctly_at_top_left_index(self):
        top_left = (0, 0)
        self.model.update_data_from_clipboard(
            copy.deepcopy(CLIPBOARD_DATA), top_left)

        # Convert to numpy arrays for easy slicing
        table_data_np = np.array(self.model.table_data, dtype=np.str_)
        clipboard_data_np = np.array(CLIPBOARD_DATA, dtype=np.str_)

        clip_shape = clipboard_data_np.shape
        table_shape = table_data_np.shape
        # May be use np.testing.array_equal
        # TODO: Simplify and correct it.
        assert table_data_np[top_left[0]:top_left[0]+clip_shape[0],
                             top_left[1]:top_left[1]+clip_shape[1]].tolist() ==\
               clipboard_data_np[:,:table_shape[1]-top_left[1]].tolist()

    def test_extra_rows_created_when_clipboard_data_pasted_at_bottom_row(self):
        bottom_left = (NUM_ROWS - 1, 0)
        self.model.update_data_from_clipboard(
            copy.deepcopy(CLIPBOARD_DATA), bottom_left)

        assert len(self.model.table_data) == NUM_ROWS + len(CLIPBOARD_DATA) - 1

    def test_clipboard_data_gets_pasted_in_table_with_hidden_columns(self):
        pass
