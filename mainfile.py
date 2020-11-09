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
        self.x = 0
        self.y = 0
        self.photoCount = 0
        self.pathToFile = "C:\\razmdataset\\WebFaces_GroundThruth.txt"
        self.file = open(self.pathToFile,'w')
        self.img = pg.ImageItem()
        self.hist = pg.HistogramLUTItem()   
        self.tab = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tab)
        self.idTab = self.tab.addTab(GraphicsLayoutWidget(),'All graphics')
        self.tab.setCurrentIndex(self.idTab)
        self.p1 = self.tab.widget(self.idTab).addPlot(title = '')
        self.photos = os.listdir("C:\\razmdataset")
        self.openImage()
    def openImage(self):
        pic = Image.open(self.photos[self.photoCount])
        pix = np.array(pic)
        self.img.setImage(pix)
        self.img.hoverEvent = self.imageHoverEvent
        self.img.mouseClickEvent = self.imageClickedEvent
        self.p1.addItem(self.img)
    
    def imageHoverEvent(self,event):
        pos = event.pos()
        ppos = self.img.mapToParent(pos)
        self.x, self.y = ppos.x(), ppos.y()
        
    def imageClickedEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            string = ''
            string = string + str(round(self.x))+' '+str(round(self.y))
            self.file.write(string);
            self.count+=1
            if self.count == 4:
                self.count = 0
                self.photoCount+=1
                self.openImage()
            print(string)
        
        
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()