mport sys
from signals import signals

# Describes the function of a Track Controller in the system
class TrackController:
    # Parameters are block offset, track line name, PLC tag
    def __init__(self, offset, line, tag):

        # Parameter Variables
        self.block_offset = offset
        self.line = line
        self.tag = tag

        # Adjacent Controllers
        self.adj_controller_list = [""]

        # Block Status Variables
        self.block_open = [True for i in range(150)]
        self.occupancy = [False for i in range(150)]
        self.authority = [True for i in range(150)]
        self.suggested_speed = [0 for i in range(150)]
        self.commanded_speed = [0 for i in range(150)]

        # Instantiate a switch
        self.switch = SwitchObj(-1,-1,-1,line)
        # Instantiate a crossing
        self.crossing = Crossing(-1)
        # Instantiate a PLC script
        self.plc_script = [PLCLine()]
        # Instantiate a block list
        self.block_list = []
        # Instantiate a list of upcoming route
        self.upcoming_blocks = [[] for i in range(150)]

        #UI used variables
        self.ui_block = 0

    # Initialize adjacent controllers
    # Parameter is a list of adjacent controllers
    def set_AdjacentControllers(self,adj_list):
        self.adj_controller_list.clear()
        self.adj_controller_list = adj_list

    # Add blocks to the list of blocks
    # Parameter is a block number
    def set_BlockList(self,block_num):
        self.block_list.append(block_num)
        
    # Sets upcoming blocks
    # Parameter is a list of the next four
    def set_UpcomingBlocks(self,block_num,next_four):
        if(block_num < len(self.upcoming_blocks)):
            self.upcoming_blocks[block_num] = next_four
    
    # Gets Upcoming Blocks
    # Parameter is a block number
    def get_UpcomingBlocks(self, block_num):
        if(block_num < len(self.upcoming_blocks)):
            return self.upcoming_blocks[block_num]
        else:
            return [0,0,0,0]

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
    # Parameter is block number and authority
    def get_Authority(self, block_num, authority):
        # Uses block offset to set the correct block
        self.authority[block_num-self.block_offset] = authority
        if(self.occupancy[block_num-self.block_offset+1] == True or self.occupancy[block_num-self.block_offset-1] == True):
            self.authority[block_num-self.block_offset] = False
        self.set_TrackStats(block_num)

    # Gets the suggested speed from the CTC office
    # Calls the commanded speed function
    # Parameters are block number, suggested speed, and speed limit
    def get_SugSpeed(self, block_num, sug_speed, limit):
        # Uses block offset to set the correct block
        self.suggested_speed[block_num-self.block_offset] = sug_speed
        self.set_ComSpeed(block_num, limit)
        print("Suggested Speed: " + str(sug_speed))

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
        self.set_TrackStats(block_num)

    # Update Track Model on the authority and commanded speed
    # Called upon when an occupancy is read
    # Parameter is block number
    def set_TrackStats(self, block_num):
        if(self.authority[block_num-self.block_offset] == False):
            signals.wayside_to_track.emit(self.line, block_num, 0, 0)
        else:
            signals.wayside_to_track.emit(self.line, block_num, 1, self.commanded_speed[block_num-self.block_offset])
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

    # Set PLC Script
    # Parameter is a list of PLC script
    def set_PLCScript(self, plc_script):
        self.plc_script.clear()
        for i in range (len(plc_script)):
            self.plc_script.append(plc_script[i])
    
    # RUN PLC
    def RunPLC(self, sent_tag):
        
        # Collision Instruction
        if(sent_tag == "COL"):
            output = True
            # Loops through all of the blocks on the block list
            for block_num in self.block_list:
                if(self.occupancy[block_num - self.block_offset] == True):
                    # Request the next four
                    signals.CTC_next_four_request.emit(self.line, block_num)
                    next_four = self.get_UpcomingBlocks(block_num)
                    for next_block in next_four:
                        # Checks current controller
                        if(self.occupancy[next_block - self.block_offset] == True):
                            output = False
                        # Checks adjacent track controllers
                        """for controller in self.adj_controller_list:
                            if(controller.occupancy[next_block - controller.block_offset] == True):
                                output = False"""
                    self.get_Authority(block_num, output)


        # Crossing Instruction
        elif(sent_tag == "CRX"):
            if(self.crossing.block != -1):
                # Loop through the lines of the PLC
                for i in range(len(self.plc_script)):
                    if(self.plc_script[i].elements[0] == "CRX"):
                        # Crossing Lights
                        if(self.plc_script[i+1].elements[0] == "LIT"):
                            light_dist = int(self.plc_script[i+1].elements[2])
                        # Crossing Gate
                        elif(self.plc_script[i+1].elements[0] == "GAT"):
                            gate_dist = int(self.plc_script[i+1].elements[2])
                        # Crossing Lights
                        if(self.plc_script[i+2].elements[0] == "LIT"):
                            light_dist = int(self.plc_script[i+2].elements[2])
                        # Crossing Gates
                        elif(self.plc_script[i+2].elements[0] == "GAT"):
                            gate_dist = int(self.plc_script[i+2].elements[2])
                        # Check Lights distance
                        for blocks in range(light_dist+1):
                            if(self.occupancy[self.crossing.block+blocks] == True):
                                signals.crossing_light_activation.emit(self.line, self.crossing.block, True)
                            elif(self.occupancy[self.crossing.block-blocks] == True):
                                signals.crossing_light_activation.emit(self.line, self.crossing.block, True)
                            else:
                                signals.crossing_light_activation.emit(self.line, self.crossing.block, False)
                        # Gate Activation/Deactivation
                        for blocks in range(gate_dist+1):
                            if(self.occupancy[self.crossing.block+blocks] == True):
                                signals.crossing_gate_activation.emit(self.line, self.crossing.block, True)
                            elif(self.occupancy[self.crossing.block-blocks] == True):
                                signals.crossing_gate_activation.emit(self.line, self.crossing.block, True)
                            else:
                                signals.crossing_gate_activation.emit(self.line, self.crossing.block, False)

        # Traffic Light Instruction
        elif(sent_tag == "TRL"):
            red_flag = False
            yel_flag = False
            # Loops through all of the blocks on the block list
            for block_num in self.block_list:    
                # Loop through the lines of the PLC
                for i in range(len(self.plc_script)):
                    if(self.plc_script[i].elements[0] == "TRL"):
                        
                        # Yellow Instruction
                        if(self.plc_script[i+1].elements[0] == "YEL"):
                            if(self.plc_script[i+1].elements[2] == "SW"):
                                sw_dist = self.plc_script[i+1].elements[3]
                                signals.CTC_next_four_request.emit(self.line, block_num)
                                next_four = self.get_UpcomingBlocks(block_num)
                                #if(sw_dist > 4):
                                    #for blk in range(4):

                            
                        # Red Instruction
                        elif(self.plc_script[i+1].elements[0] == "RED"):
                            if(self.plc_script[i+1].elements[2] == "NOT"):
                                if(self.plc_script[i+1].elements[3] == "AUT"):
                                    if(self.authority[block_num - self.block_offset] == False):
                                        red_flag = True

                        # Yellow Instruction
                        if(self.plc_script[i+2].elements[0] == "YEL"):
                            if(self.plc_script[i+2].elements[2] == "SW"):
                                sw_dist = int(self.plc_script[i+2].elements[3])
                                
                                
                        # Red Instruction
                        elif(self.plc_script[i+2].elements[0] == "RED"):
                            if(self.plc_script[i+2].elements[2] == "NOT"):
                                if(self.plc_script[i+2].elements[3] == "AUT"):        
                                    if(self.authority[block_num - self.block_offset] == False):
                                        red_flag = True

                # Logic for the switches
                if(red_flag == False):
                    if(yel_flag == False):
                        signals.wayside_signal_light.emit(self.line, block_num, 1)
                        # Send the yellow light signal
                    else:
                        signals.wayside_signal_light.emit(self.line, block_num, 0)
                        # Send the green light signal
                else:
                    signals.wayside_signal_light.emit(self.line, block_num, 2)
                    # Send the red light signal


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

# Class for the line of the PLC script
# Contains an element for each line
class PLCLine:
    def __init__(self):
        self.elements = ["" for i in range(10)]

    def set_element(self, iteration, element):
        self.elements[iteration] = element