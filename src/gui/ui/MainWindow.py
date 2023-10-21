import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from src.gui.ui.ui_main_window import Ui_main_window
from src.gui.ui.password_list_node import Ui_password_list_node
from PasswordWidget import PasswordWidget
import src.database.user_controller as user_controller


class MainWindow:
    user_id = 1
    passwords = []

    default_button_style = "QPushButton {color:#DDAF94;font: bold 20px;border: 0;text-align:left;" \
                           "background: none;box-shadow:none;border-radius: 0px;background-color:#FDF8F5;}" \
                           "QPushButton:hover {background-color:#E8CEBF}"

    pressed_button_style = "QPushButton {color:#FDF8F5;font: bold 20px;border: 0;text-align:left;" \
                           "background: none;box-shadow:none;border-radius: 0px;background-color:#DDAF94;}" \
                           "QPushButton:hover {background-color:#E8CEBF}"

    def __init__(self, user_id):
        self.user_id = user_id
        self.main_win = QMainWindow()
        self.ui = Ui_main_window()
        self.ui.setupUi(self.main_win)

        # init ui
        self.ui.new_password_frame.hide()
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("C:\Python\Python39\password_manager\src\gui\icons\magnifying_glass.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.ui.search_button.setIcon(icon1)

        # button actions
        self.ui.menu_password_button.clicked.connect(self.switch_to_password_page)
        self.ui.menu_group_button.clicked.connect(self.switch_to_group_page)
        self.ui.new_password_button.clicked.connect(self.new_password)
        self.ui.add_password_button.clicked.connect(self.add_password)
        self.ui.search_button.clicked.connect(self.search_passwords)

        # setup
        self.switch_to_password_page()
        self.passwords = user_controller.get_user_passwords(self.user_id)
        self.update_password_list_widget()

        print(self.passwords)

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
        # list_node = QWidget()
        # x = Ui_password_list_node()
        # x.setupUi(list_node, self.user_id, num, domain, account_name, url, _password)
        # item.setSizeHint(list_node.sizeHint())
        # self.ui.password_list.addItem(item)
        # self.ui.password_list.setItemWidget(item, list_node)
        password_widget = PasswordWidget(self.user_id, num, domain, account_name, url, _password)
        item.setSizeHint(password_widget.list_node.sizeHint())
        self.ui.password_list.addItem(item)
        self.ui.password_list.setItemWidget(item, password_widget.list_node)

    def switch_to_password_page(self):
        self.ui.menu_password_button.setStyleSheet(self.pressed_button_style)
        self.ui.menu_group_button.setStyleSheet(self.default_button_style)
        self.ui.stacked_widget.setCurrentWidget(self.ui.password_page)

    def switch_to_group_page(self):
        self.ui.menu_password_button.setStyleSheet(self.default_button_style)
        self.ui.menu_group_button.setStyleSheet(self.pressed_button_style)
        self.ui.stacked_widget.setCurrentWidget(self.ui.group_page)

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
            self.passwords = user_controller.get_user_passwords(self.user_id)
            self.update_password_list_widget()

    def search_passwords(self):
        query = self.ui.search_field.text()
        self.passwords = user_controller.get_user_passwords(self.user_id, query)
        self.update_password_list_widget()

    def show(self):
        self.main_win.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow(2)
    main_win.show()
    sys.exit(app.exec_())
