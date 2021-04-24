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
        self.switch_exit_num = 0
        self.switch_in_a = 0
        self.switch_in_b = 0
        self.block_authority = 0

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
        signals.CTC_authority.connect(self.getAuthority)
        signals.track_break.connect(self.setBlockClosure)
        signals.wayside_block_status.connect(self.UpdateBlockStatus)
        #signals.CTC_suggested_speed.connect(self.getSugSpeed)
        #need wayside to track switch signals

    #Sets the block offset for the track controller
    def setBlockOffset(self, b_offset):
        self.block_offset = b_offset

    #Gets the occupancy
    def getOccupancy(self, blockNum, occupied):
        self.getSugSpeed(blockNum)
        self.occupancy[blockNum-self.block_offset] = occupied        #Use block offset to set the occupancy
        self.UIBlockOutput()
        self.setOfficeOccupancy(blockNum, occupied)

        if(occupied == True):
            self.setTrackStats(blockNum)
    
    #Update the CTC Office Occupancy
    def setOfficeOccupancy(self, blockNum, occupied):
        print("\nSet the office occupancy function called\n")
        print("Occupied Block Number: " + str(blockNum)+ "\n\n")
        signals.CTC_occupancy.emit("Green",blockNum, occupied)    #Sends the Occupancy Signal

    #Gets the authority
    def getAuthority(self, line, blockNum):
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
    
    #Update the block closure
    def setBlockClosure(self, line, blockNum, break_type):
        self.block_open[blockNum-self.block_offset] = False
        self.UpdateCTCFailure(line, blockNum, break_type)
        self.UIBlockOutput()
    
    #Update the CTC Office of Block Closures
    def UpdateCTCFailure(self, line, blockNum, break_type):
        signals.CTC_failure.emit(line, blockNum, break_type)
        self.UIBlockOutput()

    #Update the Track model of block openings
    def UpdateTMOpenings(self, line, blockNum):
        signals.wayside_block_open.emit(line, blockNum)

    #Update the block status
    def UpdateBlockStatus(self, line, blockNum, status):
        self.block_open[blockNum-self.block_offset] = status
        if(status == True):
            self.UpdateTMOpenings(line,blockNum)
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
    '''

if __name__ == "__main__":
	app = QApplication(sys.argv)
	
	window = MainWindow()
	window.show()
	
	sys.exit(app.exec_())