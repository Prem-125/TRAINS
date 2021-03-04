import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from UI import Ui_TrackControllerUI

class MainWindow(QMainWindow):
    def __init__(self):
        #call parent constructor
        super(MainWindow, self).__init__()
        self.ui = Ui_TrackControllerUI()
        self.ui.setupUi(self)
        
        #Variables
        self.trackClosed = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        self.occupancy = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        self.authority = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.suggestedSpeed = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.switchState = True
        
        #Button Functions
        self.ui.CTCButton.clicked.connect(self.getCTCInputs)
        self.ui.TMButton.clicked.connect(self.getTMInputs)
        self.ui.OutputButton.clicked.connect(self.UpdateOutputs)
        self.ui.ClearButton.clicked.connect(self.ClearSystem)
        
        
    
    
    #Gets the CTC Inputs
    def getCTCInputs(self):
        if(self.ui.CTCBlockInput.toPlainText() == "1"):
            self.suggestedSpeed[0] = self.ui.SugSpeedInput.toPlainText()
            self.authority[0] = self.ui.AuthorityInput.toPlainText()
            if(self.ui.BlockStatusInput.toPlainText() == "Closed"):
                self.trackClosed[0] = True
            else:
                self.trackClosed[0] = False
        if(self.ui.CTCBlockInput.toPlainText() == "2"):
            self.suggestedSpeed[1] = self.ui.SugSpeedInput.toPlainText()
            self.authority[1] = self.ui.AuthorityInput.toPlainText()
            if(self.ui.BlockStatusInput.toPlainText() == "Closed"):
                self.trackClosed[1] = True
            else:
                self.trackClosed[1] = False 
        if(self.ui.CTCBlockInput.toPlainText() == "3"):
            self.suggestedSpeed[2] = self.ui.SugSpeedInput.toPlainText()
            self.authority[2] = self.ui.AuthorityInput.toPlainText()
            if(self.ui.BlockStatusInput.toPlainText() == "Closed"):
                self.trackClosed[2] = True
            else:
                self.trackClosed[2] = False
        if(self.ui.CTCBlockInput.toPlainText() == "4"):
            self.suggestedSpeed[3] = self.ui.SugSpeedInput.toPlainText()
            self.authority[3] = self.ui.AuthorityInput.toPlainText()
            if(self.ui.BlockStatusInput.toPlainText() == "Closed"):
                self.trackClosed[3] = True
            else:
                self.trackClosed[3] = False
        if(self.ui.CTCBlockInput.toPlainText() == "5"):
            self.suggestedSpeed[4] = self.ui.SugSpeedInput.toPlainText()
            self.authority[4] = self.ui.AuthorityInput.toPlainText()
            if(self.ui.BlockStatusInput.toPlainText() == "Closed"):
                self.trackClosed[4] = True
            else:
                self.trackClosed[4] = False
        if(self.ui.CTCBlockInput.toPlainText() == "6"):
            self.suggestedSpeed[5] = self.ui.SugSpeedInput.toPlainText()
            self.authority[5] = self.ui.AuthorityInput.toPlainText()
            if(self.ui.BlockStatusInput.toPlainText() == "Closed"):
                self.trackClosed[5] = True
            else:
                self.trackClosed[5] = False
        if(self.ui.CTCBlockInput.toPlainText() == "7"):
            self.suggestedSpeed[6] = self.ui.SugSpeedInput.toPlainText()
            self.authority[6] = self.ui.AuthorityInput.toPlainText()
            if(self.ui.BlockStatusInput.toPlainText() == "Closed"):
                self.trackClosed[6] = True
            else:
                self.trackClosed[6] = False     
        if(self.ui.CTCBlockInput.toPlainText() == "8"):
            self.suggestedSpeed[7] = self.ui.SugSpeedInput.toPlainText()
            self.authority[7] = self.ui.AuthorityInput.toPlainText()
            if(self.ui.BlockStatusInput.toPlainText() == "Closed"):
                self.trackClosed[7] = True
            else:
                self.trackClosed[7] = False 
        if(self.ui.CTCBlockInput.toPlainText() == "9"):
            self.suggestedSpeed[8] = self.ui.SugSpeedInput.toPlainText()
            self.authority[8] = self.ui.AuthorityInput.toPlainText()
            if(self.ui.BlockStatusInput.toPlainText() == "Closed"):
                self.trackClosed[8] = True
            else:
                self.trackClosed[8] = False    
        if(self.ui.CTCBlockInput.toPlainText() == "10"):
            self.suggestedSpeed[9] = self.ui.SugSpeedInput.toPlainText()
            self.authority[9] = self.ui.AuthorityInput.toPlainText()
            if(self.ui.BlockStatusInput.toPlainText() == "Closed"):
                self.trackClosed[9] = True
            else:
                self.trackClosed[9] = False  
        if(self.ui.CTCBlockInput.toPlainText() == "11"):
            self.suggestedSpeed[10] = self.ui.SugSpeedInput.toPlainText()
            self.authority[10] = self.ui.AuthorityInput.toPlainText()
            if(self.ui.BlockStatusInput.toPlainText() == "Closed"):
                self.trackClosed[10] = True
            else:
                self.trackClosed[10] = False     
        if(self.ui.CTCBlockInput.toPlainText() == "12"):
            self.suggestedSpeed[11] = self.ui.SugSpeedInput.toPlainText()
            self.authority[11] = self.ui.AuthorityInput.toPlainText()
            if(self.ui.BlockStatusInput.toPlainText() == "Closed"):
                self.trackClosed[11] = True
            else:
                self.trackClosed[11] = False
        if(self.ui.CTCBlockInput.toPlainText() == "13"):
            self.suggestedSpeed[12] = self.ui.SugSpeedInput.toPlainText()
            self.authority[12] = self.ui.AuthorityInput.toPlainText()
            if(self.ui.BlockStatusInput.toPlainText() == "Closed"):
                self.trackClosed[12] = True
            else:
                self.trackClosed[12] = False
        if(self.ui.CTCBlockInput.toPlainText() == "14"):
            self.suggestedSpeed[13] = self.ui.SugSpeedInput.toPlainText()
            self.authority[13] = self.ui.AuthorityInput.toPlainText()
            if(self.ui.BlockStatusInput.toPlainText() == "Closed"):
                self.trackClosed[13] = True
            else:
                self.trackClosed[13] = False
        if(self.ui.CTCBlockInput.toPlainText() == "15"):
            self.suggestedSpeed[14] = self.ui.SugSpeedInput.toPlainText()
            self.authority[14] = self.ui.AuthorityInput.toPlainText()
            if(self.ui.BlockStatusInput.toPlainText() == "Closed"):
                self.trackClosed[14] = True
            else:
                self.trackClosed[14] = False
            
            
            
    #gets the Track Model Inputs
    def getTMInputs(self):
        ...
    
    #Updates the Outputs
    def UpdateOutputs(self):
        ...
    
    #Clears the system
    def ClearSystem(self):
        self.trackClosed = [False, False, False, False, False, False, False, False, False, False, False, False,  False, False, False]
        self.occupancy = [False, False, False, False, False, False, False, False, False, False, False, False,  False, False, False]
        self.authority = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.suggestedSpeed = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.switchState = True
        self.TrackStatDisp
        self.OccupancyDisp
        self.AuthorityDisp
        self.SugSpeedDisp
        self.UpdateOutputs
    
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
            self.ui.OccupancyB1.setText("Unoccupied")
        else:
            self.ui.OccupancyB1.setText("Occupied")
        #Block 2
        if (self.occupancy[1] == False):
            self.ui.OccupancyB2.setText("Unoccupied")
        else:
            self.ui.OccupancyB2.setText("Occupied")
        #Block 3
        if (self.occupancy[2] == False):
            self.ui.OccupancyB3.setText("Unoccupied")
        else:
            self.ui.OccupancyB3.setText("Occupied")
        #Block 4
        if (self.occupancy[3] == False):
            self.ui.OccupancyB4.setText("Unoccupied")
        else:
            self.ui.OccupancyB4.setText("Occupied")
        #Block 5
        if (self.occupancy[4] == False):
            self.ui.OccupancyB5.setText("Unoccupied")    
        else:
            self.ui.OccupancyB5.setText("Occupied")
        #Block 6
        if (self.occupancy[5] == False):
            self.ui.OccupancyB6.setText("Unoccupied")
        else:
            self.ui.OccupancyB6.setText("Occupied")
        #Block 7
        if (self.occupancy[6] == False):
            self.ui.OccupancyB7.setText("Unoccupied")
        else:
            self.ui.OccupancyB7.setText("Occupied")
        #Block 8
        if (self.occupancy[7] == False):
            self.ui.OccupancyB8.setText("Unoccupied")
        else:
            self.ui.OccupancyB8.setText("Occupied")
        #Block 9
        if (self.occupancy[8] == False):
            self.ui.OccupancyB9.setText("Unoccupied")
        else:
            self.ui.OccupancyB9.setText("Occupied")
        #Block 10
        if (self.occupancy[9] == False):
            self.ui.OccupancyB10.setText("Unoccupied")
        else:
            self.ui.OccupancyB10.setText("Occupied")
        #Block 11
        if (self.occupancy[10] == False):
            self.ui.OccupancyB11.setText("Unoccupied")
        else:
            self.ui.OccupancyB11.setText("Occupied")
        #Block 12
        if (self.occupancy[11] == False):
            self.ui.OccupancyB12.setText("Unoccupied")
        else:
            self.ui.OccupancyB12.setText("Occupied")
        #Block 13
        if (self.occupancy[12] == False):
            self.ui.OccupancyB13.setText("Unoccupied")
        else:
            self.ui.OccupancyB13.setText("Occupied")
        #Block 14
        if (self.occupancy[13] == False):
            self.ui.OccupancyB14.setText("Unoccupied")
        else:
            self.ui.OccupancyB14.setText("Occupied")
        #Block 15
        if (self.occupancy[14] == False):
            self.ui.OccupancyB15.setText("Unoccupied")
        else:
            self.ui.OccupancyB15.setText("Occupied")
            
    #Set the authority displays        
    def AuthorityDisp(self):
        self.ui.AuthorityB1.setText(self.authority[0].toPlainText())
        self.ui.AuthorityB2.setText(self.authority[1].toPlainText())
        self.ui.AuthorityB3.setText(self.authority[2].toPlainText())
        self.ui.AuthorityB4.setText(self.authority[3].toPlainText())
        self.ui.AuthorityB5.setText(self.authority[4].toPlainText())
        self.ui.AuthorityB6.setText(self.authority[5].toPlainText())
        self.ui.AuthorityB7.setText(self.authority[6].toPlainText())
        self.ui.AuthorityB8.setText(self.authority[7].toPlainText())
        self.ui.AuthorityB9.setText(self.authority[8].toPlainText())
        self.ui.AuthorityB10.setText(self.authority[9].toPlainText())
        self.ui.AuthorityB11.setText(self.authority[10].toPlainText())
        self.ui.AuthorityB12.setText(self.authority[11].toPlainText())
        self.ui.AuthorityB13.setText(self.authority[12].toPlainText())
        self.ui.AuthorityB14.setText(self.authority[13].toPlainText())
        self.ui.AuthorityB15.setText(self.authority[14].toPlainText())
    
    #Set the Suggested Speed displays
    def SugSpeedDisp(self):
        self.ui.SugSpeedB1.setText(self.suggestedSpeed[0].toPlainText())
        self.ui.SugSpeedB2.setText(self.suggestedSpeed[1].toPlainText())
        self.ui.SugSpeedB3.setText(self.suggestedSpeed[2].toPlainText())
        self.ui.SugSpeedB4.setText(self.suggestedSpeed[3].toPlainText())
        self.ui.SugSpeedB5.setText(self.suggestedSpeed[4].toPlainText())
        self.ui.SugSpeedB6.setText(self.suggestedSpeed[5].toPlainText())
        self.ui.SugSpeedB7.setText(self.suggestedSpeed[6].toPlainText())
        self.ui.SugSpeedB8.setText(self.suggestedSpeed[7].toPlainText())
        self.ui.SugSpeedB9.setText(self.suggestedSpeed[8].toPlainText())
        self.ui.SugSpeedB10.setText(self.suggestedSpeed[9].toPlainText())
        self.ui.SugSpeedB11.setText(self.suggestedSpeed[10].toPlainText())
        self.ui.SugSpeedB12.setText(self.suggestedSpeed[11].toPlainText())
        self.ui.SugSpeedB13.setText(self.suggestedSpeed[12].toPlainText())
        self.ui.SugSpeedB14.setText(self.suggestedSpeed[13].toPlainText())
        self.ui.SugSpeedB15.setText(self.suggestedSpeed[14].toPlainText())
        
    #Set the Switch State Disp
    def SwitchDisp(self):    
        if(switchState == True):
            self.ui.SwitchDisp.setText(self.switchState.setText("B"))
        else:
            self.ui.SwitchDisp.setText(self.switchState.setText("C"))
        
        
if __name__ == "__main__":
	app = QApplication(sys.argv)
	
	window = MainWindow()
	window.show()
	
	sys.exit(app.exec_())