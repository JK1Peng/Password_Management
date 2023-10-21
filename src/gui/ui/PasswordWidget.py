from PyQt5.QtWidgets import QWidget
from src.gui.ui.ui_password_list_node import Ui_Form as Ui_password_list_node
from src.database.user_controller import remove_password
import pyperclip as pc


class PasswordWidget:
    def __init__(self, user_id, num, domain, account_name, url, password):
        self.user_id = user_id
        self.num = num
        self.domain = domain
        self.account_name = account_name
        self.url = url
        self.password = password
        self.list_node = QWidget()
        self.widget = Ui_password_list_node()
        self.widget.setupUi(self.list_node)

        self.widget.label.setText(self.num)
        self.widget.label_2.setText(self.domain)
        self.widget.label_3.setText(self.url)
        self.widget.label_4.setText(self.account_name)
        self.widget.label_5.setText(self.password)

        self.widget.x_button.clicked.connect(lambda: self.remove_node())
        self.widget.copy_button.clicked.connect(lambda: self.copy_password())

    def remove_node(self):
        self.list_node.hide()
        remove_password(self.user_id, self.domain, self.account_name)

    def copy_password(self):
        pc.copy(self.widget.label_5.text())
