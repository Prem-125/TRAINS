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
        self.GreenController2 = TrackController(21)
        self.GreenController3 = TrackController(33)
        self.GreenController4 = TrackController(61)
        self.GreenController5 = TrackController(74)
        self.GreenController6 = TrackController(82)
        self.GreenController7 = TrackController(105)

        # Green switches
        self.GreenController1.setSwitch(12, 13, 1)
        self.GreenController2.setSwitch(29, 30, 150)
        self.GreenController3.setSwitch(57, 151, 58)
        self.GreenController4.setSwitch(63, 62, 151)
        self.GreenController5.setSwitch(77, 76, 101)
        self.GreenController6.setSwitch(85, 86, 100)

        # Red Track Controllers
        self.RedController1 = TrackController(7)
        self.RedController2 = TrackController(0)
        self.RedController3 = TrackController(21)
        self.RedController4 = TrackController(30)
        self.RedController5 = TrackController(35)
        self.RedController6 = TrackController(41)
        self.RedController7 = TrackController(49)

        # Red switches
        self.RedController1.setSwitch(9, 10, 151)
        self.RedController2.setSwitch(16, 1, 15)
        self.RedController3.setSwitch(27, 28, 76)
        self.RedController4.setSwitch(33, 32, 72)
        self.RedController5.setSwitch(38, 39, 71)
        self.RedController6.setSwitch(44, 43, 67)
        self.RedController7.setSwitch(52, 53, 66)

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

    # Returns the proper controller
    def getController(self, line, block_num):
        if(line == "Green"):
            if(block_num <21):
                return self.GreenController1
            elif(block_num <33 or block_num >146):
                return self.GreenController2
            elif(block_num <61):
                return self.GreenController3
            elif(block_num <74):
                return self.GreenController4
            elif(block_num <82 or (block_num > 100 and block_num <105)):
                return self.GreenController5
            elif(block_num <101):
                return self.GreenController6
            elif(block_num < 147):
                return self.GreenController7
        if(line == "Red"):
            if(block_num <7 or (block_num >12 and block_num <21)):
                return self.RedController1
            elif(block_num <13):
                return self.RedController2
            elif(block_num <30 or block_num > 74):
                return self.RedController3
            elif(block_num <35 or (block_num > 71 and block_num <75)):
                return self.RedController4
            elif(block_num <40 or (block_num > 68 and block_num <72)):
                return self.RedController5
            elif(block_num <49 or (block_num > 66 and block_num <69)):
                return self.RedController6
            elif(block_num > 48):
                return self.RedController7

    # Occupancy Call
    def getOccupancy(self, block_num, occupied):

        self.getController("Green", block_num).getOccupancy(block_num, occupied)

        # if(block_num < 33 or block_num > 146):
        #     self.GreenController1.getOccupancy(block_num, occupied)
        # elif(block_num > 32 and block_num < 74):
        #     self.GreenController2.getOccupancy(block_num, occupied)
        # elif(block_num > 73 and block_num < 105):
        #     self.GreenController3.getOccupancy(block_num, occupied)
        # elif(block_num > 104 and block_num < 147):
        #     self.GreenController4.getOccupancy(block_num, occupied)
        self.UIBlockOutput()

    # Authority Call
    def getAuthority(self, line, block_num):

        self.getController("Green", block_num).getAuthority(block_num)

        # if(block_num < 33 or block_num > 146):
        #     self.GreenController1.getAuthority(block_num)
        # elif(block_num > 32 and block_num < 74):
        #     self.GreenController2.getAuthority(block_num)
        # elif(block_num > 73 and block_num < 105):
        #     self.GreenController3.getAuthority(block_num)
        # elif(block_num > 104 and block_num < 147):
        #     self.GreenController4.getAuthority(block_num)

    # Block Closure
    def setBlockClosure(self, line, block_num, break_type):

        self.getController("Green", block_num).setBlockClosure(line, block_num, break_type)
        # if(block_num < 33 or block_num > 146):
        #     self.GreenController1.setBlockClosure(line, block_num, break_type)
        # elif(block_num > 32 and block_num < 74):
        #     self.GreenController2.setBlockClosure(line, block_num, break_type)
        # elif(block_num > 73 and block_num < 105):
        #     self.GreenController3.setBlockClosure(line, block_num, break_type)
        # elif(block_num > 104 and block_num < 147):
        #     self.GreenController4.setBlockClosure(line, block_num, break_type)
        self.UIBlockOutput()

    # Block Status Updates
    def UpdateBlockStatus(self, line, block_num, status):

        self.getController("Green", block_num).UpdateBlockStatus(line, block__num, status)

        # if(block_num < 33 or block_num > 146):
        #     self.GreenController1.UpdateBlockStatus(line, block_num, status)
        # elif(block_num > 32 and block_num < 74):
        #     self.GreenController2.UpdateBlockStatus(line, block_num, status)
        # elif(block_num > 73 and block_num < 105):
        #     self.GreenController3.UpdateBlockStatus(line, block_num, status)
        # elif(block_num > 104 and block_num < 147):
        #     self.GreenController4.UpdateBlockStatus(line, block_num, status)
        self.UIBlockOutput()

    #Output for the UI
    def UIBlockOutput(self):
        #List of Green Line Controllers
        green_controllers = ["Choose","1","2","3","4","5","6","7"]
        red_controllers = ["Choose","1","2","3","4","5","6","7"]
        if(str(self.ui.StatusLineBox.currentText()) == "Green"):
            #Clear Combo Box
            #self.ui.StatusControllerBox.clear()
            #Enter Controller Inputs
            for controller_name in green_controllers:
                self.ui.StatusControllerBox.addItem(controller_name)
            if(str(self.ui.StatusControllerBox.currentText()) == "1"):

                #list of Blocks
                controller1_blocks = ["" for i in range(20)]
                controller1_blocks[0] = "Choose"
                for i in range(19):
                    controller1_blocks[i+1] = str(i+1)


                #Enter Block Inputs
                for block_name in controller1_blocks:
                    self.ui.BlockInput.addItem(block_name)

                #Call controller display function
                self.displayUIOutput(self.GreenController1)

            elif(str(self.ui.StatusControllerBox.currentText()) == "2"):

                #list of Blocks
                controller2_blocks = ["" for i in range(17)]
                controller2_blocks[0] = "Choose"
                for i in range(21,33):
                    controller2_blocks[i-20] = str(i)
                controller2_blocks[13] = "147"
                controller2_blocks[14] = "148"
                controller2_blocks[15] = "149"
                controller2_blocks[16] = "150"

                #Enter Block Inputs
                for block_name in controller2_blocks:
                    self.ui.BlockInput.addItem(block_name)

                #Call controller display function
                self.displayUIOutput(self.GreenController2)
            elif(str(self.ui.StatusControllerBox.currentText()) == "3"):

                #list of Blocks
                controller3_blocks = ["" for i in range(29)]
                controller3_blocks[0] = "Choose"
                for i in range(33,61):
                    controller3_blocks[i-32] = str(i)

                #Enter Block Inputs
                for block_name in controller3_blocks:
                    self.ui.BlockInput.addItem(block_name)

                #Call controller display function
                self.displayUIOutput(self.GreenController3)
            elif(str(self.ui.StatusControllerBox.currentText()) == "4"):

                #list of Blocks
                controller4_blocks = ["" for i in range(14)]
                controller4_blocks[0] = "Choose"
                for i in range(61,74):
                    controller4_blocks[i-60] = str(i)

                #Enter Block Inputs
                for block_name in controller4_blocks:
                    self.ui.BlockInput.addItem(block_name)

                #Call controller display function
                self.displayUIOutput(self.GreenController4)
            elif(str(self.ui.StatusControllerBox.currentText()) == "5"):

                #list of Blocks
                controller5_blocks = ["" for i in range(13)]
                controller5_blocks[0] = "Choose"
                for i in range(74,82):
                    controller5_blocks[i-73] = str(i)
                controller5_blocks[9] = "101"
                controller5_blocks[10] = "102"
                controller5_blocks[11] = "103"
                controller5_blocks[12] = "104"

                #Enter Block Inputs
                for block_name in controller5_blocks:
                    self.ui.BlockInput.addItem(block_name)

                #Call controller display function
                self.displayUIOutput(self.GreenController5)
            elif(str(self.ui.StatusControllerBox.currentText()) == "6"):

                #list of Blocks
                controller6_blocks = ["" for i in range(20)]
                controller6_blocks[0] = "Choose"
                for i in range(82,101):
                    controller6_blocks[i-81] = str(i)

                #Enter Block Inputs
                for block_name in controller6_blocks:
                    self.ui.BlockInput.addItem(block_name)

                #Call controller display function
                self.displayUIOutput(self.GreenController6)
            elif(str(self.ui.StatusControllerBox.currentText()) == "7"):

                #list of Blocks
                controller7_blocks = ["" for i in range(43)]
                controller7_blocks[0] = "Choose"
                for i in range(105,147):
                    controller7_blocks[i-104] = str(i)

                #Enter Block Inputs
                for block_name in controller7_blocks:
                    self.ui.BlockInput.addItem(block_name)

                #Call controller display function
                self.displayUIOutput(self.GreenController7)

        elif(str(self.ui.StatusLineBox.currentText()) == "Red"):
            #Clear Combo Box
            #self.ui.StatusControllerBox.clear()
            #Enter Controller Inputs
            for controller_name in red_controllers:
                self.ui.StatusControllerBox.addItem(controller_name)
            if(str(self.ui.StatusControllerBox.currentText()) == "1"):

                #list of Blocks
                controller1_blocks = ["" for i in range(7)]
                controller1_blocks[0] = "Choose"
                for i in range(7,13):
                    controller1_blocks[i-6] = str(i)

                #Enter Block Inputs
                for block_name in controller1_blocks:
                    self.ui.BlockInput.addItem(block_name)

                #Call controller display function
                self.displayUIOutput(self.RedController1)

            elif(str(self.ui.StatusControllerBox.currentText()) == "2"):

                #list of Blocks
                controller2_blocks = ["" for i in range(15)]
                controller2_blocks[0] = "Choose"
                for i in range(1,7):
                    controller2_blocks[i] = str(i)
                controller2_blocks[7] = "13"
                controller2_blocks[8] = "14"
                controller2_blocks[9] = "15"
                controller2_blocks[10] = "16"
                controller2_blocks[11] = "17"
                controller2_blocks[12] = "18"
                controller2_blocks[13] = "19"
                controller2_blocks[14] = "20"

                #Enter Block Inputs
                for block_name in controller2_blocks:
                    self.ui.BlockInput.addItem(block_name)

                #Call controller display function
                self.displayUIOutput(self.RedController2)
            elif(str(self.ui.StatusControllerBox.currentText()) == "3"):

                #list of Blocks
                controller3_blocks = ["" for i in range(12)]
                controller3_blocks[0] = "Choose"
                for i in range(21,30):
                    controller3_blocks[i-20] = str(i)
                controller3_blocks[10] = "75"
                controller3_blocks[11] = "76"

                #Enter Block Inputs
                for block_name in controller3_blocks:
                    self.ui.BlockInput.addItem(block_name)

                #Call controller display function
                self.displayUIOutput(self.RedController3)
            elif(str(self.ui.StatusControllerBox.currentText()) == "4"):

                #list of Blocks
                controller4_blocks = ["" for i in range(9)]
                controller4_blocks[0] = "Choose"
                for i in range(30,35):
                    controller4_blocks[i-29] = str(i)
                controller4_blocks[6] = "72"
                controller4_blocks[7] = "73"
                controller4_blocks[8] = "74"

                #Enter Block Inputs
                for block_name in controller4_blocks:
                    self.ui.BlockInput.addItem(block_name)

                #Call controller display function
                self.displayUIOutput(self.RedController4)
            elif(str(self.ui.StatusControllerBox.currentText()) == "5"):

                #list of Blocks
                controller5_blocks = ["" for i in range(11)]
                controller5_blocks[0] = "Choose"
                for i in range(35,41):
                    controller5_blocks[i-34] = str(i)
                controller5_blocks[7] = "68"
                controller5_blocks[8] = "69"
                controller5_blocks[9] = "70"
                controller5_blocks[10] = "71"

                #Enter Block Inputs
                for block_name in controller5_blocks:
                    self.ui.BlockInput.addItem(block_name)

                #Call controller display function
                self.displayUIOutput(self.RedController5)
            elif(str(self.ui.StatusControllerBox.currentText()) == "6"):

                #list of Blocks
                controller6_blocks = ["" for i in range(11)]
                controller6_blocks[0] = "Choose"
                for i in range(41,49):
                    controller6_blocks[i-40] = str(i)
                controller6_blocks[9] = "67"
                controller6_blocks[10] = "68"

                #Enter Block Inputs
                for block_name in controller6_blocks:
                    self.ui.BlockInput.addItem(block_name)

                #Call controller display function
                self.displayUIOutput(self.RedController6)
            elif(str(self.ui.StatusControllerBox.currentText()) == "7"):

                #list of Blocks
                controller7_blocks = ["" for i in range(19)]
                controller7_blocks[0] = "Choose"
                for i in range(49,67):
                    controller7_blocks[i-48] = str(i)

                #Enter Block Inputs
                for block_name in controller7_blocks:
                    self.ui.BlockInput.addItem(block_name)

                #Call controller display function
                self.displayUIOutput(self.RedController7)

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
