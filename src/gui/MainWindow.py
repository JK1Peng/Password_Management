import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from src.gui.Ui_MainWindow import Ui_MainWindow


class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        self.ui.stackedWidget.setCurrentWidget(self.ui.password_page)

        self.ui.menuButton1.clicked.connect(self.switch_to_password_page)
        self.ui.menuButton2.clicked.connect(self.switch_to_group_page)

    def switch_to_password_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.password_page)

    def switch_to_group_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)

    def show(self):
        self.main_win.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    ui = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
