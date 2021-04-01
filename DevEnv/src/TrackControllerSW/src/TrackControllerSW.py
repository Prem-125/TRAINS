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
        self.trackClosed = [False for i in range(44)]
        self.occupancy = [False for i in range(44)]
        self.authority = [True for i in range(44)]
        self.authorityFromBlock = [0 for i in range(44)]
        self.newAuthority = [0 for i in range(44)]
        self.suggestedSpeed = [0 for i in range(44)]
        self.commandedSpeed = [0 for i in range(44)]

        self.authorityBlock
        self.switchState = True
        self.trackOccString = ""
        self.block_offset = 58
        
        #Button Functions
        '''
        self.ui.CTCButton.clicked.connect(self.getCTCInputs)
        self.ui.TMButton.clicked.connect(self.getTMInputs)
        self.ui.OutputButton.clicked.connect(self.UpdateOutputs)
        self.ui.ClearButton.clicked.connect(self.ClearSystem)
        '''

        #Signal Functions
        signals.track_model_occupancy.connect(self.getOccupancy)
        #need broken track block signal
        signals.CTC_authority.connect(self.getAuthority)
        #need suggested speed signal
        #need track maintenance signal

    #Gets the occupancy
    def getOccupancy(self, blockNum, occupied):
        self.occupancy[blockNum] = occupied
        if(occupied == True):
            self.setOfficeOccupancy(blockNum)
            self.setTrackStats(blockNum)
    #Update the CTC Office Occupancy
    def setOfficeOccupancy(self, block):
        #Sends the Occupancy Signal
        signals.CTC_occupancy.emit(block)

    #Gets the authority
    def getAuthority(self, blockNum):
        self.authority[blockNum] = False
        self.blockAuthority = blockNum
    #Gets the suggested speed
    def getSugSpeed(self, blockNum):
        pass
    #Gets the commanded speed
    def getComSpeed(self, blockNum):
        pass
    #Update Track Model of the authority and commanded speed
    def setTrackStats(self, blockNum):
        if(blockNum == blockAuthority):
            signals.wayside_to_track.emit(blockNum, 0, 0)
        else:
            signals.wayside_to_track.emit(blockNum, 1, commandedSpeed[blockNum])

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
    #Calculates Commanded Speed
    '''
    def CalcCommandedSpeed(self):
        for x in range(15):
            if(authority[x] == 0)
                self.commandedSpeed[x] = 0
            else
                self.commandedSpeed[x] = int(float(self.suggestedSpeed[x]) * 0.621371)
    '''    
    #Calculates the authority to the next block
    '''
    def CalcAuthFromBlock(self):
        for x in range(15):
            if(self.authority[x] == 0):
                self.authorityFromBlock[x] = 0
            elif(int(self.authority[x]) > x):
                if(int(self.authority[x]) > 10):
                    self.authorityFromBlock[x] = self.authority[5] - x * -1
                else:
                    self.authorityFromBlock[x] = self.authority[x] - x
            else:
                if(x>10):
                    self.authorityFromBlock[x] = x-5 - int(self.authority[x])
    '''
    #Creates the Track Occupancy String
    '''
    def getTrackOccString(self):
        self.trackOccString = ""
        for x in range(15):
            if(self.occupancy[x] == False):
                self.trackOccString = self.trackOccString + "0"
            else:
                self.trackOccString = self.trackOccString + "1"
    '''
    #Gets the CTC Inputs
    '''
    def getCTCInputs(self):
        self.CTCBlockNumber = self.ui.CTCBlockInput.text()

        #Update the variables
        self.suggestedSpeed[self.CTCBlockNumber-1] = self.ui.SugSpeedInput.text()
        self.authority[self.CTCBlockNumber-1] = self.ui.AuthorityInput.text()
        if(self.ui.BlockStatusInput.text() == "Closed"):
            self.trackClosed[self.CTCBlockNumber-1] = True
        else:
            self.trackClosed[self.CTCBlockNumber-1] = False
        
        #Update the GUI
        self.TrackStatDisp()
        self.OccupancyDisp()
        self.AuthorityDisp()
        self.SugSpeedDisp()
        self.ControlSwitch()

        #Update the Track Model         
    '''

    '''
    #gets the Track Model Inputs
    def getTMInputs(self):
        
        #Update the variables
        
        #Update the GUI
        self.TrackStatDisp()
        self.OccupancyDisp()
        self.AuthorityDisp()
        self.SugSpeedDisp()
        self.ControlSwitch()

        #Update the CTC Office
        self.ControlSwitch()
        
        #Send Switch States
        #Send Occupancy
    '''

    '''    
    #Updates the Outputs
    def UpdateOutputs(self):
        #CTC Output
        self.ControlSwitch()
        if(self.switchState == True):
            self.ui.SwitchStateOutput.setText("B")
        else:
            self.ui.SwitchStateOutput.setText("C")
        
        self.getTrackOccString()
        self.CalcCommandedSpeed()
        self.CalcNewAuthority()

        self.ui.OccupancyOutput.setText(str(self.trackOccString))

        #Track Model Output
        if(self.ui.BlockOutInput.text() == "1"):
            self.ui.AuthorityOutput.setText(str(self.newAuthority[0]) + "ft")
            self.ui.ComSpeedOutput.setText(str(self.commandedSpeed[0])+ "MPH")
            self.ui.SwitchPosOutput.setText("N/A")
        if(self.ui.BlockOutInput.text() == "2"):
            self.ui.AuthorityOutput.setText(str(self.newAuthority[1]) + "ft")
            self.ui.ComSpeedOutput.setText(str(self.commandedSpeed[1])+ "MPH")
            self.ui.SwitchPosOutput.setText("N/A")
        if(self.ui.BlockOutInput.text() == "3"):
            self.ui.AuthorityOutput.setText(str(self.newAuthority[2]) + "ft")
            self.ui.ComSpeedOutput.setText(str(self.commandedSpeed[2])+ "MPH")
            self.ui.SwitchPosOutput.setText("N/A")
        if(self.ui.BlockOutInput.text() == "4"):
            self.ui.AuthorityOutput.setText(str(self.newAuthority[3]) + "ft")
            self.ui.ComSpeedOutput.setText(str(self.commandedSpeed[3])+ "MPH")
            self.ui.SwitchPosOutput.setText("N/A")
        if(self.ui.BlockOutInput.text() == "5"):
            self.ui.AuthorityOutput.setText(str(self.newAuthority[4]) + "ft")
            self.ui.ComSpeedOutput.setText(str(self.commandedSpeed[4])+ "MPH")
            if(self.switchState == True):
                self.ui.SwitchPosOutput.setText("B")
            else:
                self.ui.SwitchPosOutput.setText("C")
        if(self.ui.BlockOutInput.text() == "6"):
            self.ui.AuthorityOutput.setText(str(self.newAuthority[5]) + "ft")
            self.ui.ComSpeedOutput.setText(str(self.commandedSpeed[5])+ "MPH")
            if(self.switchState == True):
                self.ui.SwitchPosOutput.setText("B")
            else:
                self.ui.SwitchPosOutput.setText("C")
        if(self.ui.BlockOutInput.text() == "7"):
            self.ui.AuthorityOutput.setText(str(self.newAuthority[6]) + "ft")
            self.ui.ComSpeedOutput.setText(str(self.commandedSpeed[6])+ "MPH")
            self.ui.SwitchPosOutput.setText("N/A")
        if(self.ui.BlockOutInput.text() == "8"):
            self.ui.AuthorityOutput.setText(str(self.newAuthority[7]) + "ft")
            self.ui.ComSpeedOutput.setText(str(self.commandedSpeed[7])+ "MPH")
            self.ui.SwitchPosOutput.setText("N/A")
        if(self.ui.BlockOutInput.text() == "9"):
            self.ui.AuthorityOutput.setText(str(self.newAuthority[8]) + "ft")
            self.ui.ComSpeedOutput.setText(str(self.commandedSpeed[8])+ "MPH")
            self.ui.SwitchPosOutput.setText("N/A")
        if(self.ui.BlockOutInput.text() == "10"):
            self.ui.AuthorityOutput.setText(str(self.newAuthority[9]) + "ft")
            self.ui.ComSpeedOutput.setText(str(self.commandedSpeed[9])+ "MPH")
            self.ui.SwitchPosOutput.setText("N/A")
        if(self.ui.BlockOutInput.text() == "11"):
            self.ui.AuthorityOutput.setText(str(self.newAuthority[10]) + "ft")
            self.ui.ComSpeedOutput.setText(str(self.commandedSpeed[10])+ "MPH")
            if(self.switchState == True):
                self.ui.SwitchPosOutput.setText("B")
            else:
                self.ui.SwitchPosOutput.setText("C")
        if(self.ui.BlockOutInput.text() == "12"):
            self.ui.AuthorityOutput.setText(str(self.newAuthority[11]) + "ft")
            self.ui.ComSpeedOutput.setText(str(self.commandedSpeed[11])+ "MPH")
            self.ui.SwitchPosOutput.setText("N/A")
        if(self.ui.BlockOutInput.text() == "13"):
            self.ui.AuthorityOutput.setText(str(self.newAuthority[12]) + "ft")
            self.ui.ComSpeedOutput.setText(str(self.commandedSpeed[12])+ "MPH")
            self.ui.SwitchPosOutput.setText("N/A")
        if(self.ui.BlockOutInput.text() == "14"):
            self.ui.AuthorityOutput.setText(str(self.newAuthority[13]) + "ft")
            self.ui.ComSpeedOutput.setText(str(self.commandedSpeed[13])+ "MPH")
            self.ui.SwitchPosOutput.setText("N/A")
        if(self.ui.BlockOutInput.text() == "15"):
            self.ui.AuthorityOutput.setText(str(self.newAuthority[14]) + "ft")
            self.ui.ComSpeedOutput.setText(str(self.commandedSpeed[14])+ "MPH")
            self.ui.SwitchPosOutput.setText("N/A")
    
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
    
    #set the track status
    def TrackStatDisp(self):
        if (self.trackClosed[0] == False):
            self.ui.StatusB1.setText("Open")
        else:
            self.ui.StatusB1.setText("Closed")
        if (self.trackClosed[1] == False):
            self.ui.StatusB2.setText("Open")
        else:
            self.ui.StatusB2.setText("Closed")
        if (self.trackClosed[2] == False):
            self.ui.StatusB3.setText("Open")
        else:
            self.ui.StatusB3.setText("Closed")
        if (self.trackClosed[3] == False):
            self.ui.StatusB4.setText("Open")
        else:
            self.ui.StatusB4.setText("Closed")
        if (self.trackClosed[4] == False):
            self.ui.StatusB5.setText("Open")
        else:
            self.ui.StatusB5.setText("Closed")
        if (self.trackClosed[5] == False):
            self.ui.StatusB6.setText("Open")
        else:
            self.ui.StatusB6.setText("Closed")
        if (self.trackClosed[6] == False):
            self.ui.StatusB7.setText("Open")
        else:
            self.ui.StatusB7.setText("Closed")
        if (self.trackClosed[7] == False):
            self.ui.StatusB8.setText("Open")
        else:
            self.ui.StatusB8.setText("Closed")
        if (self.trackClosed[8] == False):
            self.ui.StatusB9.setText("Open")
        else:
            self.ui.StatusB9.setText("Closed")
        if (self.trackClosed[9] == False):
            self.ui.StatusB10.setText("Open")
        else:
            self.ui.StatusB10.setText("Closed")
        if (self.trackClosed[10] == False):
            self.ui.StatusB11.setText("Open")
        else:
            self.ui.StatusB11.setText("Closed")
        if (self.trackClosed[11] == False):
            self.ui.StatusB12.setText("Open")
        else:
            self.ui.StatusB12.setText("Closed")
        if (self.trackClosed[12] == False):
            self.ui.StatusB13.setText("Open")
        else:
            self.ui.StatusB13.setText("Closed")
        if (self.trackClosed[13] == False):
            self.ui.StatusB14.setText("Open")
        else:
            self.ui.StatusB14.setText("Closed")
        if (self.trackClosed[14] == False):
            self.ui.StatusB15.setText("Open")
        else:
            self.ui.StatusB15.setText("Closed")
    
    #set the track occupancy display    
    def OccupancyDisp(self):
        #Block 1
        if (self.occupancy[0] == False):
            self.ui.OccupationB1.setText("Unoccupied")
        else:
            self.ui.OccupationB1.setText("Occupied")
        #Block 2
        if (self.occupancy[1] == False):
            self.ui.OccupationB2.setText("Unoccupied")
        else:
            self.ui.OccupationB2.setText("Occupied")
        #Block 3
        if (self.occupancy[2] == False):
            self.ui.OccupationB3.setText("Unoccupied")
        else:
            self.ui.OccupationB3.setText("Occupied")
        #Block 4
        if (self.occupancy[3] == False):
            self.ui.OccupationB4.setText("Unoccupied")
        else:
            self.ui.OccupationB4.setText("Occupied")
        #Block 5
        if (self.occupancy[4] == False):
            self.ui.OccupationB5.setText("Unoccupied")    
        else:
            self.ui.OccupationB5.setText("Occupied")
        #Block 6
        if (self.occupancy[5] == False):
            self.ui.OccupationB6.setText("Unoccupied")
        else:
            self.ui.OccupationB6.setText("Occupied")
        #Block 7
        if (self.occupancy[6] == False):
            self.ui.OccupationB7.setText("Unoccupied")
        else:
            self.ui.OccupationB7.setText("Occupied")
        #Block 8
        if (self.occupancy[7] == False):
            self.ui.OccupationB8.setText("Unoccupied")
        else:
            self.ui.OccupationB8.setText("Occupied")
        #Block 9
        if (self.occupancy[8] == False):
            self.ui.OccupationB9.setText("Unoccupied")
        else:
            self.ui.OccupationB9.setText("Occupied")
        #Block 10
        if (self.occupancy[9] == False):
            self.ui.OccupationB10.setText("Unoccupied")
        else:
            self.ui.OccupationB10.setText("Occupied")
        #Block 11
        if (self.occupancy[10] == False):
            self.ui.OccupationB11.setText("Unoccupied")
        else:
            self.ui.OccupationB11.setText("Occupied")
        #Block 12
        if (self.occupancy[11] == False):
            self.ui.OccupationB12.setText("Unoccupied")
        else:
            self.ui.OccupationB12.setText("Occupied")
        #Block 13
        if (self.occupancy[12] == False):
            self.ui.OccupationB13.setText("Unoccupied")
        else:
            self.ui.OccupationB13.setText("Occupied")
        #Block 14
        if (self.occupancy[13] == False):
            self.ui.OccupationB14.setText("Unoccupied")
        else:
            self.ui.OccupationB14.setText("Occupied")
        #Block 15
        if (self.occupancy[14] == False):
            self.ui.OccupationB15.setText("Unoccupied")
        else:
            self.ui.OccupationB15.setText("Occupied")
            
    #Set the authority displays        
    def AuthorityDisp(self):
        self.CalcNewAuthority()
        self.ui.AuthorityB1.setText(str(self.newAuthority[0]) + "ft")
        self.ui.AuthorityB2.setText(str(self.newAuthority[1]) + "ft")
        self.ui.AuthorityB3.setText(str(self.newAuthority[2]) + "ft")
        self.ui.AuthorityB4.setText(str(self.newAuthority[3]) + "ft")
        self.ui.AuthorityB5.setText(str(self.newAuthority[4]) + "ft")
        self.ui.AuthorityB6.setText(str(self.newAuthority[5]) + "ft")
        self.ui.AuthorityB7.setText(str(self.newAuthority[6]) + "ft")
        self.ui.AuthorityB8.setText(str(self.newAuthority[7]) + "ft")
        self.ui.AuthorityB9.setText(str(self.newAuthority[8]) + "ft")
        self.ui.AuthorityB10.setText(str(self.newAuthority[9]) + "ft")
        self.ui.AuthorityB11.setText(str(self.newAuthority[10]) + "ft")
        self.ui.AuthorityB12.setText(str(self.newAuthority[11]) + "ft")
        self.ui.AuthorityB13.setText(str(self.newAuthority[12]) + "ft")
        self.ui.AuthorityB14.setText(str(self.newAuthority[13]) + "ft")
        self.ui.AuthorityB15.setText(str(self.newAuthority[14]) + "ft")
    
    #Set the Suggested Speed displays
    def SugSpeedDisp(self):
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
        
    #Set the Switch State Disp
    def SwitchDisp(self):
        if(self.switchState == True):
            self.ui.SwitchDisp.setText("B")
        else:
            self.ui.SwitchDisp.setText("C")
    
    #Update the CTC Office Switch States
    def UpdateCTCSwitch(self, block):

        #Sends the Switch States
        signals.BlockNumber.emit(block)
        signals.Switch.emit(switchState)

    #Update the Track Model Authority and Suggested
    def UpdateTMStats(self, block):

    #Update the Track Model Switch State
    def UpdateTMSwitch(self,block):
    '''    
if __name__ == "__main__":
	app = QApplication(sys.argv)
	
	window = MainWindow()
	window.show()
	
	sys.exit(app.exec_())