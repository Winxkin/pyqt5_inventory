# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inventory.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_inventory_wd(object):
    def setupUi(self, inventory_wd):
        inventory_wd.setObjectName("inventory_wd")
        inventory_wd.resize(576, 423)
        self.centralwidget = QtWidgets.QWidget(inventory_wd)
        self.centralwidget.setObjectName("centralwidget")
        self.date_inventory_cb = QtWidgets.QComboBox(self.centralwidget)
        self.date_inventory_cb.setGeometry(QtCore.QRect(140, 340, 211, 31))
        self.date_inventory_cb.setObjectName("date_inventory_cb")
        self.search_btn = QtWidgets.QPushButton(self.centralwidget)
        self.search_btn.setGeometry(QtCore.QRect(360, 310, 71, 61))
        self.search_btn.setText("")
        self.search_btn.setObjectName("search_btn")
        self.Analysis_logo = QtWidgets.QLabel(self.centralwidget)
        self.Analysis_logo.setGeometry(QtCore.QRect(30, 10, 521, 281))
        self.Analysis_logo.setText("")
        self.Analysis_logo.setObjectName("Analysis_logo")
        inventory_wd.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(inventory_wd)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 576, 20))
        self.menubar.setObjectName("menubar")
        inventory_wd.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(inventory_wd)
        self.statusbar.setObjectName("statusbar")
        inventory_wd.setStatusBar(self.statusbar)

        self.retranslateUi(inventory_wd)
        QtCore.QMetaObject.connectSlotsByName(inventory_wd)

    def retranslateUi(self, inventory_wd):
        _translate = QtCore.QCoreApplication.translate
        inventory_wd.setWindowTitle(_translate("inventory_wd", "Inventory Analysis"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    inventory_wd = QtWidgets.QMainWindow()
    ui = Ui_inventory_wd()
    ui.setupUi(inventory_wd)
    inventory_wd.show()
    sys.exit(app.exec_())
