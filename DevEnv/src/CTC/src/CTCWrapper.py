import sys
import time
from UI import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

#Global variable to serve as system-wide clock
gbl_seconds = 0
gbl_centiseconds = 0

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
        self.ui.GreenLineButton1.clicked.connect(self.SetGreenMap)
        self.ui.RedLineButton1.clicked.connect(self.SetRedMap)
        self.ui.SectionComboBox1.currentTextChanged.connect(self.SetSectionBlocks)

        #Set global clock
        self.utimer = QTimer()
        self.utimer.timeout.connect(self.timerUpdate)
        self.utimer.start(100)

    #End constructor

    #Methods to navigate central stacked widget
    def SetStack1Index0(self):
        self.ui.StackedWidget1.setCurrentIndex(0)

    def SetStack1Index1(self):
        self.ui.StackedWidget1.setCurrentIndex(1)

    def SetStack1Index2(self):
        self.ui.StackedWidget1.setCurrentIndex(2)

    #Methods to modify map information
    def SetGreenMap(self):
        self.ui.StackedWidget2.setCurrentIndex(0)
        
        #Create list of Green track sections
        green_track_sections = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
                                "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

        #Clear contents of section combo box
        self.ui.SectionComboBox1.clear()

        #Populate section combo box
        for letter in green_track_sections:
            self.ui.SectionComboBox1.addItem(letter)
        
    def SetRedMap(self):
        self.ui.StackedWidget2.setCurrentIndex(1)

        #Create list of Red track sections
        red_track_sections = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                                "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"]
                            
        #Clear contents of section combo box
        self.ui.SectionComboBox1.clear()

        #Populate section combo box
        for letter in red_track_sections:
            self.ui.SectionComboBox1.addItem(letter)

    def SetSectionBlocks(self):
        #Check if the Green line or Red line is being view
        if(self.ui.StackedWidget2.currentIndex() == 0): #Green line is open
            #Print member blocks of selected track section
            if(self.ui.SectionComboBox1.currentText() == "A"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section A: 1-3")
            elif(self.ui.SectionComboBox1.currentText() == "B"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section B: 4-6")
            elif(self.ui.SectionComboBox1.currentText() == "C"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section C: 7-12")
            elif(self.ui.SectionComboBox1.currentText() == "D"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section D: 13-16")
            elif(self.ui.SectionComboBox1.currentText() == "E"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section E: 17-20")
            elif(self.ui.SectionComboBox1.currentText() == "F"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section F: 21-28")
            elif(self.ui.SectionComboBox1.currentText() == "G"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section G: 29-32")
            elif(self.ui.SectionComboBox1.currentText() == "H"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section H: 33-35")
            elif(self.ui.SectionComboBox1.currentText() == "I"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section I: 36-57")
            elif(self.ui.SectionComboBox1.currentText() == "J"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section J: 58-62")
            elif(self.ui.SectionComboBox1.currentText() == "K"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section K: 63-68")
            elif(self.ui.SectionComboBox1.currentText() == "L"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section L: 69-73")
            elif(self.ui.SectionComboBox1.currentText() == "M"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section M: 74-76")
            elif(self.ui.SectionComboBox1.currentText() == "N"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section N: 77-85")
            elif(self.ui.SectionComboBox1.currentText() == "O"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section O: 86-88")
            elif(self.ui.SectionComboBox1.currentText() == "P"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section P: 89-97")
            elif(self.ui.SectionComboBox1.currentText() == "Q"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section Q: 98-100")
            elif(self.ui.SectionComboBox1.currentText() == "R"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section R: 101")
            elif(self.ui.SectionComboBox1.currentText() == "S"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section S: 102-104")
            elif(self.ui.SectionComboBox1.currentText() == "T"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section T: 105-109")
            elif(self.ui.SectionComboBox1.currentText() == "U"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section U: 110-116")
            elif(self.ui.SectionComboBox1.currentText() == "V"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section V: 117-121")
            elif(self.ui.SectionComboBox1.currentText() == "W"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section W: 122-143")
            elif(self.ui.SectionComboBox1.currentText() == "X"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section X: 144-146")
            elif(self.ui.SectionComboBox1.currentText() == "Y"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section Y: 147-149")
            elif(self.ui.SectionComboBox1.currentText() == "Z"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section Z: 150")
            #End track section if-elif block
        
        elif(self.ui.StackedWidget2.currentIndex() == 1): #Red line is open
            #Print member blocks of selected track section
            if(self.ui.SectionComboBox1.currentText() == "A"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section A: 1-3")
            elif(self.ui.SectionComboBox1.currentText() == "B"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section B: 4-6")
            elif(self.ui.SectionComboBox1.currentText() == "C"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section C: 7-9")
            elif(self.ui.SectionComboBox1.currentText() == "D"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section D: 10-12")
            elif(self.ui.SectionComboBox1.currentText() == "E"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section E: 13-15")
            elif(self.ui.SectionComboBox1.currentText() == "F"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section F: 16-20")
            elif(self.ui.SectionComboBox1.currentText() == "G"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section G: 21-23")
            elif(self.ui.SectionComboBox1.currentText() == "H"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section H: 24-45")
            elif(self.ui.SectionComboBox1.currentText() == "I"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section I: 46-48")
            elif(self.ui.SectionComboBox1.currentText() == "J"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section J: 49-54")
            elif(self.ui.SectionComboBox1.currentText() == "K"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section K: 55-57")
            elif(self.ui.SectionComboBox1.currentText() == "L"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section L: 58-60")
            elif(self.ui.SectionComboBox1.currentText() == "M"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section M: 61-63")
            elif(self.ui.SectionComboBox1.currentText() == "N"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section N: 64-66")
            elif(self.ui.SectionComboBox1.currentText() == "O"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section O: 67")
            elif(self.ui.SectionComboBox1.currentText() == "P"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section P: 68-70")
            elif(self.ui.SectionComboBox1.currentText() == "Q"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section Q: 71")
            elif(self.ui.SectionComboBox1.currentText() == "R"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section R: 72")
            elif(self.ui.SectionComboBox1.currentText() == "S"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section S: 73-75")
            elif(self.ui.SectionComboBox1.currentText() == "T"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section T: 76")

        #End track line if-elif block

    #Method to update global clock
    def timerUpdate(self):
        global gbl_seconds
        global gbl_centiseconds

        #Increment centiseconds after timeout
        gbl_centiseconds += 1

        #Increment seconds after 10 centiseconds
        if(gbl_centiseconds == 10):
            print("\n" + str(gbl_seconds))
            gbl_seconds += 1

            #Reset centiseconds to prevent overflow
            gbl_centiseconds = 0
        #End if

        #Convert seconds to hours:minutes:seconds
        hour = int(gbl_seconds / 3600)
        minute = int( (gbl_seconds%3600)/60 )
        seconds = int(gbl_seconds%60)
        gui_time = str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':' + str(seconds).zfill(2)

        #Print updated time to GUI
        self.ui.SysTimeLabel.setText("Time: " + gui_time)

        #Restart timout period
        self.utimer.start(100)


#End MainWindow class definition

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())