# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/gui/qt_designer/ui_delete_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_delete_widget(object):
    def setupUi(self, delete_widget):
        delete_widget.setObjectName("delete_widget")
        delete_widget.resize(665, 275)
        delete_widget.setStyleSheet("QFrame {\n"
"background-color:#FDF8F5;\n"
"}\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(delete_widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_9 = QtWidgets.QFrame(delete_widget)
        self.frame_9.setMinimumSize(QtCore.QSize(0, 45))
        self.frame_9.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_9)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.x_button = QtWidgets.QPushButton(self.frame_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.x_button.sizePolicy().hasHeightForWidth())
        self.x_button.setSizePolicy(sizePolicy)
        self.x_button.setMinimumSize(QtCore.QSize(0, 0))
        self.x_button.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.x_button.setStyleSheet("QPushButton {\n"
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
        self.x_button.setObjectName("x_button")
        self.horizontalLayout.addWidget(self.x_button)
        self.verticalLayout.addWidget(self.frame_9)

        self.retranslateUi(delete_widget)
        QtCore.QMetaObject.connectSlotsByName(delete_widget)

    def retranslateUi(self, delete_widget):
        _translate = QtCore.QCoreApplication.translate
        delete_widget.setWindowTitle(_translate("delete_widget", "Form"))
        self.x_button.setText(_translate("delete_widget", "X"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    delete_widget = QtWidgets.QWidget()
    ui = Ui_delete_widget()
    ui.setupUi(delete_widget)
    delete_widget.show()
    sys.exit(app.exec_())
