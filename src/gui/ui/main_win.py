from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtGui

class MainWindowFrame(QMainWindow):
    def __init__(self, func, parent=None):
        super(MainWindowFrame, self).__init__(parent)
        self.func = func

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.func()
