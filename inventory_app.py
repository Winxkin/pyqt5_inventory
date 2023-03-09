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
import cv2 as cv

#***********************************************************************
# define the function to compute MSE between two images
#***********************************************************************
def mse(img1, img2):
   h, w = img1.shape
   diff = cv.subtract(img1, img2)
   err = np.sum(diff**2)
   mse = err/(float(h*w))
   return mse

#***********************************************************************
#connect to firebase
#***********************************************************************
def connect_to_firebase():
    cred = credentials.Certificate("./inventory-firebase.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL' : 'https://inventory-16459-default-rtdb.asia-southeast1.firebasedatabase.app/',
        'storageBucket' : 'inventory-16459.appspot.com'
    })
    return

#***********************************************************************
#download image result from firebase storage
#***********************************************************************
def download_image(img_name):
    bucket = storage.bucket()
    blob = bucket.blob(img_name)
    time.sleep(2)   #waitting for image update
    blob.download_to_filename(img_name)
    return

#***********************************************************************
#listen realtime data callback function
#format data
#{'Shelf': {'In-stock': 80, 'In-stock_avalivle': '0.69', 'OOS': 5, 'img_output': 'result.jpg'}}
#***********************************************************************
def firebase_realtime_callback(event):
    json_data = event.data['Shelf']
    print("Receiving realtime data from firebase...")
    print(json_data)
    OOS = json_data['OOS']
    In_stock = json_data['In-stock']
    avaliable = json_data['In-stock_avalivle']
    img_name = json_data['img_output']
    show_data(OOS,In_stock,avaliable,img_name)
    download_image(img_name)
    print("firebase_realtime_callback end !")
    return

#***********************************************************************
#listen realtime data
#***********************************************************************
def firebase_realtime():
    print("listen from realtime firebase...")
    ref = db.reference('/').listen(firebase_realtime_callback)

    return





def show_data(OOS,In_stock,avaliable,img_name):
    print(OOS)
    print(In_stock)
    print(avaliable)
    print(img_name)
    return

#*************************
#main function begin here
#*************************
def main():
    connect_to_firebase()
    firebase_realtime()
    return

if __name__ == "__main__":
    #test()
    main()