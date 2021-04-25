import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from .UI import Ui_TrackControllerUI
from signals import signals
from TrackControllerSW.src.TrackControllerSW import *

class MainWindow(QMainWindow):
    def __init__(self):
        #call parent constructor
        super(MainWindow, self).__init__()
        self.ui = Ui_TrackControllerUI()
        self.ui.setupUi(self)

        # Green Track Controllers
        self.GreenController1 = TrackController(0)
        self.GreenController2 = TrackController(33)
        self.GreenController3 = TrackController(74)
        self.GreenController4 = TrackController(105)

        #self.RedController1 = TrackController(0)

        #UI used variables
        self.ui_block = 0
        self.plc_name = ""

        #UI Functions
        self.ui.StatusLineBox.currentTextChanged.connect(self.UIBlockOutput)
        self.ui.StatusControllerBox.currentTextChanged.connect(self.UIBlockOutput)
        self.ui.BlockInput.currentTextChanged.connect(self.UIBlockOutput)
        self.ui.ImportButton.clicked.connect(self.ImportPLC)

        #Signal Functions
        signals.track_model_occupancy.connect(self.getOccupancy)
        signals.CTC_authority.connect(self.getAuthority)
        signals.track_break.connect(self.setBlockClosure)
        signals.wayside_block_status.connect(self.UpdateBlockStatus)
        #signals.CTC_suggested_speed.connect(self.getSugSpeed)
        #need wayside to track switch signals
        #need crossing signals

    # Occupancy Call
    def getOccupancy(self, block_num, occupied):
        if(block_num < 33 or block_num > 146):
            self.GreenController1.getOccupancy(block_num, occupied)
        elif(block_num > 32 and block_num < 74):
            self.GreenController2.getOccupancy(block_num, occupied)
        elif(block_num > 73 and block_num < 105):
            self.GreenController3.getOccupancy(block_num, occupied)
        elif(block_num > 104 and block_num < 147):
            self.GreenController4.getOccupancy(block_num, occupied)
        self.UIBlockOutput()

    # Authority Call
    def getAuthority(self, line, block_num):
        if(block_num < 33 or block_num > 146):
            self.GreenController1.getAuthority(block_num)
        elif(block_num > 32 and block_num < 74):
            self.GreenController2.getAuthority(block_num)
        elif(block_num > 73 and block_num < 105):
            self.GreenController3.getAuthority(block_num)
        elif(block_num > 104 and block_num < 147):
            self.GreenController4.getAuthority(block_num)

    # Block Closure
    def setBlockClosure(self, line, block_num, break_type):
        if(block_num < 33 or block_num > 146):
            self.GreenController1.setBlockClosure(line, block_num, break_type)
        elif(block_num > 32 and block_num < 74):
            self.GreenController2.setBlockClosure(line, block_num, break_type)
        elif(block_num > 73 and block_num < 105):
            self.GreenController3.setBlockClosure(line, block_num, break_type)
        elif(block_num > 104 and block_num < 147):
            self.GreenController4.setBlockClosure(line, block_num, break_type)
        self.UIBlockOutput()

    # Block Status Updates
    def UpdateBlockStatus(self, line, block_num, status):
        if(block_num < 33 or block_num > 146):
            self.GreenController1.UpdateBlockStatus(line, block_num, status)
        elif(block_num > 32 and block_num < 74):
            self.GreenController2.UpdateBlockStatus(line, block_num, status)
        elif(block_num > 73 and block_num < 105):
            self.GreenController3.UpdateBlockStatus(line, block_num, status)
        elif(block_num > 104 and block_num < 147):
            self.GreenController4.UpdateBlockStatus(line, block_num, status)
        self.UIBlockOutput()

    #Output for the UI
    def UIBlockOutput(self):
        #List of Green Line Controllers
        green_controllers = ["Choose","1","2","3","4"]
        print("UIBlockOutput Called\n")
        if(str(self.ui.StatusLineBox.currentText()) == "Green"):

            #Clear Combo Box
            #self.ui.StatusControllerBox.clear()

            #Enter Controller Inputs
            for controller_name in green_controllers:
                self.ui.StatusControllerBox.addItem(controller_name)

            if(str(self.ui.StatusControllerBox.currentText()) == "1"):

                #list of Blocks
                controller1_blocks = ["" for i in range(37)]
                controller1_blocks[0] = "Choose"
                for i in range(32):
                    controller1_blocks[i+1] = str(i+1)
                controller1_blocks[33] = "147"
                controller1_blocks[34] = "148"
                controller1_blocks[35] = "149"
                controller1_blocks[36] = "150"

                #Enter Block Inputs
                for block_name in controller1_blocks:
                    self.ui.BlockInput.addItem(block_name)

                #Call controller display function
                self.displayUIOutput(self.GreenController1)

            elif(str(self.ui.StatusControllerBox.currentText()) == "2"):

                #list of Blocks
                controller2_blocks = ["" for i in range(42)]
                controller2_blocks[0] = "Choose"
                for i in range(33,74):
                    controller2_blocks[i-32] = str(i)

                #Enter Block Inputs
                for block_name in controller2_blocks:
                    self.ui.BlockInput.addItem(block_name)

                #Call controller display function
                self.displayUIOutput(self.GreenController2)

            elif(str(self.ui.StatusControllerBox.currentText()) == "3"):

                #list of Blocks
                controller3_blocks = ["" for i in range(32)]
                controller3_blocks[0] = "Choose"
                for i in range(74,105):
                    controller3_blocks[i-73] = str(i)

                #Enter Block Inputs
                for block_name in controller3_blocks:
                    self.ui.BlockInput.addItem(block_name)

                #Call controller display function
                self.displayUIOutput(self.GreenController3)

            elif(str(self.ui.StatusControllerBox.currentText()) == "4"):

                #list of Blocks
                controller4_blocks = ["" for i in range(43)]
                controller4_blocks[0] = "Choose"
                for i in range(105,147):
                    controller4_blocks[i-104] = str(i)

                #Enter Block Inputs
                for block_name in controller4_blocks:
                    self.ui.BlockInput.addItem(block_name)

                #Call controller display function
                self.displayUIOutput(self.GreenController4)

    #Display the UI functions
    def displayUIOutput(self, controller):
        if (self.ui.BlockInput.currentText() == "Choose"):
            self.ui.BlockStatus.setText("N/A")
            self.ui.Occupancy.setText("N/A")
            self.ui.Authority.setText("N/A")
            self.ui.CommandedSpeed.setText("N/A")
            self.ui.CrossingStatus.setText("N/A")
            self.ui.SwitchStatus.setText("N/A")
        else:
            controller.ui_block = int(self.ui.BlockInput.currentText()) #Convert block input to string

            if(controller.block_open[controller.ui_block-controller.block_offset] == True):
                self.ui.BlockStatus.setText("Open")
                self.ui.Occupancy.setText(str(controller.occupancy[controller.ui_block-controller.block_offset]))
                self.ui.Authority.setText(str(controller.authority[controller.ui_block-controller.block_offset]))
                self.ui.CommandedSpeed.setText(str(controller.commanded_speed[controller.ui_block-controller.block_offset]))
                self.ui.CrossingStatus.setText("N/A")
                self.ui.SwitchStatus.setText("N/A")
            else:
                self.ui.BlockStatus.setText("Closed")
                self.ui.Occupancy.setText("N/A")
                self.ui.Authority.setText("N/A")
                self.ui.CommandedSpeed.setText("N/A")
                self.ui.CrossingStatus.setText("N/A")
                self.ui.SwitchStatus.setText("N/A")

    #Import PLC
    def ImportPLC(self):
        self.plc_name = self.ui.ImportLine.currentText()
        self.ui.SuccessFailLine.setText("Valid File")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
