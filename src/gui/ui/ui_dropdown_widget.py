# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/gui/qt_designer/ui_dropdown_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dropdown(object):
    def setupUi(self, dropdown):
        dropdown.setObjectName("dropdown")
        dropdown.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(dropdown)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox = QtWidgets.QComboBox(dropdown)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout.addWidget(self.comboBox)

        self.retranslateUi(dropdown)
        QtCore.QMetaObject.connectSlotsByName(dropdown)

    def retranslateUi(self, dropdown):
        _translate = QtCore.QCoreApplication.translate
        dropdown.setWindowTitle(_translate("dropdown", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dropdown = QtWidgets.QWidget()
    ui = Ui_dropdown()
    ui.setupUi(dropdown)
    dropdown.show()
    sys.exit(app.exec_())