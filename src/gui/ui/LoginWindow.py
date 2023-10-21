import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from src.gui.ui.ui_login_window import Ui_login_window
from src.gui.ui.MainWindow import MainWindow
import src.database.user_controller as user_controller


class LoginWindow:

    def __init__(self):
        self.login_win = QMainWindow()
        self.ui = Ui_login_window()
        self.ui.setupUi(self.login_win)
        self.main_win = None

        self.to_login_page()
        self.ui.to_login_button.clicked.connect(self.to_login_page)
        self.ui.to_signup_button.clicked.connect(self.to_signup_page)
        self.ui.login_button.clicked.connect(self.login)
        self.ui.signup_button.clicked.connect(self.signup)

    def to_login_page(self):
        self.ui.stacked_widget.setCurrentWidget(self.ui.login_page)

    def to_signup_page(self):
        self.ui.stacked_widget.setCurrentWidget(self.ui.sign_up_page)

    def login(self):
        username = self.ui.username_field.text()
        password = self.ui.password_field.text()
        user_id = user_controller.login(username, password)
        if user_id >= 1:
            self.main_win = MainWindow(user_id)
            self.main_win.show()
            self.login_win.close()

    def signup(self):
        username = self.ui.username_field1.text()
        password = self.ui.password_field1.text()
        confirm = self.ui.confirm_field1.text()
        email = self.ui.email_field1.text()
        if password == confirm:
            user_id = user_controller.sign_up(username, password, email)
            if user_id >= 1:
                self.main_win = MainWindow(user_id)
                self.main_win.show()
                self.login_win.close()

    def show(self):
        self.login_win.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_win = LoginWindow()
    login_win.show()
    sys.exit(app.exec_())
