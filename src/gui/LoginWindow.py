"""
File: src/gui/LoginWindow.py

Author: Aaron Kersten, amk9398@rit.edu

Description: The first window that shows up when the program is run. Prompts
    the user for a username or password, or allows them the opportunity to make
    an account with the system.
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from src.gui.ui.ui_login_window import Ui_login_window
from src.gui.MainWindow import MainWindow
import src.database.user_controller as user_controller


class LoginWindow:

    # initialize var for main window
    main_win = None

    def __init__(self):
        # create new login window
        self.login_win = QMainWindow()
        self.ui = Ui_login_window()

        # setup ui
        self.ui.setupUi(self.login_win)

        # set initial page
        self.to_login_page()

        # hide the sign up error label
        self.ui.signup_error_label.hide()

        # connect button actions
        self.ui.to_login_button.clicked.connect(self.to_login_page)
        self.ui.to_signup_button.clicked.connect(self.to_signup_page)
        self.ui.login_button.clicked.connect(self.login)
        self.ui.signup_button.clicked.connect(self.signup)

    """
    Set current 'stacked_widget' page to the login page.
    """
    def to_login_page(self):
        self.ui.stacked_widget.setCurrentWidget(self.ui.login_page)

    """
    Set current 'stacked_widget' page to the sign-up page.
    """
    def to_signup_page(self):
        self.ui.stacked_widget.setCurrentWidget(self.ui.sign_up_page)

    """
    Get username and password from text fields. Attempt to login to using
    the given credentials. If the login is successful, close current window
    and start a 'MainWindow' using the received 'user_id'. Highlight the 
    text fields red upon failure. 
    """
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

    """
    Get account credentials from text fields. Attempt to signup using those
    credentials. If the signup is successful, proceed as a successful login.
    If not, display relevant error message. 
    """
    def signup(self):
        username = self.ui.username_field1.text()
        password = self.ui.password_field1.text()
        confirm = self.ui.confirm_field1.text()
        email = self.ui.email_field1.text()
        if password == confirm:
            response = user_controller.sign_up(username, password, email)
            if response == 0:
                self.ui.signup_error_label.setText("*Username or email is already in use")
                self.ui.signup_error_label.show()
                self.ui.username_field1.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")
                self.ui.email_field1.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")
                self.ui.password_field1.setStyleSheet("QLineEdit {font: 15px}")
                self.ui.confirm_field1.setStyleSheet("QLineEdit {font: 15px}")
            else:
                self.main_win = MainWindow(response)
                self.main_win.show()
                self.login_win.close()
        else:
            self.ui.signup_error_label.setText("*Passwords do no match")
            self.ui.signup_error_label.show()
            self.ui.password_field1.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")
            self.ui.confirm_field1.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")
            self.ui.username_field1.setStyleSheet("QLineEdit {font: 15px}")
            self.ui.email_field1.setStyleSheet("QLineEdit {font: 15px}")

    """
    Show the login window.
    """
    def show(self):
        self.login_win.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_win = LoginWindow()
    login_win.show()
    sys.exit(app.exec_())
