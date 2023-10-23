import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from src.gui.ui.ui_login_window import Ui_login_window
from src.gui.MainWindow import MainWindow
import src.database.user_controller as user_controller


class LoginWindow:

    def __init__(self):
        self.login_win = QMainWindow()
        self.ui = Ui_login_window()
        self.ui.setupUi(self.login_win)
        self.main_win = None

        self.to_login_page()
        self.ui.label.hide()
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
        response = user_controller.login(username, password)
        if response == 0:
            self.ui.username_field.clear()
            self.ui.password_field.clear()
            self.ui.username_field.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")
            self.ui.password_field.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")
        elif response == -2:
            print("User exceeded failed login attempts limit")
        else:
            self.main_win = MainWindow(response)
            self.main_win.show()
            self.login_win.close()

    def signup(self):

        username = self.ui.username_field1.text()
        password = self.ui.password_field1.text()
        confirm = self.ui.confirm_field1.text()
        email = self.ui.email_field1.text()
        if password == confirm:
            response = user_controller.sign_up(username, password, email)
            if response == 0:
                self.ui.label.setText("*Username or email is already in use")
                self.ui.label.show()
                self.ui.username_field1.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")
                self.ui.email_field1.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")
                self.ui.password_field1.setStyleSheet("QLineEdit {font: 15px}")
                self.ui.confirm_field1.setStyleSheet("QLineEdit {font: 15px}")
            else:
                self.main_win = MainWindow(response)
                self.main_win.show()
                self.login_win.close()
        else:
            self.ui.label.setText("*Passwords do no match")
            self.ui.label.show()
            self.ui.password_field1.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")
            self.ui.confirm_field1.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")
            self.ui.username_field1.setStyleSheet("QLineEdit {font: 15px}")
            self.ui.email_field1.setStyleSheet("QLineEdit {font: 15px}")

    def show(self):
        self.login_win.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_win = LoginWindow()
    login_win.show()
    sys.exit(app.exec_())
