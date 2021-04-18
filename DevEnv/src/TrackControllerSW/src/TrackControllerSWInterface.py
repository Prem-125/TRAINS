import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from .UI import Ui_TrackControllerUI
from signals import signals
from TrackControllerSW import TrackControllerSW

class MainWindow(QMainWindow):
    def __init__(self):
        #call parent constructor
        super(MainWindow, self).__init__()
        self.ui = Ui_TrackControllerUI()
        self.ui.setupUi(self)

        TrackController Green1
        TrackController Green2
        TrackController Green3
        TrackController Green4
        TrackController Green5

        TrackController Red1
        TrackController Red2
        TrackController Red3
        TrackController Red4
        TrackController Red5
    
    def setControllerOffset(self, track_controller, offset):
        track_controller.setBlockOffset(offset)

    def setSwitchExit(self, track_controller, block):
        track_controller.switch_exit_num = block

    def setSwitchIn(self, track_controller, a, b):
        track_controller.switch_in_a = a
        track_controller.switch_in_b = b


