import sys
from signals import signals

# Describes the function of a Track Controller in the system
class TrackController:
    # Parameters are block offset, track line name, PLC tag
    def __init__(self, offset, line, tag):

        # Parameter Variables
        self.block_offset = offset
        self.line = line
        self.tag = tag

        # Block Status Variables
        self.block_open = [True for i in range(150)]
        self.occupancy = [False for i in range(150)]
        self.authority = [True for i in range(150)]
        self.suggested_speed = [0 for i in range(150)]
        self.commanded_speed = [0 for i in range(150)]
        self.direction = [True for i in range(150)]

        # Instantiate a switch
        self.switch = SwitchObj(-1,-1,-1,line)
        # Instantiate a crossing
        self.crossing = Crossing(-1)

        #UI used variables
        self.ui_block = 0

    # Initializes the switch values, calling the switch function
    # Parameters are block number, branch a, branch b, and track line name
    def set_Switch(self, block_num, branch_a, branch_b, line):
        self.switch.set_Values(block_num, branch_a, branch_b, line)

    # Initializes the crossing value, calling the crossing function
    # Parameter is block number
    def set_Crossing(self, block_num):
        self.crossing.set_Crossing(block_num)

    # Sets the occupancy of the respective block
    # Parameters are block number and boolean occupied status
    def set_Occupancy(self, block_num, occupied):
        # Uses block offset to set the correct block
        self.occupancy[block_num-self.block_offset] = occupied

        # Updates the CTC Office occupancy
        self.set_OfficeOccupancy(block_num, occupied)

        # Calls Track stats for occupied block
        if(occupied == True):
            self.set_TrackStats(block_num)

    # Sends a signal to the CTC Office to update the Office of an occupancy
    # Parameters are block number and boolean occupied status
    def set_OfficeOccupancy(self, block_num, occupied):
        signals.CTC_occupancy.emit("Green",block_num, occupied)

    # Sets the authority of the block
    # Parameter is block number
    def get_Authority(self, block_num):
        # Uses block offset to set the correct block
        self.authority[block_num-self.block_offset] = False

    # Gets the suggested speed from the CTC office
    # Calls the commanded speed function
    # Parameters are block number, suggested speed, and speed limit
    def get_SugSpeed(self, block_num, sug_speed, limit):
        # Uses block offset to set the correct block
        self.suggested_speed[block_num-self.block_offset] = sug_speed
        self.set_ComSpeed(block_num, limit)

    # Calculates the commanded speed
    # If the speed limit is less than the suggested speed, commanded becomes the limit
    # Otherwise, the commanded speed is the suggested speed
    # Parameters are block number and speed limit
    def set_ComSpeed(self, block_num, limit):
        # Uses block offset to set the correct block
        if(self.suggested_speed[block_num-self.block_offset] > limit):
            self.commanded_speed[block_num-self.block_offset] = limit
        else:
            self.commanded_speed[block_num - self.block_offset] = self.suggested_speed[block_num-self.block_offset]

    # Update Track Model on the authority and commanded speed
    # Called upon when an occupancy is read
    # Parameter is block number
    def set_TrackStats(self, block_num):
        if(self.authority[block_num-self.offset] == False):
            signals.wayside_to_track.emit(block_num, 0, 0)
        else:
            signals.wayside_to_track.emit(block_num, 1, self.commanded_speed[block_num-self.block_offset])
            print("Suggested Speed: " + str(self.commanded_speed[block_num-self.block_offset]))

    # Closes a block after a received signal
    # sets the occupancy of the block to occupied
    # Updates the CTC Office on the closed block
    # Parameters are track line name, block number and break type
    def set_BlockClosure(self, line, block_num, break_type):
        # Uses block offset to set the correct block
        self.block_open[block_num-self.block_offset] = False
        self.occupancy[block_num-self.block_offset] = True
        self.UpdateCTCFailure(line, block_num, break_type)

    # Update the CTC Office of Block Closures
    # Parameters are track line name, block number and break type
    def UpdateCTCFailure(self, line, block_num, break_type):
        signals.CTC_failure.emit(line, block_num, break_type)

    # Update the Track model of block openings
    # Parameters are track line name and block number
    def UpdateTMOpenings(self, line, block_num):
        signals.wayside_block_open.emit(line, block_num)

    # Update the block status
    # If the block is open, update the Track Model and occupancy
    # Parameters are track line name, block number and break status
    def UpdateBlockStatus(self, line, block_num, status):
        # Uses block offset to set the correct block
        self.block_open[block_num-self.block_offset] = status
        if(status == True):
            self.UpdateTMOpenings(line,block_num)
            self.occupancy[block_num - self.block_offset] = False

    # Crossing Handler
    # Parameter is block number
    def CrossingHandler(self, block_num, direction):
        # Forwards activation and deactivation
        if(direction == True):
            distance = self.crossing.block-block_num
            if(distance <4 and distance >= 0):
                self.crossing.ActivateCrossing(distance)
            else:
                self.crossing.DeactivateCrossing()
        # Backwards activation and deactivation
        else:
            distance = block_num-self.crossing.block
            if(distance <4 and distance >= 0):
                self.crossing.ActivateCrossing(distance)
            else:
                self.crossing.DeactivateCrossing()

    # Switch Handler
    # Parameter is block number
    def SwitchHandler(self, block_num, direction):
        if(block_num == self.switch.block):
            if(direction == True):
                if(self.switch.cur_branch == self.switch.branch_b):
                    self.switch.ToggleBranch()
            elif(direction == False):
                if(self.switch.cur_branch == self.switch.branch_a):
                    self.switch.ToggleBranch()
        elif(block_num == self.switch.branch_a and self.authority[block_num-self.offset] == True):
            if(self.switch.branch_b == self.switch.cur_branch):
                self.switch.ToggleBranch()
        elif(blokc_num == self.switch.branch_a and self.authority[block_num-self.offset] == True):
            if(self.switch.branch_a == self.switch.cur_branch):
                self.switch.ToggleBranch()

    # Collision Detection
    # Parameter is block number
    def CheckCollision(self, block_num, direction):
        if(direction == True):
            if(self.occupancy(block_num-self.offset+1) == True):
                self.authority[block_num-self.offset] = False
                #send signal
        if(direction == False):
            if(self.occupancy(block_num-self.offset-1) == True):
                self.authority[block_num-self.offset] = False
                #send signal

# Describes the function of a Switch under jurisdiction of a Track Controller
class SwitchObj:
    # Parameters are block number, branch a, branch b, track line name
    def __init__(self, block_num, branch_a, branch_b, line):

        # Variables
        self.block = block_num
        self.branch_a = branch_a
        self.branch_b = branch_b
        self.cur_branch = -1
        self.line = ""

    # Toggles the current branch of the switch
    # Sends the signal to the Track Model and CTC Office
    def ToggleBranch(self):
        if(self.cur_branch == self.branch_a):
            self.cur_branch = self.branch_b
        elif(self.cur_branch == self.branch_b):
            self.cur_branch = self.branch_a
        signals.track_switch_position.emit(self.line, self.block, self.cur_branch)
        signals.CTC_switch_position.emit(self.line, self.block, self.cur_branch)
        print('emmit toggle' + self.line)

    # Establishes the value of the stems and branches
    def set_Values(self, block, branch_a, branch_b, line):
        self.block = block
        self.branch_a = branch_a
        self.branch_b = branch_b
        self.cur_branch = branch_a
        self.line = line
        signals.track_switch_position.emit(self.line, self.block, self.cur_branch)
        #signals.CTC_switch_position.emit(self.line, self.block, self.cur_branch)

# Describes the function of a Crossing under jurisdiction of a Track Controller
class Crossing:
    # Parameter is block number
    def __init__(self, block_num):
        self.block = block_num
        self.traffic_light = 0
        self.light = False
        self.gate = False
    
    # Sets the value of the crossing
    # Parameter is block number
    def set_Crossing(self, block_num):
        self.block = block_num

    # Activates the traffic light at the railway crossing
    # Activates the crossing light and gate
    # Parameter is distance from block
    def ActivateCrossing(self, distance):
        if(distance > 3):
            self.traffic_light = 0
        elif(distance == 3):
            self.traffic_light = 1
        elif(distance <= 2):
            self.traffic_light = 2
            self.light = True
            self.gate = True
    
    # Deactivates the traffic light at the railway crossing
    # Deactivates the crossing light and gate
    def DeactivateCrossing(self):
        self.traffic_light = 0
        self.light = False
        self.gate = False