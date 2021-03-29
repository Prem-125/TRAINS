import sys
import time
from UI import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

#Global variable to serve as system-wide clock
gbl_seconds = 0

#Define MainWindow class
class MainWindow(QMainWindow): #Subclass of QMainWindow

    #Constructor
    def __init__(self):
        #Call parent constructor
        super(MainWindow, self).__init__()
        self.ui = Ui_CTCOffice()
        self.ui.setupUi(self)

        #Define user navigation buttons over main stacked widget
        self.ui.StackControlButton1.clicked.connect(self.SetStack1Index0)
        self.ui.StackControlButton2.clicked.connect(self.SetStack1Index1)
        self.ui.StackControlButton3.clicked.connect(self.SetStack1Index2)

        #Define user navigation buttons in stacked widget of track map page
        self.ui.GreenLineButton1.clicked.connect(self.SetStack2Index0)
        self.ui.RedLineButton1.clicked.connect(self.SetStack2Index1)

        #Set global clock
        self.utimer = QTimer()
        self.utimer.timeout.connect(self.timerCallback)
        self.utimer.start(1000)

    #End constructor

    #Methods to navigate central stacked widget
    def SetStack1Index0(self):
        self.ui.StackedWidget1.setCurrentIndex(0)

    def SetStack1Index1(self):
        self.ui.StackedWidget1.setCurrentIndex(1)

    def SetStack1Index2(self):
        self.ui.StackedWidget1.setCurrentIndex(2)

    #Methods to navigate track map widget
    def SetStack2Index0(self):
        self.ui.StackedWidget2.setCurrentIndex(0)

    def SetStack2Index1(self):
        self.ui.StackedWidget2.setCurrentIndex(1)

    #Method to update global clock
    def timerCallback(self):
        global gbl_seconds

        print("\n" + str(gbl_seconds))

        #Increment after timeout
        gbl_seconds += 1

        #Convert seconds to hours:minutes:seconds
        hour = int(gbl_seconds / 3600)
        minute = int( (gbl_seconds%3600)/60 )
        seconds = int(gbl_seconds%60)
        gui_time = str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':' + str(seconds).zfill(2)

        #Print updated time to GUI
        self.ui.SysTimeLabel.setText("Time: " + gui_time)

        #Restart timout period
        self.utimer.start(1000)


#End MainWindow class definition

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())