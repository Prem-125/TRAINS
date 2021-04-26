import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from PySide6 import QtWidgets, QtCore 
from CTC.src.CTCWrapper import MainWindow as CTC_Office
from CTC.src.CTCWrapper import *

from TrackModel.src.TrackModel import MainWindow as TrackModel
from TrainDeployer.src.TrainDeployer import TrainDeployer
from TrackControllerSW.src.TrackControllerSW import MainWindow as TrackControllerSW
from signals import signals 
#from src.UI.window_manager import window_list

"""
def open_modules():
    window_list.append(CTC_Office())
    window_list.append(TrackModel())

"""
#have an array of advertisements and a qtimer that picks one at random interval and spits them out or do it in current speed every time i get current speed or every 10 times i amke a neew announcemnt

def start():
    app = QApplication()
    CTC = CTC_Office()
    CTC.show()
    TM = TrackModel()
    TM.show()
    TC = TrackControllerSW()
    TC.show()
    TrainConsole = TrainDeployer()
 #   TrainConsole.CreateTrains(GreenLine, 1)
    #signals.train_creation.emit('Green',1)

    sys.exit(app.exec_())
    
if __name__ == "__main__":
    start()

"""
from argparse import ArgumentParser
import sys
from PyQt5 import QtWidgets
from src.UI.login_gui import LoginUi
from src.UI.timekeeper_gui import TimekeeperUi
from src.UI.CTC.ctc_gui import CTCUi
from src.UI.SWTrackController.swtrack_gui import SWTrackControllerUi
from src.UI.TrackModel.trackmodel_gui import TrackModelUi
from src.UI.TrainModel.trainmodel_gui import TrainModelUi
from src.UI.SWTrainController.TrainController import SWTrainUi
from src.UI.window_manager import window_list
from src.timekeeper import timekeeper
from src.TrackModel.TrackModelDef import SignalHandler
from src.HWTrackController.hw_track_controller_connector import HWTrackCtrlConnector
from src.SWTrackController.track_system import track_system
from src.SWTrackController.Compiler.lexer import Lexer
from src.SWTrackController.Compiler.emitter import Emitter
from src.SWTrackController.Compiler.parse import Parser
from src.logger import get_logger
from src.HWTrainController.HWTrainArduinoConnector import HWController
"""