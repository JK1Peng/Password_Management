"""
File: src/gui/PasswordWidget.py

Author: Aaron Kersten, amk9398@rit.edu

Description: A row in the display table containing each of the user's passwords.
"""

from PyQt5.QtWidgets import QWidget
from src.gui.ui.ui_password_list_node import Ui_Form as Ui_password_list_node
from src.database.user_controller import remove_password
import pyperclip as pc
from PyQt5 import QtGui


class PasswordWidget:
    def __init__(self, width, user_id, num, domain, account_name, url, password):
        self.user_id = user_id
        self.width = width
        self.num = num
        self.domain = domain
        self.account_name = account_name
        self.url = url
        self.password = password
        self.list_node = QWidget()
        self.widget = Ui_password_list_node()
        self.widget.setupUi(self.list_node)

        copy_icon = QtGui.QIcon()
        copy_icon.addPixmap(QtGui.QPixmap("../icons/copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.widget.copy_button.setIcon(copy_icon)

        # self.fix_node_format()

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

    def fix_node_format(self):
        label_width = (self.width - 119) / 4
        if label_width < 0:
            label_width = 135
        self.widget.frame_4.setFixedWidth(label_width)
        self.widget.frame_6.setFixedWidth(label_width)
        self.widget.frame_7.setFixedWidth(label_width)
        self.widget.frame_8.setFixedWidth(label_width)
