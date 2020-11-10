# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 12:12:35 2020

@author: Егор
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PIL import Image
import sys
import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget
import numpy as np
from PyQt5.QtWidgets import QFileDialog
import os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("mainwindow.ui", self)
        self.files = []
        self.idTab = 0
        self.count = 0
        self.photoCount = 0
        self.pathToFile = "A:\\progrforrazm\\appforazm\\WebFaces_GroundThruth.txt"
        self.file = open(self.pathToFile,'w')
        self.img = pg.ImageItem()
        self.tab = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tab)
        self.idTab = self.tab.addTab(GraphicsLayoutWidget(),'All graphics')
        self.tab.setCurrentIndex(self.idTab)
        self.p1 = self.tab.widget(self.idTab).addPlot(title = '')
        self.photo_name = os.listdir("A:\\progrforrazm\\appforazm\\data")
        for i in range(len(self.photo_name)):
            self.files.append("A:\\progrforrazm\\appforazm\\data\\"+self.photo_name[i])
            print(self.files[i])
        self.openImage()
        
    def openImage(self):
        pic = Image.open(self.files[self.photoCount])
        self.file.write(self.photo_name[self.photoCount]+' ')
        pix = np.array(pic)
        self.img.setImage(pix)
        self.img.mouseClickEvent = self.imageClickedEvent
        self.p1.addItem(self.img)
    
    def imageClickedEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            pos = ev.pos()
            ppos = self.img.mapToParent(pos)
            x, y = ppos.x(), ppos.y()
            print(x,y)
            string = ''
            string = string + str(round(y))+' '+str(round(x))+' '
            self.file.write(string);
            self.count+=1
            if self.count == 4:
                self.count = 0
                self.photoCount+=1
                if self.photoCount < len(self.files):
                    self.file.write("\n")
                    self.openImage()
                else:
                    print("end of files")
                    self.file.close()
        
        
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()