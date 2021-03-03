import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from UI import Ui_MainWindow

#Define MainWindow class
class MainWindow(QMainWindow): #Subclass of QMainWindow

    #Constructor
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())



import xlrd

#Define Block class
class Block:

    #Constructor
    def __Init__(self, number, section, length, grade, speed_limit, elevation, cum_elevation):
        #Initialize Block instance variables
        self.number = number
        self.section = section
        self.length = length
        self.grade = grade
        self.speed_limit = speed_limit
        self.elevation = elevation
        self.cum_elevation = cum_elevation

    #Define Mutator Methods
    def setOccupancy(self, occupancy):
        self.occupancy = occupancy

    def setStatus(self, status):
        self.status = status

    #Define Accessor Methods
    def getNumber(Self):
        return self.number

    def getSection(Self):
        return self.section

    def getLength(self):
        return self.length

    def getGrade(self):
        return self.grade

    def getSpeedLimit(self):
        return self.speed_limit

    def getElevation(self):
        return self.elevation

    def getCumElevation(self):
        return self.cum_elevation

    def getOccupancy(self):
        return self.occupancy

    def getStatus(self):
        return self.status


#Define Switch Class
class Switch:

    #Constructor
    def __init__(self, root_block_num, branch_1_num, branch_2_num):
        #Initialize instance variable to hold root block number
        self.root_block_num = root_block_num

        #Initialize instance variable to hold branch block numbers
        self.branch_1_num = branch_1_num
        self.branch_2_num = branch_2_num

        #Initialize instance variable to hold current swtich position
        self.curr_position = branch_1_num

    #Define method to toggle switch position
    def TogglePosition(self):
        if self.curr_position == self.branch_1_num:
            self.curr_position = self.branch_2_num
        else:
            self.curr_position = self.branch_1_num


#Define TrackLine class
class Trackline:

    #Constructor
    def __init__(self, color, file_path):
        #Initialize color instance variable
        self.color = color

        #Initialize block composition of TrackLine
        self.TrackSetup(file_path)
    
    #Define method to establish track layout
    def TrackSetup(self, file_path):
        #Read from excel file





#Define Schedule class
class Schedule:

    #Constructor
    def __init__(self

class TrackLine

class TrackBlock

class Train