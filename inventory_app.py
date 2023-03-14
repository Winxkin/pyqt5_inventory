import os 
import time
import argparse
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import _http_client
from firebase_admin import storage, firestore
from firebase_admin import db
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal ,QObject
import csv
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as Navi
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd
import sip

#define value here
matplotlib.use('Qt5Agg')
analysis_dir = os.getcwd() + '/analysis/'
image_dir = os.getcwd() + '/image/'

#*************************
# connecting to firebase 
#*************************
def connect_to_firebase():
    cred = credentials.Certificate("./inventory-firebase.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL' : 'https://inventory-16459-default-rtdb.asia-southeast1.firebasedatabase.app/',
        'storageBucket' : 'inventory-16459.appspot.com'
    })
    print("connecting to firebase server...")
    return

# replace `object` with `QObject` to fix
class Signaller(object):
    signal = pyqtSignal(str)

    def trigger(self, msg):
        print("emitting: {}".format(msg))
        self.signal.emit(msg)


#***********************************************************************
#class gui design for application
#***********************************************************************
class Ui_MainWindow(QObject):
    firebase_sig = QtCore.pyqtSignal()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1050, 811)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.logo_HCMUTE = QtWidgets.QLabel(self.centralwidget)
        self.logo_HCMUTE.setGeometry(QtCore.QRect(250, 10, 451, 111))
        self.logo_HCMUTE.setText("")
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
        self.TimeBox.setGeometry(QtCore.QRect(820, 290, 151, 121))
        font = QtGui.QFont()
        font.setFamily("URW Bookman")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.TimeBox.setFont(font)
        self.TimeBox.setObjectName("TimeBox")
        self.time = QtWidgets.QLabel(self.TimeBox)
        self.time.setGeometry(QtCore.QRect(10, 40, 131, 71))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.time.setFont(font)
        self.time.setObjectName("time")
        self.Date_box = QtWidgets.QGroupBox(self.centralwidget)
        self.Date_box.setGeometry(QtCore.QRect(820, 140, 161, 121))
        font = QtGui.QFont()
        font.setFamily("URW Bookman")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.Date_box.setFont(font)
        self.Date_box.setObjectName("Date_box")
        self.date = QtWidgets.QLabel(self.Date_box)
        self.date.setGeometry(QtCore.QRect(10, 40, 141, 71))
        font = QtGui.QFont()
        font.setFamily("DejaVu Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.date.setFont(font)
        self.date.setObjectName("date")
        self.inventory_btn = QtWidgets.QPushButton(self.centralwidget)
        self.inventory_btn.setGeometry(QtCore.QRect(820, 680, 171, 71))
        font = QtGui.QFont()
        font.setFamily("URW Bookman [UKWN]")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.inventory_btn.setFont(font)
        self.inventory_btn.setText("")
        self.inventory_btn.setObjectName("inventory_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1050, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #***my code here ***
        self.logo_HCMUTE.setPixmap(QtGui.QPixmap(image_dir + "Logo.png"))
        self.inventory_btn.setIcon(QtGui.QIcon('./image/analysis_icon'))
        self.inventory_btn.setIconSize(QtCore.QSize(40,40))

        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Inventory App"))
        self.group_img.setTitle(_translate("MainWindow", "shelf"))
        self.result_img.setText(_translate("MainWindow", "Image"))
        self.group_info.setTitle(_translate("MainWindow", "Index"))
        self.OOS_lable.setText(_translate("MainWindow", "Out of stock"))
        self.IS_lable.setText(_translate("MainWindow", "In stock"))
        self.avalible_lable.setText(_translate("MainWindow", "Available on shelf"))
        self.OOS_index.setText(_translate("MainWindow", "0"))
        self.IS_index.setText(_translate("MainWindow", "0"))
        self.TimeBox.setTitle(_translate("MainWindow", "Time"))
        self.time.setText(_translate("MainWindow", "time"))
        self.Date_box.setTitle(_translate("MainWindow", "Date"))
        self.date.setText(_translate("MainWindow", "date"))
    
    #******************************************************
    #my code here
    #******************************************************
    def connect_signal(self):
        self.firebase_sig.connect(self.update_data)

    def update_data(self):
        print("update data on GUI...")
        self.OOS_index.setText(str(self.OOS))
        self.IS_index.setText(str(self.In_stock))
        self.time.setText(str(self._time))
        self.date.setText(str(self._date))
        self.avalible_index.setProperty("value",self.avaliable)
        #set image
        self.qimg = QtGui.QImage(self.img_name)
        self.pixmap = QtGui.QPixmap().fromImage(self.qimg)
        self.h = self.result_img.width() - 10
        self.w = self.result_img.height() - 10
        self.result_img.setPixmap(self.pixmap.scaled(QtCore.QSize(self.w,self.h),
                                QtCore.Qt.KeepAspectRatio))
        self.wirte_csv()
        # log success
        print("update data on GUI success")
        

    def wirte_csv(self):
        print("write data to csv file...")
        # check csv file is exist
        file_list = [f for f in os.listdir(analysis_dir) if os.path.isfile(os.path.join(analysis_dir, f))]
        print("list all of files in analysis directory")
        print(file_list)
        if str(self._date + '.csv') in file_list:
            print('open ' + str(self._date + '.csv') + 'file and append data')
            with open(analysis_dir + str(self._date) + '.csv', 'a', newline='') as file:
                write_append = csv.writer(file)
                write_append.writerow([str(self.OOS), str(self.In_stock), str(self.avaliable), str(self._time)])
                file.close()
        else:
            print('create ' + str(self._date + '.csv') + 'file and write data')
            # define format data
            data = [['OOS', 'IS', 'Avalible', 'time'],
                    [str(self.OOS), str(self.In_stock), str(self.avaliable), str(self._time)]]
                
            with open(analysis_dir + str(self._date) + '.csv', 'w', newline='') as file:
                write = csv.writer(file)
                write.writerows(data)
                file.close()
        # log success        
        print("write data to csv file success.")
                



    def download_image(self):
        print("load image from firebase")
        self.bucket = storage.bucket()
        self.blob = self.bucket.blob(self.img_name)
        self.blob.download_to_filename(self.img_name)
        # log success
        print("load image from firebase success")
        

    def firebase_realtime_callback(self,event):
        self.json_data = event.data['Shelf']
        print("Receiving realtime data from firebase...")
        print(self.json_data)
        self.OOS = self.json_data['OOS']
        self.In_stock = self.json_data['In-stock']
        self.avaliable = int(float(self.json_data['In-stock_avalivle'])*100)
        self.img_name = self.json_data['img_output']
        self._time = self.json_data['time']
        self._date = self.json_data['date']
        #self.update_sig.emit()
        self.download_image()
        self.firebase_sig.emit()
        print("firebase_realtime_callback end !")
        
    def reshow_data(self):
        print('reshow_data.')

    def firebase_realtime(self):
        print("listen from realtime firebase...")
        self.ref = db.reference('/').listen(self.firebase_realtime_callback)



#*************************
#main function begin here
#*************************
def main():
    connect_to_firebase()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.firebase_realtime()
    ui.connect_signal()
    sys.exit(app.exec_())
    return
    

if __name__ == "__main__":
    main()




#Note: -----------------------------------------------------------------
#        def setupUi(self, MainWindow):
#        self.inventory_btn.setIcon(QtGui.QIcon('./image/analysis_icon'))
#        self.inventory_btn.setIconSize(QtCore.QSize(40,40))
#        self.inventory_btn.setObjectName("inventory_btn")