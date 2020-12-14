from aqt.qt import QDialog, QLabel, QVBoxLayout
from aqt import mw

class Options(QDialog):
    def __init__(self, parent = None):
        if parent is None:
            parent = mw.app.activeWindow()

        QDialog.__init__(self, parent)
        self.parent = parent

        self.setWindowTitle("Set SM-style Cloze")
        self.setup_ui()
        self.exec_()

    def setup_ui(self):
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("Test"))
        vbox.addWidget(QLabel("Test2"))

        self.setLayout(vbox)

def open_options():
    option = Options()
