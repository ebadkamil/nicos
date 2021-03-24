from nicos.guisupport.qt import QDoubleValidator, QIntValidator, QLineEdit, \
    QRegExp, QRegExpValidator, QStyledItemDelegate, Qt


class Validators:
    class PIntValidator(QIntValidator):
        def __init__(self, parent=None):
            super().__init__(parent=parent)
            self.setBottom(0)

    class PDoubleValidator(QDoubleValidator):
        def __init__(self, parent=None):
            super().__init__(parent=parent)
            self.setBottom(0.0)

    integer = QIntValidator()
    pinteger = PIntValidator()
    double = QDoubleValidator()
    pdouble = PDoubleValidator()
    string = QRegExpValidator(QRegExp("^(?!\s*$).+"))


class Delegate(QStyledItemDelegate):
    def __init__(self, owner, validator_type):
        super().__init__(owner)
        self.validator_type = validator_type

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setValidator(self.validator_type)
        return editor

    def setModelData(self, editor, model, index):
        text = editor.text()
        model.setData(index, text, Qt.EditRole)
