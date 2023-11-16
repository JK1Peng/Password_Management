"""
File: src/gui/MainWindow.py

Author: Aaron Kersten, amk9398@rit.edu

Description: The primary window that is displayed and used for the majority of
    operation. Contains all the functionality that our application provides.
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtGui
from src.gui.ui.ui_main_window import Ui_main_window
from PasswordWidget import PasswordWidget
import src.database.user_controller as user_controller
import pandas as pd
import os
from definitions import ROOT_DIR


class MainWindow:
    # initialize vars for user id, and the user's list of passwords
    user_id = None
    passwords = []

    # button style css descriptions
    default_button_style1 = "QPushButton {color:#FDF8F5;font: bold 20px;border: 0;text-align:left;" \
                            "background: none;box-shadow:none;border-radius: 0px;background-color:#DDAF94;" \
                            "padding-left:40px;}" \
                            "QPushButton:hover {background-color:#E8CEBF}"

    pressed_button_style1 = "QPushButton {color:#DDAF94;font: bold 20px;border: 0;text-align:left;" \
                            "background: none;box-shadow:none;border-radius: 0px;background-color:#FDF8F5;" \
                            "padding-left:40px}" \
                            "QPushButton:hover {background-color:#E8CEBF}"

    default_button_style2 = "QPushButton {color:#FDF8F5;font: bold 20px;border: 0;text-align:center;" \
                            "background: none;box-shadow:none;border-radius: 0px;background-color:#DDAF94;}" \
                            "QPushButton:hover {background-color:#E8CEBF}"

    pressed_button_style2 = "QPushButton {color:#DDAF94;font: bold 20px;border: 0;text-align:center;" \
                            "background: none;box-shadow:none;border-radius: 0px;background-color:#FDF8F5;}" \
                            "QPushButton:hover {background-color:#E8CEBF}"

    def __init__(self, user_id):
        # initialize with session user id
        self.user_id = user_id

        # create new main window
        self.main_win = QMainWindow()
        self.ui = Ui_main_window()

        # setup ui
        self.ui.setupUi(self.main_win)

        # hide some things
        self.ui.new_password_frame.hide()
        self.ui.add_error_frame.hide()
        self.ui.export_loc_label.hide()
        self.ui.import_error_label.hide()

        # init icon elements
        self.icon1 = QtGui.QIcon()
        self.group_icon = QtGui.QIcon()
        self.profile_icon = QtGui.QIcon()
        self.password_icon = QtGui.QIcon()
        self.settings_icon = QtGui.QIcon()
        self.security_icon = QtGui.QIcon()
        self.menu_icon = QtGui.QIcon()
        self.icon1.addPixmap(QtGui.QPixmap("../icons/magnifying_glass.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.group_icon.addPixmap(QtGui.QPixmap("../icons/group_icon2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.profile_icon.addPixmap(QtGui.QPixmap("../icons/profile_icon1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.password_icon.addPixmap(QtGui.QPixmap("../icons/password_icon2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settings_icon.addPixmap(QtGui.QPixmap("../icons/settings_icon1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.security_icon.addPixmap(QtGui.QPixmap("../icons/security_icon2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menu_icon.addPixmap(QtGui.QPixmap("../icons/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.search_button.setIcon(self.icon1)
        self.ui.menu_password_button.setIcon(self.password_icon)
        self.ui.menu_group_button.setIcon(self.group_icon)
        self.ui.menu_security_button.setIcon(self.security_icon)
        self.ui.menu_profile_button.setIcon(self.profile_icon)
        self.ui.menu_settings_button.setIcon(self.settings_icon)
        self.ui.menu_toggle_button.setIcon(self.menu_icon)

        # connect button actions
        self.ui.menu_password_button.clicked.connect(self.switch_to_password_page)
        self.ui.menu_group_button.clicked.connect(self.switch_to_group_page)
        self.ui.menu_security_button.clicked.connect(self.switch_to_security_page)
        self.ui.menu_profile_button.clicked.connect(self.switch_to_profile_page)
        self.ui.menu_settings_button.clicked.connect(self.switch_to_settings_page)
        self.ui.new_password_button.clicked.connect(self.toggle_new_password_button)
        self.ui.add_password_button.clicked.connect(self.add_password)
        self.ui.search_button.clicked.connect(self.search_passwords)
        self.ui.menu_toggle_button.clicked.connect(self.toggle_menu)
        self.ui.export_button.clicked.connect(self.export_passwords)
        self.ui.import_button.clicked.connect(self.import_passwords)

        # set initial page
        self.switch_to_password_page()

        # get passwords from database and update list
        self.passwords = user_controller.get_user_passwords(self.user_id)
        self.update_password_list_widget()

    """
    Updates the rows of the password widget.
    """
    def update_password_list_widget(self):
        self.ui.password_list.clear()
        for i, password in enumerate(self.passwords):
            domain = password[0]
            account_name = password[1]
            url = password[2]
            _password = password[3]
            self.append_password_list_widget(str(i + 1), domain, account_name, url, _password)

    """
    Adds row with given credentials to password list
    """
    def append_password_list_widget(self, num, domain, account_name, url, _password):
        item = QListWidgetItem()
        password_widget = PasswordWidget(self.user_id, num, domain, account_name, url, _password)
        item.setSizeHint(password_widget.list_node.sizeHint())
        self.ui.password_list.addItem(item)
        self.ui.password_list.setItemWidget(item, password_widget.list_node)

    """"
    Reset all menu ui elements to default style.
    """
    def reset_menu_buttons(self):
        self.ui.menu_group_button.setStyleSheet(self.default_button_style1)
        self.ui.menu_password_button.setStyleSheet(self.default_button_style1)
        self.ui.menu_security_button.setStyleSheet(self.default_button_style1)
        self.ui.menu_profile_button.setStyleSheet(self.default_button_style2)
        self.ui.menu_settings_button.setStyleSheet(self.default_button_style2)
        self.ui.search_button.setIcon(self.icon1)
        self.ui.menu_password_button.setIcon(self.password_icon)
        self.ui.menu_group_button.setIcon(self.group_icon)
        self.ui.menu_security_button.setIcon(self.security_icon)
        self.ui.menu_profile_button.setIcon(self.profile_icon)
        self.ui.menu_settings_button.setIcon(self.settings_icon)
        self.ui.menu_toggle_button.setIcon(self.menu_icon)

    """
    Switch current 'self.stacked_widget' page to password page.
    """
    def switch_to_password_page(self):
        self.passwords = user_controller.get_user_passwords(self.user_id)
        self.update_password_list_widget()
        self.reset_menu_buttons()
        self.ui.menu_password_button.setStyleSheet(self.pressed_button_style1)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icons/password_icon1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.menu_password_button.setIcon(icon)
        self.ui.stacked_widget.setCurrentWidget(self.ui.password_page)

    """
    Switch current 'self.stacked_widget' page to group page.
    """
    def switch_to_group_page(self):
        self.reset_menu_buttons()
        self.ui.menu_group_button.setStyleSheet(self.pressed_button_style1)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icons/group_icon1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.menu_group_button.setIcon(icon)
        self.ui.stacked_widget.setCurrentWidget(self.ui.group_page)

    """
    Switch current 'self.stacked_widget' page to security page.
    """
    def switch_to_security_page(self):
        self.ui.import_error_label.hide()
        self.reset_menu_buttons()
        self.ui.menu_security_button.setStyleSheet(self.pressed_button_style1)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icons/security_icon1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.menu_security_button.setIcon(icon)
        self.ui.stacked_widget.setCurrentWidget(self.ui.security_page)

    """
    Switch current 'self.stacked_widget' page to profile page.
    """
    def switch_to_profile_page(self):
        self.reset_menu_buttons()
        self.ui.menu_profile_button.setStyleSheet(self.pressed_button_style2)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icons/profile_icon2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.menu_profile_button.setIcon(icon)
        self.ui.stacked_widget.setCurrentWidget(self.ui.profile_page)

    """
    Switch current 'self.stacked_widget' page to settings page.
    """
    def switch_to_settings_page(self):
        self.reset_menu_buttons()
        self.ui.menu_settings_button.setStyleSheet(self.pressed_button_style2)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icons/settings_icon2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.menu_settings_button.setIcon(icon)
        self.ui.stacked_widget.setCurrentWidget(self.ui.settings_page)

    """
    Toggle between drop down interface for creating new passwords.
    """
    def toggle_new_password_button(self):
        if self.ui.new_password_frame.isHidden():
            self.ui.new_password_frame.show()
            self.ui.new_password_button.setText("New ▼")
        else:
            self.ui.new_password_frame.hide()
            self.ui.new_password_button.setText("New ▲")

    """
    Get text field strings and use them with 'user_controller' to create 
    a new password. Display error if pertinent.
    """
    def add_password(self):
        domain = self.ui.domain_field.text()
        account_name = self.ui.account_field.text()
        url = self.ui.url_field.text()
        password = self.ui.password_field.text()
        response = user_controller.add_password(self.user_id, domain, password, account_name, url)
        if response == 1:
            self.ui.domain_field.clear()
            self.ui.account_field.clear()
            self.ui.url_field.clear()
            self.ui.password_field.clear()
            self.ui.new_password_frame.hide()
            self.ui.add_error_frame.hide()
            self.passwords = user_controller.get_user_passwords(self.user_id)
            self.update_password_list_widget()
        elif response == 0:
            self.ui.add_error_frame.show()

    """
    Search for passwords. Send query to 'user_controller' to get new list.
    """
    def search_passwords(self):
        query = self.ui.search_field.text().lower()
        response = user_controller.get_user_passwords(self.user_id, query)
        if response == 0:
            pass
        else:
            self.passwords = response
        self.update_password_list_widget()

    """
    Toggle menu sidebar size. 
    """
    def toggle_menu(self):
        if self.ui.menu_frame.width() == 100:
            self.ui.menu_frame.setFixedWidth(350)
            self.ui.menu_password_button.setText(" Passwords")
            self.ui.menu_security_button.setText(" Security")
            self.ui.menu_group_button.setText(" Groups")
            self.ui.menu_profile_button.setText("Profile")
            self.ui.menu_settings_button.setText("Settings")
        else:
            self.ui.menu_frame.setFixedWidth(100)
            self.ui.menu_password_button.setText("")
            self.ui.menu_security_button.setText("")
            self.ui.menu_group_button.setText("")
            self.ui.menu_profile_button.setText("")
            self.ui.menu_settings_button.setText("")

    """
    Export user's passwords as csv to the project root directory.
    """
    def export_passwords(self):
        # get passwords from user's repo
        passwords = user_controller.get_user_passwords(self.user_id)

        # compile data into columns
        data = {
            "name": [passwords[i][0] for i in range(len(passwords))],
            "url": [passwords[i][2] for i in range(len(passwords))],
            "username": [passwords[i][1] for i in range(len(passwords))],
            "password": [passwords[i][3] for i in range(len(passwords))],
            "note": ["" for i in range(len(passwords))]
        }

        # create dataframe and save to the root directory
        df = pd.DataFrame(data)
        loc = os.path.join(ROOT_DIR, "passwords.csv")
        df.to_csv(loc, index=False)

        # display location of file write
        self.ui.export_loc_label.setText(f"Wrote to {loc}")
        self.ui.export_loc_label.show()

    """
    Read in the csv file at the specified location. Add passwords info
    to user's password database.
    """
    def import_passwords(self):
        # get file name from text field
        filename = self.ui.import_field.text()
        try:
            # read csv at file location
            df = pd.read_csv(filename)

            # convert everything to string
            df = df.astype(str)

            # get each column
            names = df["name"].to_list()
            urls = df["url"].to_list()
            usernames = df["username"].to_list()
            passwords = df["password"].to_list()

            # add each password row to the database
            for i in range(len(names)):
                # if account_name or url are NaN, set to default
                account_name = usernames[i] if usernames[i] != "nan" else ""
                url = urls[i] if urls[i] != "nan" else ""
                response = user_controller.add_password(self.user_id, names[i], passwords[i], account_name, url)

        # if any error occurs, show error label
        except Exception as e:
            self.ui.import_error_label.show()
            return

        # hide error label
        self.ui.import_error_label.hide()

    """
    Show the main window.
    """
    def show(self):
        self.main_win.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow(2)
    main_win.show()
    sys.exit(app.exec_())
