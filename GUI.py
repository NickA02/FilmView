"""GUI Module"""
import random
import sys

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget)
from __feature__ import snake_case, true_property
from Controller import Controller


class MyWidget(QWidget):
    def __init__(self, controller: Controller):
        self.controller = controller
        QWidget.__init__(self)
        self.layout = QVBoxLayout(self)
        self.playButton = QPushButton("Play")
        self.layout.add_widget(self.playButton)
        self.playButton.clicked.connect(self.controller.playVideo())

        self.pauseButton = QPushButton("Pause")
        self.layout.add_widget(self.pauseButton)
        self.pauseButton.clicked.connect(self.controller.pauseVideo())

        self.nextViewButton = QPushButton("Next View")
        self.layout.add_widget(self.nextViewButton)
        self.nextViewButton.clicked.connect(self.controller.nextView())

        self.nextPlayButton = QPushButton("Next Play")
        self.layout.add_widget(self.nextPlayButton)
        self.nextPlayButton.clicked.connect(self.controller.nextPlay())

        self.prevViewButton = QPushButton("Previous View")
        self.layout.add_widget(self.prevViewButton)
        self.prevViewButton.clicked.connect(self.controller.prevView())

        self.prevPlayButton = QPushButton("Previous Play")  
        self.layout.add_widget(self.prevPlayButton)
        self.prevPlayButton.clicked.connect(self.controller.prevPlay())


        







#if __name__ == "__main__":
app = QApplication(sys.argv)
controller = Controller()
widget = MyWidget(controller)
widget.show()

sys.exit(app.exec_())