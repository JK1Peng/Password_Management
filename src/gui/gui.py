from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def function():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(0, 0, 600, 400)
    win.setWindowTitle("Password Manager")
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    function()