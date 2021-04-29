import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from UI2 import Ui_TrackControllerUI
from signals import signals
import csv
from TrackControllerHW.src.TrackControllerHW2 import *

class MainWindow(QMainWindow):
    def __init__(self):
        #call parent constructor
        super(MainWindow, self).__init__()
        self.ui = Ui_TrackControllerUI()
        self.ui.setupUi(self)

        # Instantiate Green Track Controllers for the system
        # Parameters are block offset value for the controller, and the line the Track Controller is on
        self.GreenController1 = TrackController(0, "Green", "G1")
        self.GreenController2 = TrackController(21, "Green", "G2")
        self.GreenController3 = TrackController(33, "Green", "G3")
        self.GreenController4 = TrackController(61, "Green", "G4")
        self.GreenController5 = TrackController(74, "Green", "G5")
        self.GreenController6 = TrackController(82, "Green", "G6")
        self.GreenController7 = TrackController(105, "Green", "G7")

        # Instantiate the switches for the Green Controllers
        # Parameters are the block stem number, branch a number, branch b number, and line
        self.GreenController1.set_Switch(13, 12, 1, "Green")
        self.GreenController2.set_Switch(28, 29, 150, "Green")
        self.GreenController3.set_Switch(57, 58, 151, "Green")
        self.GreenController4.set_Switch(63, 151, 62, "Green")
        self.GreenController5.set_Switch(77, 101, 76, "Green")
        self.GreenController6.set_Switch(85, 86, 100, "Green")

        # Instantiate the crossing for Green Controller
        # Parameter is block number
        self.GreenController1.set_Crossing(19)

        # Instantiate Red Track Controllers for the system
        # Parameters are block offset value for the controller, and the line the Track Controller is on
        self.RedController1 = TrackController(7, "Red", "R1")
        self.RedController2 = TrackController(0, "Red", "R2")
        self.RedController3 = TrackController(21, "Red", "R3")
        self.RedController4 = TrackController(30, "Red", "R4")
        self.RedController5 = TrackController(35, "Red", "R5")
        self.RedController6 = TrackController(41, "Red", "R6")
        self.RedController7 = TrackController(49, "Red", "R7")

        # Instantiate the switches for the Red Controllers
        # Parameters are the block stem number, branch a number, branch b number, and line
        self.RedController1.set_Switch(9, 10, 151, "Red")
        self.RedController2.set_Switch(16, 1, 15, "Red")
        self.RedController3.set_Switch(27, 28, 76, "Red")
        self.RedController4.set_Switch(33, 32, 72, "Red")
        self.RedController5.set_Switch(38, 39, 71, "Red")
        self.RedController6.set_Switch(44, 43, 67, "Red")
        self.RedController7.set_Switch(52, 53, 66, "Red")

        # Instantiate the crossing for Red Controller
        # Parameter is block number
        self.RedController6.set_Crossing(47)

        # Variables utilized by the UI functions
        # ui_block and ui_switch indicate the number for the referenced object
        self.ui_block = 0
        self.ui_switch = 0
        self.plc_name = [PLCLine()]

        # UI Functions
        # currentTextChanged method indicates a change in a combo box
        # clicked method indicates the push of a button
        self.ui.StatusLineBox.currentTextChanged.connect(self.UIBlockOutput)
        self.ui.StatusControllerBox.currentTextChanged.connect(self.UIBlockOutput)
        self.ui.BlockInput.currentTextChanged.connect(self.UIBlockOutput)
        self.ui.ImportButton.clicked.connect(self.ImportPLC)
        self.ui.ToggleBranchButton.clicked.connect(self.ToggleSwitchBranch)
        self.ui.MainLineBox.currentTextChanged.connect(self.UISwitchOutput)
        self.ui.MainControllerBox.currentTextChanged.connect(self.UISwitchOutput)

        # Signal Functions
        # Signals sent from the CTC Office and Track Model are connected to functions here
        signals.track_model_occupancy.connect(self.set_Occupancy)
        signals.CTC_authority.connect(self.get_Authority)
        signals.track_break.connect(self.set_BlockClosure)
        signals.wayside_block_status.connect(self.UpdateBlockStatus)
        signals.CTC_suggested_speed.connect(self.get_SugSpeed)
        signals.CTC_toggle_switch.connect(self.CTCToggleSwitch)

        #setup arduino
        self.utimer = QTimer()
        self.utimer.timeout.connect(self.timerCallback)
        self.utimer.start(500)
        self.testval = 0
        self.arduino = serial.Serial(port='COM4', baudrate=115200,timeout=.5)
        self.eol = '\n'.encode('utf-8')
        self.nFlag=0
        self.encodedTC=0
        self.rawToggle = 0
        self.encodedB=0
        self.switch_state1 = None
        self.switch_state2 = None
        self.switch_state3 = None
        self.switch_state4 = None
        self.switch_state5 = None
        self.temp_out = 0
        self.temp_val = ''

    #set up arduino reading
    def timerCallback(self):
        self.serialRead()

    #read arduino values and interpret
    def serialRead(self):
        
        #print("test")
        #print(self.arduino.in_waiting)
        while(self.arduino.in_waiting > 0):

            raw = self.arduino.readline()
            raw2 = self.arduino.readline()
            raw3 = self.arduino.readline()
            raw4 = self.arduino.readline()
            raw5 = self.arduino.readline()


            status1 = raw.decode('ascii').strip('\r\n')
            status2 = raw2.decode('ascii').strip('\r\n')
            status3 = raw3.decode('ascii').strip('\r\n')
            status4 = raw4.decode('ascii').strip('\r\n')
            status5 = raw5.decode('ascii').strip('\r\n')

            #print("ur in")


            #button 1 logic
            #make button to toggle tabs
            if int(status1)== 1 and self.switch_state1 !=1:
                self.switch_state1 = 1
                #print(type(self.ui.junctionPositionDisplay.text()))
                self.temp_val = self.ui.BlockInput.currentIndex()
                if(self.temp_val == 0):
                    self.ui.Program_2.setCurrentIndex(1)
                    self.UIBlockOutput()
                elif(self.temp_val == 1):
                    self.ui.Program_2.setCurrentIndex(2)
                    self.UIBlockOutput()
                else:
                    self.ui.Program_2.setCurrentIndex(0)
                    self.UIBlockOutput()
            if int(status1)==0 and self.switch_state1 !=0:
                self.switch_state1 = 0

            #button 2 logic
            #hardcode for specific controller
            if int(status2)== 1 and self.switch_state2 !=1:
                self.switch_state2 = 1
                #get index of tabwidget
                self.temp_val = self.ui.Program_2.currentIndex()
                if(self.temp_val == 2):
                    self.ToggleSwitchBranch()
            if int(status2)==0 and self.switch_state2 !=0:
                self.switch_state2 = 0




    # get_Controller is called to return a Controller object based on input
    # Parameters are track line name and block number
    def get_Controller(self, line, block_num):
        
        # Green line controllers
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
        
        # Red line controllers
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

    # get_SwitchController is called to return a Controller object based on input
    # Parameters are track line name and switch number
    # Used in UI functions
    def get_SwitchController(self, line, switch):
        
        # Green line controllers
        if(line == "Green"):
            if(switch == 1):
                return self.GreenController1
            elif(switch == 2):
                return self.GreenController2
            elif(switch == 3):
                return self.GreenController3
            elif(switch == 4):
                return self.GreenController4
            elif(switch == 5):
                return self.GreenController5
            elif(switch == 6):
                return self.GreenController6
            elif(switch == 7):
                return self.GreenController7
        
        # Red line controllers
        elif(line == "Red"):
            if(switch == 1):
                return self.RedController1
            elif(switch == 2):
                return self.RedController2
            elif(switch == 3):
                return self.RedController3
            elif(switch == 4):
                return self.RedController4
            elif(switch == 5):
                return self.RedController5
            elif(switch == 6):
                return self.RedController6
            elif(switch == 7):
                return self.RedController7

    # get_Tag gets the tag of the PLC function call controller to run for the system
    # Parameters are either line name, block number
    def get_Tag(self, line, block_num):
        
        # Green line controllers
        if(line == "Green"):
            if(block_num <21):
                return "G1"
            elif(block_num <33 or block_num >146):
                return "G2"
            elif(block_num <61):
                return "G3"
            elif(block_num <74):
                return "G4"
            elif(block_num <82 or (block_num > 100 and block_num <105)):
                return "G5"
            elif(block_num <101):
                return "G6"
            elif(block_num < 147):
                return "G7"
        
        # Red line controllers
        if(line == "Red"):
            if(block_num <7 or (block_num >12 and block_num <21)):
                return "R1"
            elif(block_num <13):
                return "R2"
            elif(block_num <30 or block_num > 74):
                return "R3"
            elif(block_num <35 or (block_num > 71 and block_num <75)):
                return "R4"
            elif(block_num <40 or (block_num > 68 and block_num <72)):
                return "R5"
            elif(block_num <49 or (block_num > 66 and block_num <69)):
                return "R6"
            elif(block_num > 48):
                return "R7"
    
    # set_Occupancy is called to set the occupancy recieved from the Track Model
    # Calls set_Occupancy function in the proper TrackController object
    # Parameters are block number, and boolean occupied status
    def set_Occupancy(self, line, block_num, occupied):
        # Asks for controller object, calls controller function
        self.get_Controller(line, block_num).set_Occupancy(block_num, occupied)
        self.UIBlockOutput()
        #self.RunPLC(self.get_Tag(line, block_num))

    # get_Authority is called to return the Authority of the block
    # Calls get_Authority function in the proper TrackController object
    # Parameters are track line name, block number, and authority
    def get_Authority(self, line, block_num, authority):
        # Asks for controller object, calls controller function
        self.get_Controller(line, block_num).get_Authority(block_num, authority)
        self.UIBlockOutput()

    # get_SugSpeed is called to get the Suggested Speed from CTC Office
    # Calls the respective TrackController get_SugSpeed Function
    # Sets the limit with the suggested speed
    # Parameters are track line name, block number, and suggested speed
    def get_SugSpeed(self, line, block_num, sug_speed):
        
        # Initialize limit
        limit = 0
        
        # Green Limits
        if(line == "Green"):
            if((block_num > 0 and block_num < 13) \
            or (block_num > 85 and block_num < 101)):
                limit = 55
            elif((block_num > 16 and block_num < 21) \
            or (block_num > 57 and block_num < 63) \
            or (block_num > 68 and block_num < 77) \
            or (block_num > 101 and block_num < 110) \
            or (block_num > 116 and block_num < 122)):
                limit = 60
            else:
                limit = 70

        # Red Limits
        elif(line == "Red"):
            if(block_num > 0 and block_num < 17):
                limit = 40
            elif((block_num > 20 and block_num < 24) \
            or (block_num > 50 and block_num < 77) \
            or (block_num == 17)):
                limit = 55
            elif(block_num > 48 and block_num < 51):
                limit = 60
            else:
                limit = 70
        
        # Asks for controller object, calls controller function
        self.get_Controller(line, block_num).get_SugSpeed(block_num, sug_speed, limit)
        self.UIBlockOutput()

    # set_BlockClosure is called from Signal
    # Calls the closure function in the proper TrackController object
    # Parameters are track line name, block number, and break type
    def set_BlockClosure(self, line, block_num, break_type):
        # Asks for controller object, calls controller function
        self.get_Controller(line, block_num).set_BlockClosure(line, block_num, break_type)
        self.UIBlockOutput()

    # Updates the Block status from Signal if reopened
    # Calls the update block function in the proper TrackController object
    # Parameters are track line name, block number, and block status
    def UpdateBlockStatus(self, line, block_num, status):
        # Asks for controller object, calls controller function
        self.get_Controller(line, block_num).UpdateBlockStatus(line, block_num, status)
        self.UIBlockOutput()

    # ToggleSwitchBranch is called by the UI push button
    # Checks the UI combobox text and toggles the proper switch
    def ToggleSwitchBranch(self):
        # Green Controllers
        if(self.ui.MainLineBox.currentText() == "Green"):
            if(self.ui.MainControllerBox.currentText() == "1"):
                self.GreenController1.switch.ToggleBranch()
                self.UISwitchOutput(self.GreenController1)
            elif(self.ui.MainControllerBox.currentText() == "2"):
                self.GreenController2.switch.ToggleBranch()
                self.UISwitchOutput(self.GreenController2)
            elif(self.ui.MainControllerBox.currentText() == "3"):
                self.GreenController3.switch.ToggleBranch()
                self.UISwitchOutput(self.GreenController3)
            elif(self.ui.MainControllerBox.currentText() == "4"):
                self.GreenController4.switch.ToggleBranch()
                self.UISwitchOutput(self.GreenController4)
            elif(self.ui.MainControllerBox.currentText() == "5"):
                self.GreenController5.switch.ToggleBranch()
                self.UISwitchOutput(self.GreenController5)
            elif(self.ui.MainControllerBox.currentText() == "6"):
                self.GreenController6.switch.ToggleBranch()
                self.UISwitchOutput(self.GreenController6)
            elif(self.ui.MainControllerBox.currentText() == "7"):
                self.GreenController7.switch.ToggleBranch()
                self.UISwitchOutput(self.GreenController7)
        # Red Controllers
        elif(self.ui.MainLineBox.currentText() == "Red"):
            if(self.ui.MainControllerBox.currentText() == "1"):
                self.RedController1.switch.ToggleBranch()
                self.UISwitchOutput(self.RedController1)
            elif(self.ui.MainControllerBox.currentText() == "2"):
                self.RedController2.switch.ToggleBranch()
                self.UISwitchOutput(self.RedController2)
            elif(self.ui.MainControllerBox.currentText() == "3"):
                self.RedController3.switch.ToggleBranch()
                self.UISwitchOutput(self.RedController3)
            elif(self.ui.MainControllerBox.currentText() == "4"):
                self.RedController4.switch.ToggleBranch()
                self.UISwitchOutput(self.RedController4)
            elif(self.ui.MainControllerBox.currentText() == "5"):
                self.RedController5.switch.ToggleBranch()
                self.UISwitchOutput(self.RedController5)
            elif(self.ui.MainControllerBox.currentText() == "6"):
                self.RedController6.switch.ToggleBranch()
                self.UISwitchOutput(self.RedController6)
            elif(self.ui.MainControllerBox.currentText() == "7"):
                self.RedController7.switch.ToggleBranch()
                self.UISwitchOutput(self.RedController7)

    # CTCToggleSwitch is called when the CTC toggles a switch
    # Uses the proper Track Controller to toggle the switch
    # Parameters are track line name and block number
    def CTCToggleSwitch(self, line, block_num):
        # Asks for controller object, calls controller function
        self.get_Controller(line, block_num).switch.ToggleBranch()

    # Populates the comboboxes and selections for the UI
    # Reads from the comboboxes to populate the boxes correctly
    def UIBlockOutput(self):
        # List of Green Line Controllers
        green_controllers = ["Choose","1","2","3","4","5","6","7"]
        # List of Red Line Controllers
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

    # Populates the Switch Outputs for the UI
    # Parameters are TrackControllerSW object
    def UISwitchOutput(self, controller):
        if(self.ui.MainControllerBox.currentText() == "Choose"):
            self.ui.StemBox.setText("N/A")
            self.ui.BranchABox.setText("N/A")
            self.ui.BranchBBox.setText("N/A")
            self.ui.MainBranchCon.setText("N/A")
        else:
            controller = self.get_SwitchController(self.ui.MainLineBox.currentText(), int(self.ui.MainControllerBox.currentText()))
            if(controller.switch.block == -1):
                self.ui.StemBox.setText("N/A")
                self.ui.BranchABox.setText("N/A")
                self.ui.BranchBBox.setText("N/A")
                self.ui.MainBranchCon.setText("N/A")
            else:
                self.ui.StemBox.setText(str(controller.switch.block))
                self.ui.BranchABox.setText(str(controller.switch.branch_a))
                self.ui.BranchBBox.setText(str(controller.switch.branch_b))
                self.ui.MainBranchCon.setText(str(controller.switch.cur_branch))

    # Displays the UI output for the specified controller
    # Parameters are TrackControllerSW object
    def displayUIOutput(self, controller):
        if (self.ui.BlockInput.currentText() == "Choose"):
            self.ui.BlockStatus.setText("N/A")
            self.ui.Occupancy.setText("N/A")
            self.ui.Authority.setText("N/A")
            self.ui.CommandedSpeed.setText("N/A")
            self.ui.CrossingStatus.setText("N/A")
            self.ui.SwitchStatus.setText("N/A")
        else:
            controller.ui_block = int(self.ui.BlockInput.currentText())

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

    # Imports the PLC script designated by the UI
    # Prints validity output
    def ImportPLC(self):
        
        # Clears the PLC array
        self.plc_name.clear()
        inputFileName = self.ui.ImportLine.text()

        # Error checking
        try:
            plc_file = open(inputFileName,'r')

        except OSError:
            self.ui.SuccessFailLine.setText("Invalid File")

        with plc_file:
            self.ui.SuccessFailLine.setText("Valid File")
            
            # CSV reader implementation
            csv_reader = csv.reader(plc_file, delimiter=' ')
            num_lines = 0
            for row in csv_reader:
                if(num_lines == 0):
                    print("Importing PLC Scripts")
                print(row)
                
                line_length = len(row)
                
                # Adds a PLC Line object and adds the elements
                self.plc_name.append(PLCLine())
                for i in range(line_length):
                    self.plc_name[num_lines].set_element(i,row[i])
                
                num_lines+=1

        print("PLC Scripts Imported")
        plc_file.close()
    
    # Runs the PLC script for the designated tag
    # Outputs the proper boolean value of the 
    def RunPLC(self, tag):

        # Loops through all of the lines instructions
        for i in range(len(self.plc_name)):

            # Checks the first instruction
            if(self.plc_name[i].element[0] == tag):
                
                # Switch Instruction
                if(tag(0) == "G" or tag(0) == "R"):
                    if(tag(0) == "G"):
                        s_controller = self.get_SwitchController("Green", int(tag(1)))
                    elif(tag(0) == "R"):
                        s_controller = self.get_SwitchController("Red", int(tag(1)))
                        block_1 = self.plc_name[i+1].elements[2]

                        # More than one block
                        if(len(self.plc_name[i+1].elements) > 3):
                            op_1 = self.plc_name[i+1].elements[3]
                            block_2 = self.plc_name[i+1].elements[5]
                            block_end = self.plc_name[i+1].elements[7]
                            
                            # More than two blocks
                            if(len(self.plc_name[i+1].elements)>8):
                                block_4 = self.plc_name[i+1].elements[9]

                            # One block and Range
                            else:
                                continue

                        # Only one block
                        else:
                            s_offset = s_controller.block_offset
                            # Boolean True
                            if(s_controller.occupancy[block - s_offset] == True):
                                if(s_controller.switch.cur_branch != block_1):
                                    s_controller.switch.ToggleBranch()
                            # Boolean False
                            else:
                                if(s_controller.switch.cur_branch == block_1):
                                    s_controller.switch.ToggleBranch()
                            


                # Collision Instruction
                elif(tag == "COL"):
                    continue
                
                # Authority Instruction
                elif(tag == "AUT"):
                    continue
                
                # Crossing Instruction
                elif(tag == "CRX"):
                    continue


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
