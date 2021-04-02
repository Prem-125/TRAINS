import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from .UI import Ui_TrackControllerUI
from signals import signals

class MainWindow(QMainWindow):
    def __init__(self):
        #call parent constructor
        super(MainWindow, self).__init__()
        self.ui = Ui_TrackControllerUI()
        self.ui.setupUi(self)
        
        #Variables
        self.block_open = [True for i in range(150)]
        self.occupancy = [False for i in range(150)]
        self.authority = [True for i in range(150)]
        self.suggested_speed = [0 for i in range(150)]
        self.commanded_speed = [0 for i in range(150)]
        self.authority_block = 0
        self.switch_state = True
        self.block_offset = 33

        #UI used variables
        self.ui_block = 0
        self.plc_name = ""
        
        #UI Functions
        self.ui.BlockInput.currentTextChanged.connect(self.UIBlockOutput)
        self.ui.ImportButton.clicked.connect(self.ImportPLC)
        '''
        self.ui.ClearButton.clicked.connect(self.ClearSystem)
        '''

        #Signal Functions
        signals.track_model_occupancy.connect(self.getOccupancy)
        #need broken track block signal
        signals.CTC_authority.connect(self.getAuthority)
        #signals.CTC_suggested_speed.connect(self.getSugSpeed)
        #need track maintenance signal
        #need wayside to track switch signals

    #Gets the occupancy
    def getOccupancy(self, blockNum, occupied):
        self.getSugSpeed(blockNum)
        self.occupancy[blockNum-self.block_offset] = occupied        #Use block offset to set the occupancy
        self.UIBlockOutput()
        if(occupied == True):
            self.setOfficeOccupancy(blockNum)
            self.setTrackStats(blockNum)
    #Update the CTC Office Occupancy
    def setOfficeOccupancy(self, blockNum):
        signals.CTC_occupancy.emit(blockNum)    #Sends the Occupancy Signal

    #Gets the authority
    def getAuthority(self, blockNum):
        self.authority[blockNum-self.block_offset] = False
        self.block_authority = blockNum


    #Gets the suggested speed
    def getSugSpeed(self, blockNum):
        self.setComSpeed(blockNum)

    #Gets the commanded speed
    def setComSpeed(self, blockNum):
        for i in range(0, 25):
            self.commanded_speed[i] = 70
        for i in range(25, 30):
            self.commanded_speed[i] = 60
        for i in range(30, 36):
            self.commanded_speed[i] = 70
        for i in range(36, 41):
            self.commanded_speed[i] = 60   

    #Update Track Model of the authority and commanded speed
    def setTrackStats(self, blockNum):
        if(blockNum == self.block_authority):
            signals.wayside_to_track.emit(blockNum, 0, 0)
        else:
            signals.wayside_to_track.emit(blockNum, 1, self.commanded_speed[blockNum-self.block_offset])
    
    #Update the block status
    def setBlockStatus(self, blockNum, status):
        self.block_open[blockNum-self.block_offset] = status
        self.UIBlockOutput()

    #Import PLC
    def ImportPLC(self):
        self.plc_name = self.ui.ImportLine.currentText()
        self.ui.SuccessFailLine.setText("Valid File")
    
    #Output for the UI
    def UIBlockOutput(self):
        if (self.ui.BlockInput.currentText() == "Choose"):
            self.ui.BlockStatus.setText("N/A")
            self.ui.Occupancy.setText("N/A")
            self.ui.Authority.setText("N/A")
            self.ui.CommandedSpeed.setText("N/A")
            self.ui.CrossingStatus.setText("N/A")
            self.ui.SwitchStatus.setText("N/A")
        else:
            self.ui_block = int(self.ui.BlockInput.currentText()) #Convert block input to string
            
            if(self.block_open[self.ui_block-self.block_offset] == True):
                self.ui.BlockStatus.setText("Open")
                self.ui.Occupancy.setText(str(self.occupancy[self.ui_block-self.block_offset]))
                self.ui.Authority.setText(str(self.authority[self.ui_block-self.block_offset]))
                self.ui.CommandedSpeed.setText(str(self.commanded_speed[self.ui_block-self.block_offset]))
                self.ui.CrossingStatus.setText("N/A")
                self.ui.SwitchStatus.setText("N/A")
            else:
                self.ui.BlockStatus.setText("Closed")
                self.ui.Occupancy.setText("N/A")
                self.ui.Authority.setText("N/A")
                self.ui.CommandedSpeed.setText("N/A")
                self.ui.CrossingStatus.setText("N/A")
                self.ui.SwitchStatus.setText("N/A")
    
    #Controls the Switch States
    '''
    def ControlSwitch(self):
        if(self.occupancy[4]):
            if(self.occupancy[5] == False):
                if(self.occupancy[10] == False):
                    if((int(self.authority[4]) < 11)):
                        if(int(self.authority[4]) > 5):
                            self.switchState = True
                    elif(int(self.authority[4]) >11):
                        self.switchState = False
                else:
                    self.switchState = True
            else:
                self.switchState = False
        elif (self.occupancy[10] == True):
            self.switchState = False
        elif (self.occupancy[5] == True):
            self.switchState = True
        self.SwitchDisp()
    '''

if __name__ == "__main__":
	app = QApplication(sys.argv)
	
	window = MainWindow()
	window.show()
	
	sys.exit(app.exec_())