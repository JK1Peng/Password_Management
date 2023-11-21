"""
File: src/gui/MainWindow.py

Author: Aaron Kersten, amk9398@rit.edu

Description: The primary window that is displayed and used for the majority of
    operation. Contains all the functionality that our application provides.
"""

import sys

from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from src.gui.ui.ui_main_window import Ui_main_window
import src.database.user_controller as user_controller
import pandas as pd
import os
from definitions import ROOT_DIR
from src.gui.ui.ui_password_field_widget import Ui_Form
from src.gui.ui.ui_label_field_widget import Ui_label_widget
from src.gui.ui.ui_delete_widget import Ui_delete_widget
from src.gui.ui.ui_dropdown_widget import Ui_dropdown
from src.gui.ui.ui_category_widget import Ui_category_widget
from src.passwords.password_strength import measure_password_strength
from src.gui.ui.main_win import MainWindowFrame
from src.gui.ui.ui_button_widget import Ui_button_widget
from src.gui.ui.ui_label_edit import Ui_text_field_widget
import pyperclip as pc
from src.captcha.generate_captcha import generate_captcha


class MainWindow:
    # initialize vars for user id, the user's list of passwords and categories
    user_id = None
    passwords = []
    categories = []
    category_widgets = []
    edit_fields = []

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
        self.main_win = MainWindowFrame(self.resizeEvent)
        self.ui = Ui_main_window()

        # setup ui
        self.ui.setupUi(self.main_win)

        # set password table header labels
        self.ui.password_list.setHorizontalHeaderItem(0, QTableWidgetItem("Domain"))
        self.ui.password_list.setHorizontalHeaderItem(1, QTableWidgetItem("URL"))
        self.ui.password_list.setHorizontalHeaderItem(2, QTableWidgetItem("Account name"))
        self.ui.password_list.setHorizontalHeaderItem(3, QTableWidgetItem("Category"))
        self.ui.password_list.setHorizontalHeaderItem(4, QTableWidgetItem("Password"))
        self.ui.password_list.setHorizontalHeaderItem(5, QTableWidgetItem("Options"))

        self.ui.security_table.setHorizontalHeaderItem(0, QTableWidgetItem("Domain"))
        self.ui.security_table.setHorizontalHeaderItem(1, QTableWidgetItem("URL"))
        self.ui.security_table.setHorizontalHeaderItem(2, QTableWidgetItem("Account name"))
        self.ui.security_table.setHorizontalHeaderItem(3, QTableWidgetItem("Category"))
        self.ui.security_table.setHorizontalHeaderItem(4, QTableWidgetItem("Password"))
        self.ui.security_table.setHorizontalHeaderItem(5, QTableWidgetItem("Strength"))

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
        self.icon1.addPixmap(QtGui.QPixmap(os.path.join(ROOT_DIR, "src", "gui", "icons", "magnifying_glass.png")),
                             QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.group_icon.addPixmap(QtGui.QPixmap(os.path.join(ROOT_DIR, "src", "gui", "icons", "group_icon2.png")),
                                  QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.profile_icon.addPixmap(QtGui.QPixmap(os.path.join(ROOT_DIR, "src", "gui", "icons", "profile_icon1.png")),
                                    QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.password_icon.addPixmap(QtGui.QPixmap(os.path.join(ROOT_DIR, "src", "gui", "icons", "password_icon2.png")),
                                     QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settings_icon.addPixmap(QtGui.QPixmap(os.path.join(ROOT_DIR, "src", "gui", "icons", "settings_icon1.png")),
                                     QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.security_icon.addPixmap(QtGui.QPixmap(os.path.join(ROOT_DIR, "src", "gui", "icons", "security_icon2.png")),
                                     QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menu_icon.addPixmap(QtGui.QPixmap(os.path.join(ROOT_DIR, "src", "gui", "icons", "logo.png")),
                                 QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        self.ui.new_category_button.clicked.connect(self.add_new_category)
        self.ui.run_security_button.clicked.connect(self.run_security_check)

        # set initial page
        self.switch_to_password_page()

        generate_captcha("captcha.png")

    """
    Updates the rows of the password widget.
    """
    def update_password_list_widget(self):
        self.ui.password_list.setRowCount(0)
        for i, password in enumerate(self.passwords):
            domain, account_name, url, _password, category_name, color, entry_id = password
            # category_id = list(filter(lambda x: x[0] == category_name, self.categories))[0]
            self.append_password_list_widget(domain, account_name, url, _password, category_name, color, entry_id, 0)

    """
    Adds row with given credentials to password list
    """
    def append_password_list_widget(self, domain, account_name, url, _password, category_name, color, entry_id, category_id):
        row_position = self.ui.password_list.rowCount()
        self.ui.password_list.insertRow(row_position)
        self.ui.password_list.setCellWidget(row_position, 0, self.create_label_widget(domain, color))
        self.ui.password_list.setCellWidget(row_position, 1, self.create_label_widget(url, color))
        self.ui.password_list.setCellWidget(row_position, 2, self.create_label_widget(account_name, color))
        self.ui.password_list.setCellWidget(row_position, 3, self.create_label_widget(category_name, color))
        self.ui.password_list.setCellWidget(row_position, 4, self.create_password_widget(_password, color))
        self.ui.password_list.setCellWidget(row_position, 5, self.create_dropdown_widget(domain, account_name, url,
                                                                                         _password, category_name,
                                                                                         row_position, entry_id,
                                                                                         category_id))

    """
    Create label widget for the password list.
    """
    @staticmethod
    def create_label_widget(text, color="#4F4846"):
        label_widget = QtWidgets.QWidget()
        ui = Ui_label_widget()
        ui.setupUi(label_widget)
        ui.label_4.setText(text)
        ui.label_4.setStyleSheet("QLabel {font: 16px;color:" + color + ";}")
        return label_widget

    """
    Create widget with password label and copy button.
    """
    def create_password_widget(self, text, color):
        widget = QtWidgets.QWidget()
        ui = Ui_Form()
        ui.setupUi(widget)
        copy_icon = QtGui.QIcon()
        copy_icon.addPixmap(QtGui.QPixmap(os.path.join(ROOT_DIR, "src", "gui", "icons", "copy.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ui.copy_button.setIcon(copy_icon)
        ui.password_label.setText("*******")
        ui.password_label.setStyleSheet("QPushButton {color:" + color + ";font: 16px;border: 0;background: none;"
                                        "box-shadow: none;border-radius: 5px;background-color:#FDF8F5;text-align: left}")
        ui.copy_button.clicked.connect(lambda: pc.copy(text))
        ui.password_label.clicked.connect(lambda: self.toggle_password_hide(ui.password_label, text))
        return widget

    """
    Create delete button widget for the password list.
    """
    def create_delete_widget(self, domain, account_name, row):
        delete_widget = QtWidgets.QWidget()
        ui = Ui_delete_widget()
        ui.setupUi(delete_widget)
        ui.x_button.clicked.connect(lambda: self.delete_password(domain, account_name, row))
        return delete_widget

    """
    Create the dropdown widget for the password list.
    """
    def create_dropdown_widget(self, domain, account_name, url, password, category, row, entry_id, category_id):
        dropdown_widget = QtWidgets.QWidget()
        ui = Ui_dropdown()
        ui.setupUi(dropdown_widget)
        ui.comboBox.addItems(["-", "Edit", "Delete"])
        ui.comboBox.activated[str].connect(lambda text: self.dropdown_action(text, domain, account_name, url, password,
                                                                             category, entry_id, row, category_id))
        return dropdown_widget

    def create_dropdown_edit(self, text):
        dropdown_widget = QtWidgets.QWidget()
        ui = Ui_dropdown()
        ui.setupUi(dropdown_widget)
        for category in self.categories:
            ui.comboBox.addItem(category[1])
        ui.comboBox.setCurrentText(text)
        self.edit_fields.append(ui.comboBox)
        return dropdown_widget

    def create_line_edit_widget(self, text):
        line_edit_widget = QtWidgets.QWidget()
        ui = Ui_text_field_widget()
        ui.setupUi(line_edit_widget)
        ui.label_edit.setText(text)
        self.edit_fields.append(ui.label_edit)
        return line_edit_widget

    def create_button_widget(self, entry_id, category):
        button_widget = QtWidgets.QWidget()
        ui = Ui_button_widget()
        ui.setupUi(button_widget)
        ui.submit_button.clicked.connect(lambda: self.submit_password_edit(entry_id, category))
        return button_widget

    """
    Perform action on dropdown click.
    """
    def dropdown_action(self, text, domain, account_name, url, password, category, entry_id, row, category_id):
        if text == "Edit":
            self.update_password_list_widget()
            self.edit_fields = []
            self.edit_password_row(domain, account_name, url, password, category, entry_id, row, category_id)
        elif text == "Delete":
            self.delete_password(domain, account_name, row)

    """
    Delete a user's password (from both the table and the database).
    """
    def delete_password(self, domain, account_name, row):
        user_controller.remove_password(self.user_id, domain, account_name)
        self.ui.password_list.removeRow(row)

    def toggle_password_hide(self, button, text):
        if button.text() == "*******":
            button.setText(text)
        else:
            button.setText("*******")

    def edit_password_row(self, domain, account_name, url, password, category, entry_id, row, category_id):
        self.ui.password_list.setCellWidget(row, 0, self.create_line_edit_widget(domain))
        self.ui.password_list.setCellWidget(row, 1, self.create_line_edit_widget(url))
        self.ui.password_list.setCellWidget(row, 2, self.create_line_edit_widget(account_name))
        self.ui.password_list.setCellWidget(row, 3, self.create_dropdown_edit(category))
        self.ui.password_list.setCellWidget(row, 4, self.create_line_edit_widget(password))
        self.ui.password_list.setCellWidget(row, 5, self.create_button_widget(entry_id, category))

    def submit_password_edit(self, entry_id, category):
        self.passwords = user_controller.update_user_password(self.user_id, entry_id, self.edit_fields[0].text(),
                                                              self.edit_fields[1].text(), self.edit_fields[2].text(),
                                                              self.edit_fields[3].currentText(), self.edit_fields[4].text())
        self.update_password_list_widget()


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
        self.categories = user_controller.get_user_categories(self.user_id)
        self.ui.p_category_dropdown.clear()
        self.ui.p_category_dropdown.addItem("-")
        for category in self.categories:
            self.ui.p_category_dropdown.addItem(category[1])
        self.reset_menu_buttons()
        self.ui.menu_password_button.setStyleSheet(self.pressed_button_style1)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ROOT_DIR, "src", "gui", "icons", "password_icon1.png")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.menu_password_button.setIcon(icon)
        self.ui.stacked_widget.setCurrentWidget(self.ui.password_page)
        self.resize_password_page()

    """
    Switch current 'self.stacked_widget' page to group page.
    """
    def switch_to_group_page(self):
        self.update_category_list()
        self.reset_menu_buttons()
        self.ui.menu_group_button.setStyleSheet(self.pressed_button_style1)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ROOT_DIR, "src", "gui", "icons", "group_icon1.png")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.menu_group_button.setIcon(icon)
        self.ui.stacked_widget.setCurrentWidget(self.ui.group_page)
        self.resize_group_page()

    """
    Switch current 'self.stacked_widget' page to security page.
    """
    def switch_to_security_page(self):
        self.ui.import_error_label.hide()
        self.reset_menu_buttons()
        self.ui.menu_security_button.setStyleSheet(self.pressed_button_style1)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ROOT_DIR, "src", "gui", "icons", "security_icon1.png")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.menu_security_button.setIcon(icon)
        self.ui.stacked_widget.setCurrentWidget(self.ui.security_page)
        self.resize_security_page()

    """
    Switch current 'self.stacked_widget' page to profile page.
    """
    def switch_to_profile_page(self):
        self.reset_menu_buttons()
        self.ui.menu_profile_button.setStyleSheet(self.pressed_button_style2)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ROOT_DIR, "src", "gui", "icons", "profile_icon2.png")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.menu_profile_button.setIcon(icon)
        self.ui.stacked_widget.setCurrentWidget(self.ui.profile_page)

    """
    Switch current 'self.stacked_widget' page to settings page.
    """
    def switch_to_settings_page(self):
        self.reset_menu_buttons()
        self.ui.menu_settings_button.setStyleSheet(self.pressed_button_style2)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(ROOT_DIR, "src", "gui", "icons", "settings_icon2.png")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        category = self.ui.p_category_dropdown.currentText()
        response = user_controller.add_password(self.user_id, domain, password, account_name, url, category)
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
        print(self.passwords)

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
    Update the list of password categories.
    """
    def update_category_list(self):
        self.ui.category_list.clear()
        self.category_widgets.clear()
        self.categories = user_controller.get_user_categories(self.user_id)
        for category in self.categories:
            passwords = list(filter(lambda x: x[4] == category[1], self.passwords))
            self.append_category_list(category[1], passwords, category[2], category[0])

    """
    Add password category to category list.
    """
    def append_category_list(self, category_name, passwords, color, cat_id):
        item = QtWidgets.QListWidgetItem()
        widget = QtWidgets.QWidget()
        category_widget = Ui_category_widget()
        category_widget.setupUi(widget)
        category_widget.category_name.setText("⏵ " + category_name)
        category_widget.category_name.clicked.connect(lambda: self.toggle_category_table(category_widget, item))
        category_widget.category_table.setHorizontalHeaderItem(0, QTableWidgetItem("Domain"))
        category_widget.category_table.setHorizontalHeaderItem(1, QTableWidgetItem("URL"))
        category_widget.category_table.setHorizontalHeaderItem(2, QTableWidgetItem("Account name"))
        category_widget.category_table.setHorizontalHeaderItem(3, QTableWidgetItem("Password"))
        category_widget.category_table.setRowCount(0)
        for i, password in enumerate(passwords):
            domain, account_name, url, _password, name, id, entry_id = password
            row_position = category_widget.category_table.rowCount()
            category_widget.category_table.insertRow(row_position)
            category_widget.category_table.setCellWidget(row_position, 0, self.create_label_widget(domain))
            category_widget.category_table.setCellWidget(row_position, 1, self.create_label_widget(url))
            category_widget.category_table.setCellWidget(row_position, 2, self.create_label_widget(account_name))
            category_widget.category_table.setCellWidget(row_position, 3, self.create_password_widget(_password, color))
        category_widget.frame_2.hide()
        category_widget.category_name.setStyleSheet("QPushButton {color:" + color + ";font: bold 20px;border: 0;"
                                                    "background: none;box-shadow: none;border-radius: 5px;"
                                                    "text-align:left;} QPushButton:hover {text-decoration: underline;}")
        category_widget.color_button.setStyleSheet("QPushButton {border: 0;background: none;box-shadow: none;"
                                                   "border-radius: 2px;background-color:" + color + ";} "
                                                   "QPushButton:hover {border: 3px solid;}")
        category_widget.color_button.clicked.connect(lambda: self.pick_color(cat_id))
        item.setSizeHint(category_widget.frame.sizeHint())
        self.ui.category_list.addItem(item)
        self.ui.category_list.setItemWidget(item, widget)
        self.category_widgets.append(category_widget)

    """
    Create pop-up window for color picker. Save user's category color.
    """
    def pick_color(self, cat_id):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            user_controller.change_category_color(cat_id, color.name())
            self.update_category_list()

    """
    Toggle the visibility of the category password table.
    """
    def toggle_category_table(self, category_widget, item):
        if category_widget.frame_2.isHidden():
            category_widget.frame_2.show()
            item.setSizeHint(category_widget.frame.sizeHint())
            category_widget.category_name.setText("▼ " + category_widget.category_name.text()[2:])
        else:
            category_widget.frame_2.hide()
            item.setSizeHint(category_widget.frame.sizeHint())
            category_widget.category_name.setText("⏵ " + category_widget.category_name.text()[2:])

    """
    Add a new category to the user's profile.
    """
    def add_new_category(self):
        category = self.ui.new_category_field.text()
        response = user_controller.add_category(self.user_id, category)
        if response == 1:
            self.ui.new_category_field.setStyleSheet("QLineEdit {font: 18px;background-color:#ffffff}")
            self.update_category_list()
        else:
            self.ui.new_category_field.setStyleSheet("QLineEdit {font: 18px;background-color:#fa9487}")

    """
    Adjust dimensions of password tables on resize.
    """
    def resizeEvent(self):
        if self.ui.stacked_widget.currentWidget().objectName() == "password_page":
            self.resize_password_page()
        elif self.ui.stacked_widget.currentWidget().objectName() == "group_page":
            self.resize_group_page()
        elif self.ui.stacked_widget.currentWidget().objectName() == "security_page":
            self.resize_security_page()

    """
    Resize the password page's password list.
    """
    def resize_password_page(self):
        width = self.ui.frame_2.width() - 40
        for i in range(6):
            self.ui.password_list.setColumnWidth(i, int(width / 6))

    """
    Resize the group page's password list.
    """
    def resize_group_page(self):
        width = self.ui.frame.width() - 75
        for widget in self.category_widgets:
            for i in range(4):
                widget.category_table.setColumnWidth(i, int(width / 4))

    def resize_security_page(self):
        width = self.ui.frame_10.width() - 60
        for i in range(6):
            self.ui.security_table.setColumnWidth(i, int(width / 6))

    def run_security_check(self):
        self.ui.security_table.setRowCount(0)
        for password in self.passwords:
            domain, account_name, url, _password, category_name, color, entry_id = password
            score = measure_password_strength(_password, domain, account_name)
            if score <= 2:
                if score == 0:
                    score_label = "Extremely weak"
                    score_color = "red"
                elif score == 1:
                    score_label = "Weak"
                    score_color = "orange"
                else:
                    score_label = "Somewhat weak"
                    score_color = "yellow"
                row_position = self.ui.security_table.rowCount()
                self.ui.security_table.insertRow(row_position)
                self.ui.security_table.setCellWidget(row_position, 0, self.create_label_widget(domain))
                self.ui.security_table.setCellWidget(row_position, 1, self.create_label_widget(url))
                self.ui.security_table.setCellWidget(row_position, 2, self.create_label_widget(account_name))
                self.ui.security_table.setCellWidget(row_position, 3, self.create_label_widget(category_name))
                self.ui.security_table.setCellWidget(row_position, 4, self.create_label_widget(_password, color))
                self.ui.security_table.setCellWidget(row_position, 5, self.create_label_widget(score_label, score_color))

    """
    Show the main window.
    """
    def show(self):
        self.main_win.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow(24)
    main_win.show()
    sys.exit(app.exec_())
