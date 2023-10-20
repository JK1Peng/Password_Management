import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QWidget
from src.gui.ui.ui_main_window import Ui_main_window
from src.gui.ui.password_list_node import Ui_password_list_node
import src.database.user_controller as user_controller


class MainWindow:
    user_id = 1
    passwords = []

    default_button_style = "QPushButton {color:#DDAF94;font: bold 20px;border: 0;background: none;box-shadow: " \
                           "none;border-radius: 0px;background-color:#FDF8F5;}QPushButton:hover " \
                           "{background-color:#E8CEBF}"

    pressed_button_style = "QPushButton {color:#FDF8F5;font: bold 20px;border: 0;background: none;box-shadow: " \
                           "none;border-radius: 0px;background-color:#DDAF94;}QPushButton:hover " \
                           "{background-color:#E8CEBF}"

    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_main_window()
        self.ui.setupUi(self.main_win)

        self.ui.menu_password_button.clicked.connect(self.switch_to_password_page)
        self.ui.menu_group_button.clicked.connect(self.switch_to_group_page)

        self.switch_to_password_page()
        self.user_id = user_controller.login("admin", "password")
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
            for j in range(20):
                self.append_password_list_widget(str(j+1), domain, _password)

    def append_password_list_widget(self, num, domain, _password):
        item = QListWidgetItem()
        list_node = QWidget()
        x = Ui_password_list_node()
        x.setupUi(list_node, num, domain, _password)
        item.setSizeHint(list_node.sizeHint())

        self.ui.password_list.addItem(item)
        self.ui.password_list.setItemWidget(item, list_node)

    def switch_to_password_page(self):
        self.ui.menu_password_button.setStyleSheet(self.pressed_button_style)
        self.ui.menu_group_button.setStyleSheet(self.default_button_style)
        self.ui.stacked_widget.setCurrentWidget(self.ui.password_page)

    def switch_to_group_page(self):
        self.ui.menu_password_button.setStyleSheet(self.default_button_style)
        self.ui.menu_group_button.setStyleSheet(self.pressed_button_style)
        self.ui.stacked_widget.setCurrentWidget(self.ui.group_page)

    def show(self):
        self.main_win.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    ui = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
