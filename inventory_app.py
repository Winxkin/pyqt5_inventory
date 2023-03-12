import os 
import time
import argparse
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import _http_client
from firebase_admin import storage, firestore
from firebase_admin import db
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
import resource_rc

def connect_to_firebase():
    cred = credentials.Certificate("./inventory-firebase.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL' : 'https://inventory-16459-default-rtdb.asia-southeast1.firebasedatabase.app/',
        'storageBucket' : 'inventory-16459.appspot.com'
    })
    print("connecting to firebase server...")
    return

#***********************************************************************
#class gui design for application
#***********************************************************************
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1056, 811)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.logo_HCMUTE = QtWidgets.QLabel(self.centralwidget)
        self.logo_HCMUTE.setGeometry(QtCore.QRect(250, 10, 451, 111))
        self.logo_HCMUTE.setText("")
        self.logo_HCMUTE.setPixmap(QtGui.QPixmap(":/newPrefix/Logo.png"))
        self.logo_HCMUTE.setObjectName("logo_HCMUTE")
        self.group_img = QtWidgets.QGroupBox(self.centralwidget)
        self.group_img.setGeometry(QtCore.QRect(160, 260, 651, 491))
        font = QtGui.QFont()
        font.setFamily("URW Bookman [urw]")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.group_img.setFont(font)
        self.group_img.setObjectName("group_img")
        self.result_img = QtWidgets.QLabel(self.group_img)
        self.result_img.setGeometry(QtCore.QRect(110, 40, 448, 448))
        self.result_img.setObjectName("result_img")
        self.group_info = QtWidgets.QGroupBox(self.centralwidget)
        self.group_info.setGeometry(QtCore.QRect(160, 120, 651, 141))
        font = QtGui.QFont()
        font.setFamily("URW Bookman [UKWN]")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.group_info.setFont(font)
        self.group_info.setObjectName("group_info")
        self.OOS_lable = QtWidgets.QLabel(self.group_info)
        self.OOS_lable.setGeometry(QtCore.QRect(40, 30, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.OOS_lable.setFont(font)
        self.OOS_lable.setObjectName("OOS_lable")
        self.IS_lable = QtWidgets.QLabel(self.group_info)
        self.IS_lable.setGeometry(QtCore.QRect(270, 40, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.IS_lable.setFont(font)
        self.IS_lable.setObjectName("IS_lable")
        self.avalible_lable = QtWidgets.QLabel(self.group_info)
        self.avalible_lable.setGeometry(QtCore.QRect(440, 30, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.avalible_lable.setFont(font)
        self.avalible_lable.setObjectName("avalible_lable")
        self.OOS_index = QtWidgets.QLabel(self.group_info)
        self.OOS_index.setGeometry(QtCore.QRect(40, 80, 111, 41))
        self.OOS_index.setObjectName("OOS_index")
        self.IS_index = QtWidgets.QLabel(self.group_info)
        self.IS_index.setGeometry(QtCore.QRect(260, 80, 111, 41))
        self.IS_index.setObjectName("IS_index")
        self.avalible_index = QtWidgets.QProgressBar(self.group_info)
        self.avalible_index.setGeometry(QtCore.QRect(460, 90, 118, 23))
        self.avalible_index.setProperty("value", 24)
        self.avalible_index.setObjectName("avalible_index")
        self.TimeBox = QtWidgets.QGroupBox(self.centralwidget)
        self.TimeBox.setGeometry(QtCore.QRect(820, 140, 201, 121))
        font = QtGui.QFont()
        font.setFamily("URW Bookman")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.TimeBox.setFont(font)
        self.TimeBox.setObjectName("TimeBox")
        self.time = QtWidgets.QLabel(self.TimeBox)
        self.time.setGeometry(QtCore.QRect(10, 40, 210, 71))
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.time.setFont(font)
        self.time.setObjectName("time")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1056, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    #******************************************************
    #my code here
    #******************************************************
    def update_data(self, OOS, IS, avaliable, img_name,current_time):
        self.OOS_index.setText(str(OOS))
        self.IS_index.setText(str(IS))
        self.time.setText(str(current_time))
        self.avalible_index.setProperty("value",float(avaliable)*100)
        #set image
        pixmap = QtGui.QPixmap(img_name)
        self.h = self.result_img.width() - 10
        self.w = self.result_img.height() - 10
        self.result_img.setPixmap(pixmap.scaled(QtCore.QSize(self.w,self.h),
                                QtCore.Qt.KeepAspectRatio))
        return

    def download_image(self,img_name):
        self.bucket = storage.bucket()
        self.blob = self.bucket.blob(img_name)
        time.sleep(2)   #waitting for image update
        self.blob.download_to_filename(img_name)
        return

    def firebase_realtime_callback(self,event):
        self.json_data = event.data['Shelf']
        print("Receiving realtime data from firebase...")
        print(self.json_data)
        self.OOS = self.json_data['OOS']
        self.In_stock = self.json_data['In-stock']
        self.avaliable = self.json_data['In-stock_avalivle']
        self.img_name = self.json_data['img_output']
        self._time = self.json_data['time']
        self.download_image(self.img_name)
        self.update_data(self.OOS,self.In_stock,self.avaliable,self.img_name,self._time)
        print("firebase_realtime_callback end !")
        return
    
    def firebase_realtime(self):
        print("listen from realtime firebase...")
        self.ref = db.reference('/').listen(self.firebase_realtime_callback)
        return

    #******************************************************
    #End my code 
    #******************************************************

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.group_img.setTitle(_translate("MainWindow", "shelf"))
        self.result_img.setText(_translate("MainWindow", "Image"))
        self.group_info.setTitle(_translate("MainWindow", "Index"))
        self.OOS_lable.setText(_translate("MainWindow", "Out of stock"))
        self.IS_lable.setText(_translate("MainWindow", "In stock"))
        self.avalible_lable.setText(_translate("MainWindow", "Available in shelf"))
        self.OOS_index.setText(_translate("MainWindow", "0"))
        self.IS_index.setText(_translate("MainWindow", "0"))
        self.TimeBox.setTitle(_translate("MainWindow", "Time"))
        self.time.setText(_translate("MainWindow", "time"))



#*************************
#main function begin here
#*************************
def main():
    connect_to_firebase()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.firebase_realtime()
    MainWindow.show()
    sys.exit(app.exec_())
    return
    

if __name__ == "__main__":
    main()

