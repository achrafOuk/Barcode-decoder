import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from PyQt5 import QtWidgets, uic,QtCore
import sys
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtCore import QTimer,Qt
import sqlite3
import os

def create_connect(database):
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        pass
    return conn

def recherche_produit(conn,barcode_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM produit WHERE barcode_id=?", (barcode_id,))
    rows = cur.fetchone()
    liste=[]
    if(rows):
        for index,j in enumerate(rows):
            liste.append(j)
    return liste


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui,self).__init__()
        
        uic.loadUi('cv_projet_barcode.ui',self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.uploadImageButton.clicked.connect(self.get_image)
        self.cameraButton.clicked.connect(self.show_camera)
        self.closeCamera.clicked.connect(self.close_camera)
        self.show()
    def get_image(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'insert image', os.path.dirname(os.path.abspath(__file__)),'image(*.jpg *.png )')
        filepath=filename[0]
        img=cv2.imread(filepath)
        img=self.detectAndDecodeFromImage(filepath)
        w=self.label.width()
        h=self.label.height()
        img=cv2.resize(img, (w,h), interpolation = cv2.INTER_AREA)
        img=img[:,:,::-1]
        ch=img.shape[2]
        bytesPerLine = ch * w
        image=QImage(img.data.tobytes(), w, h, bytesPerLine,QImage.Format_RGB888)
        Piximage=QPixmap.fromImage(image)
        
        image_resize = Piximage.scaled(w,h, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(image_resize)
        
    def show_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,600)
        self.cap.set(4,271)
        self.timer.start(1000/24)
        self.cameraButton.setEnabled(False)
        self.closeCamera.setEnabled(True)
    def close_camera(self):
        self.timer.stop()
        self.cameraButton.setEnabled(True)
        self.closeCamera.setEnabled(False)
        self.cap.release()
        self.label.setText("")
    def nextFrameSlot(self):
        val,frame=self.cap.read()
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        image=QImage(frame,frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        cam=QPixmap.fromImage(image)
        self.label.setPixmap(cam)
        barcodes = pyzbar.decode(frame)
        conn=create_connect("barcode_ti_product.db")
        if barcodes :
            for barcode in barcodes :
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
                text = "{} ({})".format(barcodeData, barcodeType)
                image=QImage(frame,frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                cam=QPixmap.fromImage(image)
                self.label.setPixmap(cam)
                rows=recherche_produit(conn,barcodeData)
                if (len(rows) != 0):
                    text = "barcode produit:{}\n".format(rows[1])

                    text1 = "nom de produit:{}\n".format(rows[2])

                    text2 = "prix de produit:{}\n".format(rows[3])

                    self.produit_data.setPlainText(text + text1 + text2)
                print(barcodeData)
                print("------")
    def detectAndDecodeFromImage(self,img):
        image=cv2.imread(img)
        barcodes = pyzbar.decode(image)
        for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            conn=create_connect("barcode_ti_product.db")
            rows=recherche_produit(conn,barcodeData)
            
            if(len(rows)!=0):
                (x, y, w, h) = barcode.rect
                cv2.rectangle(image, (x, y), (x + w, y + h), (255,255, 0), 2)
                text = "barcode produit:{}\n".format(rows[1])
                
                text1 = "nom de produit:{}\n".format(rows[2])
                
                text2 = "prix de produit:{}\n".format(rows[3])
                
                self.produit_data.setPlainText(text+text1+text2)

        return image    
        
app=QtWidgets.QApplication(sys.argv)
window=Ui()
app.exec_()


        
        
    
