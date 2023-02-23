"""GUI Module"""
import random
import sys
import os
import cv2 as cv
import xml.etree.ElementTree as ET
import pandas as pd

from PySide6.QtCore import Qt, Slot, QThread, Signal
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget, QTreeWidget, 
                               QHBoxLayout, QGridLayout, QScrollArea,
                               QFileDialog)
from PySide6.QtGui import QImage, QPixmap
import numpy as np
from Controller import Controller
from MetaDataHandler import parsed_metadata

class VideoThread(QThread):
    change_pixmap_signal = Signal(np.ndarray)
    play_data_signal = Signal(parsed_metadata)

    def __init__(self, controller: Controller):
        QThread.__init__(self)
        self.controller = controller
        self._run_flag = True
        self._stop_flag = False

    def run(self):
        # capture from web cam
        self._stop_flag = False
        self._run_flag = True
        while self._run_flag:
            self.controller.update_frame()
            self.controller.fetch_metadata()
            self.change_pixmap_signal.emit(controller.fetch_current_frame())
            if self.controller.check_metadata_change():
                self.play_data_signal.emit(controller.fetch_metadata())
        self._stop_flag = True
    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
    
    def pause(self):
        self._run_flag = False
        i = 0
        while not self._stop_flag:
            i += 1
            if i == 100000:
                return False
        return True


class MyWidget(QWidget):
    def __init__(self, controller: Controller):
        self.controller = controller
        QWidget.__init__(self)
        self.layout = QHBoxLayout(self)
        self.buttonLayout = QGridLayout()
        self.playButton = QPushButton("Play")
        self.playButton.clicked.connect(self.play)
        self.buttonLayout.addWidget(self.playButton,0,0)

        self.pauseButton = QPushButton("Pause")
        self.pauseButton.clicked.connect(self.pause)
        self.buttonLayout.addWidget(self.pauseButton,0,1)

        self.nextViewButton = QPushButton("Next View")
        self.nextViewButton.clicked.connect(self.nextView)
        self.buttonLayout.addWidget(self.nextViewButton,2,1)

        self.nextPlayButton = QPushButton("Next Play")
        self.nextPlayButton.clicked.connect(self.nextPlay)
        self.buttonLayout.addWidget(self.nextPlayButton,1,1)

        self.prevViewButton = QPushButton("Previous View")
        self.prevViewButton.clicked.connect(self.prevView)
        self.buttonLayout.addWidget(self.prevViewButton,2,0)

        self.changeViewButton = QPushButton("Change File")
        self.changeViewButton.clicked.connect(self.changeFile)
        self.buttonLayout.addWidget(self.changeViewButton,3,0,1,2)

        self.prevPlayButton = QPushButton("Previous Play")  

        self.prevPlayButton.clicked.connect(self.prevPlay)
        self.buttonLayout.addWidget(self.prevPlayButton, 1, 0)
        
        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)
        self.image_label.resize(720, 1280)
        # create the video capture thread
        self.thread = VideoThread(controller)
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.metadata_box = QScrollArea()
        self.metadata_box.setWidgetResizable(True)
        self.dataLabel = QLabel("Data")
        self.dataLabel.setWordWrap(True)
        self.metadata_box.setWidget(self.dataLabel)
    
    
        self.thread.play_data_signal.connect(self.update_metadata)
        # start the thread
        self.thread.start()
        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.buttonLayout)
        self.vlayout.addWidget(self.metadata_box)

        self.layout.addLayout(self.vlayout)

        self.buttonLayout = QGridLayout()

    
    def closeEvent(self, event):
        self.thread.stop()
        event.accept()
    
    def play(self):
        self.thread.pause()
        self.controller.playVideo()
        self.thread.start()
    
    def pause(self):
        self.thread.pause()
        self.controller.pauseVideo()
        self.thread.start()

    def nextView(self):
        self.thread.pause()
        self.controller.nextView()
        self.controller.update_frame()
        self.controller.fetch_metadata()
        self.thread.start()

    def prevView(self):
        self.thread.pause()
        self.controller.prevView()
        self.controller.update_frame()
        controller.fetch_metadata()
        self.thread.start()

    def nextPlay(self):
        self.thread.pause()
        self.controller.nextPlay()
        self.controller.update_frame()
        controller.fetch_metadata()
        self.thread.start()

    def prevPlay(self):
        self.thread.pause()
        self.controller.prevPlay()
        self.controller.update_frame()
        self.controller.fetch_metadata()
        self.thread.start()
    
    def changeFile(self):
        self.thread.pause()
        file_filter = 'Data file (*.mp4)'
        res = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a file',
            dir=os.getcwd(),
            filter=file_filter
        )
        print(res)
        self.controller.changeVideo(res[0])


    @Slot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    @Slot(parsed_metadata)
    def update_metadata(self, data: parsed_metadata):
        data_string = ("Play ID: " + str(data.play_number) +"\n")
        data_string += ("View: " + data.current_view + "\n")
        for section in data.pff_data.keys():
            if not pd.isna(data.pff_data[section]):
                data_string += section + ":" + str(data.pff_data[section]) + "\n"
        #print(data_string)
        self.dataLabel.setText(data_string)


    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(1280, 720, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    








if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    widget = MyWidget(controller)
    widget.show()

    sys.exit(app.exec())