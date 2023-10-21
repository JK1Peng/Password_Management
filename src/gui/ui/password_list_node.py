# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/gui/ui_password_list_node.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_password_list_node(object):


    def setupUi(self, password_list_node, num, domain, _password):
        password_list_node.setObjectName("password_list_node")
        password_list_node.resize(698, 54)
        password_list_node.setMinimumSize(QtCore.QSize(478, 54))
        password_list_node.setMaximumSize(QtCore.QSize(16777215, 54))
        password_list_node.setStyleSheet("background-color:#FDF8F5")
        self.verticalLayout = QtWidgets.QVBoxLayout(password_list_node)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.password_list_frame = QtWidgets.QFrame(password_list_node)
        self.password_list_frame.setStyleSheet("QFrame {\n"
"    border: 1px solid;\n"
"    border-color:#4F4846;\n"
"\n"
"}")
        self.password_list_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.password_list_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.password_list_frame.setObjectName("password_list_frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.password_list_frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.num_frame = QtWidgets.QFrame(self.password_list_frame)
        self.num_frame.setMinimumSize(QtCore.QSize(50, 0))
        self.num_frame.setMaximumSize(QtCore.QSize(50, 16777215))
        self.num_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.num_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.num_frame.setObjectName("num_frame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.num_frame)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.num_label = QtWidgets.QLabel(self.num_frame)
        self.num_label.setStyleSheet("QLabel {\n"
"    font: bold 12px;\n"
"    color:#4F4846;\n"
"}")
        self.num_label.setAlignment(QtCore.Qt.AlignCenter)
        self.num_label.setObjectName("num_label")
        self.horizontalLayout_4.addWidget(self.num_label)
        self.horizontalLayout.addWidget(self.num_frame)
        self.domain_name_frame = QtWidgets.QFrame(self.password_list_frame)
        self.domain_name_frame.setStyleSheet("")
        self.domain_name_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.domain_name_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.domain_name_frame.setObjectName("domain_name_frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.domain_name_frame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.domain_name_label = QtWidgets.QLabel(self.domain_name_frame)
        self.domain_name_label.setStyleSheet("QLabel {\n"
"    font: bold 12px;\n"
"    color:#4F4846;\n"
"}")
        self.domain_name_label.setObjectName("domain_name_label")
        self.horizontalLayout_3.addWidget(self.domain_name_label)
        self.horizontalLayout.addWidget(self.domain_name_frame)
        self.password_frame = QtWidgets.QFrame(self.password_list_frame)
        self.password_frame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.password_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.password_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.password_frame.setObjectName("password_frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.password_frame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.password_label = QtWidgets.QLabel(self.password_frame)
        self.password_label.setStyleSheet("QLabel {\n"
"    font: bold 12px;\n"
"    color:#4F4846;\n"
"}")
        self.password_label.setObjectName("password_label")
        self.horizontalLayout_2.addWidget(self.password_label)
        self.frame = QtWidgets.QFrame(self.password_frame)
        self.frame.setMinimumSize(QtCore.QSize(50, 0))
        self.frame.setMaximumSize(QtCore.QSize(50, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton.setStyleSheet("QPushButton {\n"
"    color:#FDF8F5;\n"
"    font: bold 15px; border: 0;\n"
" background: none;\n"
" box-shadow: none;\n"
" border-radius: 2px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:#E8CEBF\n"
"}\n"
"")
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("src/gui\\icons/copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_6.addWidget(self.pushButton)
        self.horizontalLayout_2.addWidget(self.frame)
        self.horizontalLayout.addWidget(self.password_frame)
        self.option_button_frame = QtWidgets.QFrame(self.password_list_frame)
        self.option_button_frame.setMinimumSize(QtCore.QSize(50, 0))
        self.option_button_frame.setMaximumSize(QtCore.QSize(50, 16777215))
        self.option_button_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.option_button_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.option_button_frame.setObjectName("option_button_frame")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.option_button_frame)
        self.horizontalLayout_5.setContentsMargins(2, -1, 2, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.option_button = QtWidgets.QPushButton(self.option_button_frame)
        self.option_button.setMinimumSize(QtCore.QSize(30, 30))
        self.option_button.setMaximumSize(QtCore.QSize(30, 30))
        self.option_button.setStyleSheet("QPushButton {\n"
"    color:#4F4846;\n"
"    font: bold 15px; border: 0;\n"
" background: none;\n"
" box-shadow: none;\n"
" border-radius: 2px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:#E8CEBF\n"
"}\n"
"")
        self.option_button.setObjectName("option_button")
        self.horizontalLayout_5.addWidget(self.option_button)
        self.horizontalLayout.addWidget(self.option_button_frame)
        self.verticalLayout.addWidget(self.password_list_frame)

        self.retranslateUi(password_list_node)
        QtCore.QMetaObject.connectSlotsByName(password_list_node)

    def retranslateUi(self, password_list_node):
        _translate = QtCore.QCoreApplication.translate
        password_list_node.setWindowTitle(_translate("password_list_node", "Form"))
        self.num_label.setText(_translate("password_list_node", self.num))
        self.domain_name_label.setText(_translate("password_list_node", self.domain))
        self.password_label.setText(_translate("password_list_node", self._password))
        self.option_button.setText(_translate("password_list_node", "X"))

    def remove(self):
        self.list_node.hide()
        database.user_controller.remove_password(self.user_id, self.domain, self.account_name)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    password_list_node = QtWidgets.QWidget()
    ui = Ui_password_list_node()
    ui.setupUi(password_list_node)
    password_list_node.show()
    sys.exit(app.exec_())
