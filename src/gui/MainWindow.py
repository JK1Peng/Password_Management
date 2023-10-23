import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtGui
from src.gui.ui.ui_main_window import Ui_main_window
from PasswordWidget import PasswordWidget
import src.database.user_controller as user_controller


class MainWindow:
    user_id = 1
    passwords = []

    default_button_style1 = "QPushButton {color:#FDF8F5;font: bold 20px;border: 0;text-align:left;" \
                            "background: none;box-shadow:none;border-radius: 0px;background-color:#DDAF94;" \
                            "padding-left:20px;}" \
                            "QPushButton:hover {background-color:#E8CEBF}"

    pressed_button_style1 = "QPushButton {color:#DDAF94;font: bold 20px;border: 0;text-align:left;" \
                            "background: none;box-shadow:none;border-radius: 0px;background-color:#FDF8F5;" \
                            "padding-left:20px}" \
                            "QPushButton:hover {background-color:#E8CEBF}"

    default_button_style2 = "QPushButton {color:#FDF8F5;font: bold 20px;border: 0;text-align:center;" \
                            "background: none;box-shadow:none;border-radius: 0px;background-color:#DDAF94;}" \
                            "QPushButton:hover {background-color:#E8CEBF}"

    pressed_button_style2 = "QPushButton {color:#DDAF94;font: bold 20px;border: 0;text-align:center;" \
                            "background: none;box-shadow:none;border-radius: 0px;background-color:#FDF8F5;}" \
                            "QPushButton:hover {background-color:#E8CEBF}"

    def __init__(self, user_id):
        self.user_id = user_id
        self.main_win = QMainWindow()
        self.ui = Ui_main_window()
        self.ui.setupUi(self.main_win)

        # init ui
        self.ui.new_password_frame.hide()
        self.ui.add_error_frame.hide()
        icon1 = QtGui.QIcon()
        group_icon = QtGui.QIcon()
        profile_icon = QtGui.QIcon()
        password_icon = QtGui.QIcon()
        settings_icon = QtGui.QIcon()
        security_icon = QtGui.QIcon()
        menu_icon = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../icons/magnifying_glass.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        group_icon.addPixmap(QtGui.QPixmap("../icons/group_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        profile_icon.addPixmap(QtGui.QPixmap("../icons/profile_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        password_icon.addPixmap(QtGui.QPixmap("../icons/password_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        settings_icon.addPixmap(QtGui.QPixmap("../icons/settings_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        security_icon.addPixmap(QtGui.QPixmap("../icons/security_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        menu_icon.addPixmap(QtGui.QPixmap("../icons/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.search_button.setIcon(icon1)
        self.ui.menu_password_button.setIcon(password_icon)
        self.ui.menu_group_button.setIcon(group_icon)
        self.ui.menu_security_button.setIcon(security_icon)
        self.ui.menu_profile_button.setIcon(profile_icon)
        self.ui.menu_settings_button.setIcon(settings_icon)
        self.ui.menu_toggle_button.setIcon(menu_icon)

        # button actions
        self.ui.menu_password_button.clicked.connect(self.switch_to_password_page)
        self.ui.menu_group_button.clicked.connect(self.switch_to_group_page)
        self.ui.menu_security_button.clicked.connect(self.switch_to_security_page)
        self.ui.menu_profile_button.clicked.connect(self.switch_to_profile_page)
        self.ui.menu_settings_button.clicked.connect(self.switch_to_settings_page)
        self.ui.new_password_button.clicked.connect(self.new_password)
        self.ui.add_password_button.clicked.connect(self.add_password)
        self.ui.search_button.clicked.connect(self.search_passwords)

        # setup
        self.switch_to_password_page()
        self.passwords = user_controller.get_user_passwords(self.user_id)
        self.update_password_list_widget()

    def update(self, message, *params):
        if message == "switch page":
            new_page = params[0]
            if new_page == "password":
                self.switch_to_password_page()
            elif new_page == "group":
                self.switch_to_group_page()
        elif message == "add password":
            pass
        elif message == "remove password":
            pass

    def update_password_list_widget(self):
        self.ui.password_list.clear()
        for i, password in enumerate(self.passwords):
            domain = password[0]
            account_name = password[1]
            url = password[2]
            _password = password[3]
            self.append_password_list_widget(str(i+1), domain, account_name, url, _password)

    def append_password_list_widget(self, num, domain, account_name, url, _password):
        item = QListWidgetItem()
        password_widget = PasswordWidget(self.user_id, num, domain, account_name, url, _password)
        item.setSizeHint(password_widget.list_node.sizeHint())
        self.ui.password_list.addItem(item)
        self.ui.password_list.setItemWidget(item, password_widget.list_node)

    def reset_menu_buttons(self):
        self.ui.menu_group_button.setStyleSheet(self.default_button_style1)
        self.ui.menu_password_button.setStyleSheet(self.default_button_style1)
        self.ui.menu_security_button.setStyleSheet(self.default_button_style1)
        self.ui.menu_profile_button.setStyleSheet(self.default_button_style2)
        self.ui.menu_settings_button.setStyleSheet(self.default_button_style2)

    def switch_to_password_page(self):
        self.reset_menu_buttons()
        self.ui.menu_password_button.setStyleSheet(self.pressed_button_style1)
        self.ui.stacked_widget.setCurrentWidget(self.ui.password_page)

    def switch_to_group_page(self):
        self.reset_menu_buttons()
        self.ui.menu_group_button.setStyleSheet(self.pressed_button_style1)
        self.ui.stacked_widget.setCurrentWidget(self.ui.group_page)

    def switch_to_security_page(self):
        self.reset_menu_buttons()
        self.ui.menu_security_button.setStyleSheet(self.pressed_button_style1)
        self.ui.stacked_widget.setCurrentWidget(self.ui.security_page)

    def switch_to_profile_page(self):
        self.reset_menu_buttons()
        self.ui.menu_profile_button.setStyleSheet(self.pressed_button_style2)
        self.ui.stacked_widget.setCurrentWidget(self.ui.profile_page)

    def switch_to_settings_page(self):
        self.reset_menu_buttons()
        self.ui.menu_settings_button.setStyleSheet(self.pressed_button_style2)
        self.ui.stacked_widget.setCurrentWidget(self.ui.settings_page)

    def new_password(self):
        if self.ui.new_password_frame.isHidden():
            self.ui.new_password_frame.show()
            self.ui.new_password_button.setText("New ▼")
        else:
            self.ui.new_password_frame.hide()
            self.ui.new_password_button.setText("New ▲")

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

    def search_passwords(self):
        query = self.ui.search_field.text().lower()
        response = user_controller.get_user_passwords(self.user_id, query)
        if response == 0:
            pass
        else:
            self.passwords = response
        self.update_password_list_widget()

    def show(self):
        self.main_win.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow(2)
    main_win.show()
    sys.exit(app.exec_())
