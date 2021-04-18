import sys
import serial
import time
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, QTimer
from .UI import Ui_TrackControllerUI
from signals import signals

class MainWindow(QMainWindow):
    def __init__(self):
        #call parent constructor
        super(MainWindow, self).__init__()
        self.ui = Ui_TrackControllerUI()
        self.ui.setupUi(self)
        
        #Variables
        self.block_open = [True for i in range(44)]
        self.occupancy = [False for i in range(44)]
        self.authority = [True for i in range(44)]
        self.suggested_speed = [0 for i in range(44)]
        self.commanded_speed = [0 for i in range(44)]
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

    def timerCallback(self):
        #self.arduino.write(str(self.testval).encode('utf-8')+ self.eol)
        #self.serialWrite()
        self.serialRead()
        
        
        
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

            #if(int(status1) == 0):

            if int(status1)== 1 and self.switch_state1 !=1:
                self.switch_state1 = 1
                #print(type(self.ui.junctionPositionDisplay.text()))
              

                
                self.temp_val = self.ui.BlockInput.currentIndex()
                if(self.temp_val == 0):
                    self.ui.BlockInput.setCurrentIndex(self.temp_val + 1)
                    self.UIBlockOutput()
                elif(self.temp_val == 41):
                    self.ui.BlockInput.setCurrentIndex(0)
                    self.UIBlockOutput()
                else:
                    self.ui.BlockInput.setCurrentIndex(self.temp_val + 1)
                    self.UIBlockOutput()

                '''
                if (self.ui.junctionPositionDisplay.text() == "5-11"):
                    #self.button56_clicked()
                    print("this is pog")
                elif (self.ui.junctionPositionDisplay.text() == "5-6"):
                    #self.button511_clicked()
                    print("this is not pog")
                '''
            if int(status1)==0 and self.switch_state1 !=0:
                self.switch_state1 = 0
               

    def serialWrite(self):
        self.arduino.reset_output_buffer()
        self.arduino.write(str(self.nFlag).encode('utf-8')+ self.eol)
        self.arduino.write(str(self.encodedTC).encode('utf-8')+ self.eol)
        #self.arduino.write(self.curSpeed.encode('utf-8')+ self.eol)
        self.arduino.write(str(self.encodedB).encode('utf-8')+ self.eol)
        self.nFlag=0



    #Gets the occupancy
    def getOccupancy(self, blockNum, occupied):
        self.getSugSpeed()
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
        if(blockNum == blockAuthority):
            signals.wayside_to_track.emit(blockNum, 0, 0)
        else:
            signals.wayside_to_track.emit(blockNum, 1, commanded_speed[blockNum-self.block_offset])
    
    #Update the block status
    def setBlockStatus(self, blockNum, status):
        self.block_open[blockNum-block_offset] = status
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
       
    #Clears the system
    def ClearSystem(self):
        self.trackClosed = [False, False, False, False, False, False, False, False, False, False, False, False,  False, False, False]
        self.occupancy = [False, False, False, False, False, False, False, False, False, False, False, False,  False, False, False]
        self.authority = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.suggestedSpeed = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.switchState = True
        self.TrackStatDisp()
        self.OccupancyDisp()
        self.ControlSwitch()
        self.AuthorityDisp()
        self.SugSpeedDisp()
        self.UpdateOutputs()
    
   
        self.ui.SugSpeedB1.setText(str(self.suggestedSpeed[0]) +"MPH")
        self.ui.SugSpeedB2.setText(str(self.suggestedSpeed[1]) +"MPH")
        self.ui.SugSpeedB3.setText(str(self.suggestedSpeed[2]) +"MPH")
        self.ui.SugSpeedB4.setText(str(self.suggestedSpeed[3]) +"MPH")
        self.ui.SugSpeedB5.setText(str(self.suggestedSpeed[4]) +"MPH")
        self.ui.SugSpeedB6.setText(str(self.suggestedSpeed[5]) +"MPH")
        self.ui.SugSpeedB7.setText(str(self.suggestedSpeed[6]) +"MPH")
        self.ui.SugSpeedB8.setText(str(self.suggestedSpeed[7]) +"MPH")
        self.ui.SugSpeedB9.setText(str(self.suggestedSpeed[8]) +"MPH")
        self.ui.SugSpeedB10.setText(str(self.suggestedSpeed[9]) +"MPH")
        self.ui.SugSpeedB11.setText(str(self.suggestedSpeed[10]) +"MPH")
        self.ui.SugSpeedB12.setText(str(self.suggestedSpeed[11]) +"MPH")
        self.ui.SugSpeedB13.setText(str(self.suggestedSpeed[12]) +"MPH")
        self.ui.SugSpeedB14.setText(str(self.suggestedSpeed[13]) +"MPH")
        self.ui.SugSpeedB15.setText(str(self.suggestedSpeed[14]) +"MPH")
    '''

if __name__ == "__main__":
	app = QApplication(sys.argv)
	
	window = MainWindow()
	window.show()
	
	sys.exit(app.exec_())