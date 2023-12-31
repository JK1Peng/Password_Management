"""
File: src/gui/LoginWindow.py

Author: Aaron Kersten, amk9398@rit.edu

Description: The first window that shows up when the program is run. Prompts
    the user for a username or password, or allows them the opportunity to make
    an account with the system.
"""

import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit
from src.gui.ui.ui_login_window import Ui_login_window
from src.gui.MainWindow import MainWindow
import src.database.user_controller as user_controller
import random
from src.smtp.email_controller import send_verification_email, send_hint_email
from src.captcha.generate_captcha import generate_captcha
import os
from definitions import ROOT_DIR
from src.passwords.password_strength import password_check



class LoginWindow:

    # initialize var for main window
    main_win = None

    password = None
    username = None
    code = None
    captcha_text = None

    def __init__(self):
        # create new login window
        self.login_win = QMainWindow()
        self.ui = Ui_login_window()

        # setup ui
        self.ui.setupUi(self.login_win)

        self.ui.password_field.setEchoMode(QLineEdit.EchoMode.Password)

        # set initial page
        self.to_login_page()

        # hide the sign up error label
        self.ui.signup_error_label.hide()
        self.ui.login_verify_frame.hide()

        # connect button actions
        self.ui.to_login_button.clicked.connect(self.to_login_page)
        self.ui.to_signup_button.clicked.connect(self.to_signup_page)
        self.ui.login_button.clicked.connect(self.login)
        self.ui.signup_button.clicked.connect(self.signup)
        self.ui.verify_cancel_button.clicked.connect(self.cancel_verify)
        self.ui.verify_button.clicked.connect(self.verify_code)
        self.ui.login_verify_button.clicked.connect(lambda: self.to_hint_page(self.to_captcha_page, "Enter"))
        self.ui.hint_back_button.clicked.connect(self.to_login_page)
        self.ui.forgot_password_button.clicked.connect(lambda: self.to_hint_page(self.send_hint, "Send hint"))
        self.ui.captcha_send_button.clicked.connect(lambda: self.check_captcha(self.to_verify_page))
        self.ui.refresh_button.clicked.connect(self.regen_captcha)

    """
    Set current 'stacked_widget' page to the login page.
    """
    def to_login_page(self):
        self.ui.username_field.setStyleSheet("QLineEdit {font: 15px}")
        self.ui.password_field.setStyleSheet("QLineEdit {font: 15px}")
        self.ui.stacked_widget.setCurrentWidget(self.ui.login_page)

    """
    Set current 'stacked_widget' page to the sign-up page.
    """
    def to_signup_page(self):
        self.ui.stacked_widget.setCurrentWidget(self.ui.sign_up_page)

    """
    Set current 'stacked_widget' page to the verify page. Send verification
    email, and switch to verify page.
    """
    def to_verify_page(self, email=None):
        # if email is not specified, get email based on used login username
        if not email:
            username = self.ui.hint_username_field.text()
            email = user_controller.get_user_email(username=username)

            # if error returned, do not proceed
            if email == 0 or email == -1:
                return

        self.ui.verify_label.setText(f"A verification code has been sent to {email}. "
                                     "\nPlease enter it below to proceed. ")

        # choose random number for the verification code
        self.code = str(random.randint(100, 999)) + str(random.randint(100, 999))

        # send verification email to user's account
        response = send_verification_email(email, self.code)

        # successful send: switch to verify page
        if response == 1:
            self.ui.verify_label.setText(f"A verification code has been sent to {email} "
                                         "\nPlease enter it below to proceed. ")
            self.ui.stacked_widget.setCurrentWidget(self.ui.verify_page)

        # unsuccessful: cancel verification process
        else:
            self.cancel_verify()

    """
    Set current 'stacked_widget' page to the hint page.
    """
    def to_hint_page(self, redirect, button_label):
        self.ui.hint_send_button.clicked.connect(redirect)
        self.ui.hint_send_button.setText(button_label)
        self.ui.stacked_widget.setCurrentWidget(self.ui.hint_page)

    def to_captcha_page(self):
        self.regen_captcha()
        self.ui.stacked_widget.setCurrentWidget(self.ui.captcha_page)

    """
    Remove attempted sign up account. Return to login page.
    """
    def cancel_verify(self):
        user_controller.remove_account(username=self.username)
        self.ui.email_field1.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")
        self.to_login_page()

    """
    Get username and password from text fields. Attempt to login to using
    the given credentials. If the login is successful, close current window
    and start a 'MainWindow' using the received 'user_id'. Highlight the 
    text fields red upon failure. 
    """
    def login(self):
        # get username and password from text fields
        self.username = self.ui.username_field.text()
        self.password = self.ui.password_field.text()

        # send login request to database
        response = user_controller.login(self.username, self.password)

        # username or password incorrect
        if response == 0:
            self.ui.username_field.clear()
            self.ui.password_field.clear()
            self.ui.username_field.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")
            self.ui.password_field.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")

        # account not verified
        elif response == -2:
            self.ui.login_verify_frame.show()

        # login successful: open main window
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
        # get strings from text fields
        self.username = self.ui.username_field1.text()
        self.password = self.ui.password_field1.text()
        confirm = self.ui.confirm_field1.text()
        email = self.ui.email_field1.text()
        hint = self.ui.password_hint_field.text()

        # calculate password strength
        password_strength = password_check(self.password, self.username)

        # if hint is left blank, set to None
        if hint == "":
            hint = None

        # check that password equals confirm password
        if self.password == confirm:

            # verify password is strong
            if password_strength is True:

                # send sign up request to the database
                response = user_controller.sign_up(self.username, self.password, email, hint)

                # username or email already in use
                if response == 0:
                    self.ui.signup_error_label.setText("*Username or email is already in use")
                    self.ui.signup_error_label.show()
                    self.ui.username_field1.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")
                    self.ui.email_field1.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")
                    self.ui.password_field1.setStyleSheet("QLineEdit {font: 15px}")
                    self.ui.confirm_field1.setStyleSheet("QLineEdit {font: 15px}")

                # if login successful, go to verification page
                else:
                    self.to_verify_page(email)

            # if password is weak, display error label
            else:
                self.ui.signup_error_label.setText(f"*Password is not strong enough: {password_strength}")
                self.ui.signup_error_label.show()

        else:
            self.ui.signup_error_label.setText("*Passwords do no match")
            self.ui.signup_error_label.show()
            self.ui.password_field1.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")
            self.ui.confirm_field1.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")
            self.ui.username_field1.setStyleSheet("QLineEdit {font: 15px}")
            self.ui.email_field1.setStyleSheet("QLineEdit {font: 15px}")

    """
    Verify entered code. Login into MainWindow upon success.
    """
    def verify_code(self):
        # get code from text field
        code = self.ui.verify_code_field.text()

        # check that code is correct
        if code == self.code:
            # verify user and login
            user_controller.verify_user(username=self.username)
            response = user_controller.login(self.username, self.password)

            # if original login credentials were not correct, return to login page
            if response == 0:
                self.ui.login_verify_frame.hide()
                self.ui.username_field.clear()
                self.ui.password_field.clear()
                self.ui.username_field.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")
                self.ui.password_field.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")
                self.to_login_page()
            elif response > 0:
                self.main_win = MainWindow(response)
                self.main_win.show()
                self.login_win.close()

        # if not, make text field red
        else:
            self.ui.verify_code_field.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")

    """
    Send password hint to the user's email address.
    """
    def send_hint(self):
        username = self.ui.hint_username_field.text()
        email = self.ui.hint_email_field.text()
        response = user_controller.check_user_email(username, email)
        if response == 1:
            hint = user_controller.get_user_hint(username)
            send_hint_email(email, hint)
        else:
            self.ui.hint_username_field.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")
            self.ui.hint_email_field.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")

    """
    Regenerate a captcha image in the captcha folder.
    """
    def regen_captcha(self):
        file_location = os.path.join(ROOT_DIR, "src", "captcha", "captcha.png")
        self.captcha_text = generate_captcha(file_location)
        pixmap = QPixmap(file_location)
        self.ui.captcha_label.setPixmap(pixmap)

    """
    Check entered code matches the captcha. Redirect to next_fun.
    """
    def check_captcha(self, next_func):
        if self.ui.captcha_code_field.text() == self.captcha_text:
            next_func()
        else:
            self.ui.captcha_code_field.setStyleSheet("QLineEdit {font: 15px;background-color:#fa9487}")

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
