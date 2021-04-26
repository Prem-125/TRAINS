import sys
""" from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from .UI import Ui_TrackControllerUI """
from signals import signals

class TrackController:
    def __init__(self, offset):

        #Variables
        self.block_open = [True for i in range(150)]
        self.occupancy = [False for i in range(150)]
        self.authority = [True for i in range(150)]
        self.suggested_speed = [0 for i in range(150)]
        self.commanded_speed = [0 for i in range(150)]
        self.direction = [True for i in range(150)]
        self.block_offset = offset
        self.block_authority = 0
        self.crossing_signal = False
        self.crossing_pos = 0

        #Switch
        self.switch = Switch(-1,-1,-1)
        #UI used variables
        self.ui_block = 0

    #Sets the block offset for the track controller
    def setSwitch(self, block_num, branch_a, branch_b):
        self.switch.setValues(block_num, branch_a, branch_b)

    #Gets the occupancy
    def getOccupancy(self, block_num, occupied):
        self.getSugSpeed(block_num)
        self.occupancy[block_num-self.block_offset] = occupied        #Use block offset to set the occupancy
        self.setOfficeOccupancy(block_num, occupied)

        if(occupied == True):
            self.setTrackStats(block_num)

    #Update the CTC Office Occupancy
    def setOfficeOccupancy(self, block_num, occupied):
        print("\nSet the office occupancy function called\n")
        print("Occupied Block Number: " + str(block_num)+ "\n\n")
        signals.CTC_occupancy.emit("Green",block_num, occupied)    #Sends the Occupancy Signal

    #Gets the authority
    def getAuthority(self, block_num):
        self.authority[block_num-self.block_offset] = False
        self.block_authority = block_num

    #Gets the suggested speed
    def getSugSpeed(self, block_num):
        self.setComSpeed(block_num)

    #Gets the commanded speed
    def setComSpeed(self, block_num):
        for i in range(0, 25):
            self.commanded_speed[i] = 70
        for i in range(25, 30):
            self.commanded_speed[i] = 60
        for i in range(30, 36):
            self.commanded_speed[i] = 70
        for i in range(36, 41):
            self.commanded_speed[i] = 60

    #Update Track Model of the authority and commanded speed
    def setTrackStats(self, block_num):
        if(block_num == self.block_authority):
            signals.wayside_to_track.emit(block_num, 0, 0)
        else:
            signals.wayside_to_track.emit(block_num, 1, self.commanded_speed[block_num-self.block_offset])

    #Update the block closure
    def setBlockClosure(self, line, block_num, break_type):
        self.block_open[block_num-self.block_offset] = False
        self.UpdateCTCFailure(line, block_num, break_type)

    #Update the CTC Office of Block Closures
    def UpdateCTCFailure(self, line, block_num, break_type):
        signals.CTC_failure.emit(line, block_num, break_type)

    #Update the Track model of block openings
    def UpdateTMOpenings(self, line, block_num):
        signals.wayside_block_open.emit(line, block_num)

    #Update the block status
    def UpdateBlockStatus(self, line, block_num, status):
        self.block_open[block_num-self.block_offset] = status
        if(status == True):
            self.UpdateTMOpenings(line,block_num)

    #Turn on the crossing signal
    def ActivateCrossingSignal(self, block_num):
        #Forward
        if(self.direction[block_num] == True):
            if(self.crossing_pos == block_num+5):
                self.crossing_signal = True
                #send the crossing activate signal
        #backward
        elif(self.direction[block_num] == False):
            if(self.crossing_pos == block_num+5):
                self.crossing_signal = True
                #send the crossing activate signal

    #Turn off the crossing signal
    def DeactivateCrossingSignal(self, block_num):
        #Forward
        if(self.direction[block_num] == True):
            if(self.crossing_pos == block_num-1):
                self.crossing_signal = False
                #send the crossing deactivate signal
        #backward
        elif(self.direction[block_num] == False):
            if(self.crossing_pos == block_num+1):
                self.crossing_signal = False
                #send the crossing deactivate signal

    #Collision Detection
    def checkCollision(self, block_num):
        if(self.direction[block_num] == True):
            if(self.occupancy(block_num+1) == True):
                self.authority[block_num] =0
                #send signal
        if(self.direction[block_num] == False):
            if(self.occupancy(block_num-1) == True):
                self.authority[block_num] =0
                #send signal

    #Controls the Switch States
    '''
    def ControlSwitch(self):
    '''

class SwitchObj:
    def __init__(self, block_num, branch_a, branch_b):

        # Variables
        self.block = block_num
        self.branch_a = branch_a
        self.branch_b = branch_b
        self.cur_branch = -1

    def ToggleBranch(self):
        if(self.cur_branch == self.branch_a):
            self.cur_branch = self.branch_b
        elif(self.cur_branch == self.branch_b):
            self.cur_branch = self.branch_a

    def setValues(self, block, branch_a, branch_b):
        self.block = block
        self.branch_a = branch_a
        self.branch_b = branch_b
        self.cur_branch = branch_a
