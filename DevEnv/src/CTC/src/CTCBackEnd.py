import xlrd
from PySide6.QtCore import *
from signals import signals

#Define Block class
class Block:

    #Constructor
    def __init__(self, block_number, track_section, block_length, block_speed_limit):
        #Initialize Block instance variables
        self.number = block_number   #Integer
        self.section = track_section #String
        self.length = block_length   #Meters
        self.speed_limit = block_speed_limit #Meters/Second
        self.occupancy = 0
        self.status = True

        #Compute fastest traveral time in seconds
        self.min_traveral_time = round(block_length / block_speed_limit , 2)

    #End contructor

#End Block class definition


#Define Switch Class
class Switch:

    #Constructor
    def __init__(self, block_num_0, block_num_1, block_num_2):
        #Initialize instance variable to hold block number at which switch is rooted
        self.root = block_num_0
        #Initialize instance variables to hold branch block numbers
        self.branch_1 = block_num_1
        self.branch_2 = block_num_2

        #Initialize instance variable to hold current switch position
        self.curr_position = block_num_1
    #End contructor

    #Define method to toggle switch position
    def TogglePosition(self):
        if self.curr_position == self.branch_1:
            self.curr_position = self.branch_2
        else:
            self.curr_position = self.branch_1
        #End if-else block
    #End method

#End Switch class definition


#Define Station class
class Station:

    #Constructor
    def __init__(self, station_name, assoc_block_num):
        #Initialize instance variable to hold name of station
        self.name = station_name
        #Initialize instance variable to hold block number to which station is belongs
        self.block_num = assoc_block_num
    #End constructor

#End Station class definition


#Define Train class
class Train:

    #Constructor
    def __init__(self, train_number, block_destination, TrackLineObj, train_arrival_time, train_departure_time):
        #Initialize Block instance variables
        self.number = train_number
        self.destination = block_destination #Block Number
        self.HostTrackLine = TrackLineObj #String
        self.arrival_time = train_arrival_time     #Seconds
        self.departure_time = train_departure_time #Seconds
        
        #Initialize route queue
        self.route_queue = []
        if(self.HostTrackLine.color == "Green"):
            self.GenerateGreenRoute()
            print("\nCTC- ROUTE QUEUE HAS BEEN GENERATED")
        elif(self.HostTrackLine.color == "Red"):
            self.GenerateRedRoute()

        #Connect signal to obtain occupancy from wayside controller
        signals.CTC_occupancy.connect(self.UpdatePosition)

        #Configure single shot timer for dwell period at destinations
        """
        self.dwell_timer = QTimer()
        self.dwell_timer.setSingleShot(True)
        self.dwell_timer.timeout.connect(self.LeaveStation)
        """
        
    #End contructor

    #Method to populate queue structure that specifies train route for Green line
    def GenerateGreenRoute(self):
        #Train always begins at yard
        self.route_queue.append(0)

        #Specify blocks for track sections K through Q
        for block_num in range(63, 101):
            self.route_queue.append(block_num)

        #Specify blocks for track section N in reverse
        for block_num in range(85, 76, -1):
            self.route_queue.append(block_num)

        #Specify blocks for track secionts R through Z
        for block_num in range(101, 151):
            self.route_queue.append(block_num)

        #Specify blocks for track sections A through F in reverse
        for block_num in range(28, 0, -1):
            self.route_queue.append(block_num)
        
        #Specify blocks for track sections D through I
        for block_num in range(13, 58):
            self.route_queue.append(block_num)

        #Train ends at yard by default
        self.route_queue.append(0)
    #End method

    #Method to populate queue structure that specifies train route for Red line
    def GenerateRedRoute(self):
        #Train always begins at yard
        self.route_queue.append(0)

        #Specify blocks for track sections A, B, C in reverse
        for block_num in range(9, 0, -1):
            self.route_queue.append(block_num)

        #Specify blocks for track sections F through N
        for block_num in range(16, 67):
            self.route_queue.append(block_num)

        #Specify blocks for part of H, I, and part of J in reverse
        for block_num in range(52, 42, -1):
            self.route_queue.append(block_num)

        #Specify blocks for track sections O through Q
        for block_num in range(67, 72):
            self.route_queue.append(block_num)

        #Specify blocks for part of H in reverse
        for block_num in range(38, 31, -1):
            self.route_queue.append(block_num)

        #Specify blocks for track sections R through T
        for block_num in range(72, 77):
            self.route_queue.append(block_num)

        #Specify blocks for F, G, and part of H in reverse
        for block_num in range(27, 15, -1):
            self.route_queue.append(block_num)

        #Specify blocks for track sections D and E in reverse
        for block_num in range(15, 9, -1):
            self.route_queue.append(block_num)

        #Train ends always ends at yard
        self.route_queue.append(0)
    #End method

    """
    #Method to invoke backend functions for train position and suggested speed
    def UpdateTrainParameters(self, track_line_name, block_num, occupancy):
        #Send occupancy information to each train
        if(track_line_name == "Green"):
            for TrainObj in CTCSchedule.train_list:
                TrainObj.UpdatePosition(GreenLine, block_num, occupancy)
            #End for loop
        elif(track_line_name == "Red"):
            for TrainObj in CTCSchedule.train_list:
                TrainObj.UpdatePosition(RedLine, block_num, occupancy)
            #End for loop
        #End if-elif block
    #End method
    """

    #Method to update position of train
    def UpdatePosition(self, track_line_name, block_num, occupancy):
        print("ENTERED UPDATE TRAIN POSITION FUNCTION")
        print("COMPARING " + str(block_num) + " WITH " + str(self.route_queue[1]) + " ON QUEUE")
        #Determine if occupancy corresponds to movement of self
        if(occupancy == True and block_num == self.route_queue[1] and self.HostTrackLine.color == track_line_name):
            #Dequeue from list
            self.route_queue.pop(0)
            print("\nCTC- QUEUE HAS BEEN POPPED\n")

            #ATTENTION: Delete train if loop is complete

            #Update suggested speed according to train position
            if(self.destination == self.route_queue[3]):
                suggested_speed = int(.75*self.HostTrackLine.block_list[self.route_queue[0]-1].speed_limit)
                signals.CTC_suggested_speed.emit(self.HostTrackLine.color, self.route_queue[0], suggested_speed*3.60)
            elif(self.destination == self.route_queue[2]):
                suggested_speed = int(.50*self.HostTrackLine.block_list[self.route_queue[0]-1].speed_limit)
                signals.CTC_suggested_speed.emit(self.HostTrackLine.color, self.route_queue[0], suggested_speed*3.60)
            elif(self.destination == self.route_queue[1]):
                suggested_speed = int(.25*self.HostTrackLine.block_list[self.route_queue[0]-1].speed_limit)
                signals.CTC_suggested_speed.emit(self.HostTrackLine.color, self.route_queue[0], suggested_speed*3.60)
            elif(self.destination == self.route_queue[0]):
                suggested_speed = int(0*self.HostTrackLine.block_list[self.route_queue[0]-1].speed_limit)
                signals.CTC_suggested_speed.emit(self.HostTrackLine.color, self.route_queue[0], suggested_speed*3.60) 

                #Send authority to track controller
                signals.CTC_authority.emit(self.HostTrackLine.color, self.destination, False)  

                #Start dwell timer
                QTimer.singleShot(6000, self.LeaveStation)
                print("\n\nTIMER HAS BEEN STARTED\n\n")
            else:
                suggested_speed = self.HostTrackLine.block_list[self.route_queue[0]-1].speed_limit
                signals.CTC_suggested_speed.emit(self.HostTrackLine.color, self.route_queue[0], suggested_speed*3.60)   
    #End method

    #Method to alert train to leave station after dwell period has expired
    def LeaveStation(self):
        #Send authority to track controller
        signals.CTC_authority.emit(self.HostTrackLine.color, self.destination, True)
        print("\nHIT1\n")
        suggested_speed = self.HostTrackLine.block_list[self.route_queue[0]-1].speed_limit
        print("\nHIT2\n")
        signals.CTC_suggested_speed.emit(self.HostTrackLine.color, self.route_queue[0], suggested_speed*3.60)
        print("\nHIT3\n")
    #End method
    
#End Train class definition


#Define TrackLine class
class TrackLine:

    #Constructor
    def __init__(self, filepath, sheet_index):
        #Declare a list of track blocks
        self.block_list = []
        #Declare a list of switches
        self.switch_list = []
        #Declare a list of stations
        self.station_list = []

        #Obtain ticket sales from TrackModel
        signals.station_ticket_sales.connect(self.UpdateTicketSales)

        #Obtain occupancy from wayside controller
        signals.CTC_occupancy.connect(self.UpdateOccupancy)

        #Obtain switch position from wayside controller
        signals.CTC_switch_position.connect(self.UpdateSwitchPos)

        #Initialize block composition of TrackLine
        self.TrackSetup(filepath, sheet_index)

        #Initialize instance variable to hold the total number of tickets sold on track line
        self.ticket_sales = 0

        #Declare a list of closed blocks
        self.closed_blocks = []

        """
        print("INITIAL SWITCH LAYOUT FOR " + str(self.color) + "LINE")

        for SwitchObj in self.switch_list:
            print("Switch on Block " + str(SwitchObj.root) + " with Branches " + str(SwitchObj.branch_1) + " and " + str(SwitchObj.branch_2))
        """

        print("\n\nSTATION CONFIGURATION FOR GREENLINE")
        for StationObj in self.station_list:
            print("Station " + StationObj.name + " is on block " + str(StationObj.block_num))

    #End contructor

    #Define method to establish track layout
    def TrackSetup(self, filepath, sheet_index):
        #Open excel file
        exl_workbook = xlrd.open_workbook(filepath)
        #Navigate to specified excel sheet within file
        exl_sheet = exl_workbook.sheet_by_index(sheet_index)

        #Initialize color instance variable
        self.color = exl_sheet.cell_value(1, 0)

        #Loop through contents of sheet row-wise
        for i in range(1, exl_sheet.nrows): #Skip first row of column headers

            #All valid track layout spreadsheets have 10 columns per row

            #Initialize temporary variables to hold cell contents of current row
            track_section = exl_sheet.cell_value(i, 1) 
            block_num = int(exl_sheet.cell_value(i, 2))
            block_length = int(exl_sheet.cell_value(i, 3))      #Meters
            block_speed_limit = int(exl_sheet.cell_value(i, 5)) * .27778 #Kilometers/Hour

            #Create new block and append to list
            self.block_list.append( Block(block_num, track_section, block_length, block_speed_limit) )

            #Obtain infrastructure associated with current block
            block_infra = exl_sheet.cell_value(i, 6)

            #Check if current block is the root of a switch or station
            if('YARD' in block_infra):
                #Infrascture cell will specify the root block number

                #Initialize temporary string to hold block numbers associated with the switch
                temp_str = ''

                #Capture block numbers from the infrastructure cell
                for character in block_infra:
                    #Form block numbers from component digits while eliminating all other characters
                    if(character.isdigit()):
                        temp_str += character
                        continue
                
                root_block_num = int(temp_str)

                #Create new switch and append to list
                self.switch_list.append( Switch(root_block_num, 0, block_num) )
                #Yard is arbitrarily assigned block number of zero
                #Other branch of switch is the current block

            elif('SWITCH' in block_infra):
                #Infrascture cell will specify the block connections formed by the switch

                #Declare temporary list of numerical values in infrastructure string
                branch_block_nums = []

                #Initialize temporary string to hold block numbers associated with the switch
                temp_str = ''

                #Capture block numbers from the infrastructure cell
                for character in block_infra:
                    #Form block numbers from component digits while eliminating all other characters
                    if(character.isdigit()):
                        temp_str += character
                        continue
                    
                    #Identify root block and branching blocks for switch
                    if(temp_str != ''):
                        if(int(temp_str) in branch_block_nums): #Isolate root block
                            branch_block_nums.remove( int(temp_str) )
                            root_block_num = int(temp_str)
                        else: #Store branch blocks in list
                            branch_block_nums.append( int(temp_str) )
                        #End if-else block

                    #Reset temporary string
                    temp_str = ''
                #End for loop

                #Create new switch and append to list
                self.switch_list.append( Switch(root_block_num, branch_block_nums[0], branch_block_nums[1]) )

            elif('STATION' in block_infra):
                #Capture station name from the infrastructure cell
                parsed_block_infra = block_infra.split('; ')
                station_name = parsed_block_infra[1]

                #Determine block at which station is rooted
                assoc_block_num = block_num

                #Reset flag variable
                duplicate = False

                #Determine if station has already been created
                for stationObj in self.station_list:
                    if(stationObj.name == station_name):
                        duplicate = True
                        break

                #ATTENTION: Allow for creation of duplicate station
                
                #Do not create duplicate station
                if(duplicate == True):
                    continue
                

                #Create new station and append to list
                self.station_list.append( Station(station_name, assoc_block_num) )

            #End if-elif block
        #End for loop

        #Close xlrd workbook
        exl_workbook.release_resources()

    #End method

    #Method to update ticket count
    def UpdateTicketSales(self, track_line_name, new_ticket_sales):
        #Add new ticket sales to total ticket sales
        if(track_line_name == self.color):
            self.ticket_sales += new_ticket_sales
    #End method

    #Method to compute throughput
    def ComputeThroughput(self, curr_time):
        #Recompute throughput
        throughput = self.ticket_sales / curr_time

        return throughput
    #End method

    #Method to update block occupancy
    def UpdateOccupancy(self, track_line_name, block_number, block_occupancy):
        #Determine if occupancy signal corresponds to self
        if(track_line_name == self.color):
            self.block_list[block_number-1].occupancy = block_occupancy
        #End if
    #End method

    #Method to update switch position
    def UpdateSwitchPos(self, track_line_name, root_block_num, branch_block_num):

        print("Zack sends Switch on Block " + str(root_block_num) + " of " + track_line_name + " connected to block " + str(branch_block_num))

        #Search switch list
        for SwitchObj in self.switch_list:
            if(self.color == track_line_name and SwitchObj.root == root_block_num):
                print("Switch on Block " + str(root_block_num) + " was at position " + str(SwitchObj.curr_position))
                SwitchObj.curr_position = branch_block_num
                print("Switch on Block " + str(root_block_num) + " is now at position " + str(SwitchObj.curr_position))
            #End if
        #End for loop
    #End method

#End TrackLine class definition


#Define Schedule class
class Schedule:

    #Constructor
    def __init__(self):
        #Initialize operational mode to manual
        self.mode = "manual"

        #Declare a list of trains
        self.train_list = []
    #End constructor

    #Define method for manual train dispatch
    def ManualSchedule(self, block_destination, train_arrival_time, TrackLineObj, curr_time):
        global gbl_seconds
        
        #Assign train number
        train_number = len(self.train_list) + 1

        #Compute train travel time
        travel_time = self.ComputeTravelTime(block_destination, train_arrival_time, TrackLineObj)

        print("TRAVEL TIME: " + str(travel_time))

        #Compute train departure time
        train_departure_time = train_arrival_time - travel_time

        #Determine if specified arrival time is valid
        if(train_departure_time < curr_time):
            return False

        #Determine if computed depature time matches that of another train
        for trainObj in self.train_list:
            if(trainObj.departure_time == train_departure_time):
                return False

        """
        #Determine if specified destination is valid
        if(TrackLineObj.color == "Green"):
            if(block_destination < 1 or block_destination > 150):
                return False
        elif(TrackLineObj.color == "Red"):
            if(block_destination < 1 or block_destination > 76):
                return False
        """
        
        #If travel parameters have been verified, add train object to the schedule's train list
        self.train_list.append( Train(train_number, block_destination, TrackLineObj, train_arrival_time, train_departure_time) )

        return True
    #End method

    #Define method to compute departure time for train
    def ComputeTravelTime(self, block_destination, train_arrival_time, TrackLineObj):
        #Initialize temporary accumulation variable for travel time
        travel_time = 0

        #Determine if the train is to dispatched on the Green or Red lines
        if(TrackLineObj.color == "Green"):
            #Destination is located on sections K through Q
            if(block_destination >= 63 and block_destination <= 100):
                for i in range(63, block_destination):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

            #Destination is located on sections R though Z
            elif(block_destination >= 101 and block_destination <= 150):
                for i in range(63, 101):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

                #Section N is traversed twice
                for i in range(77, 86):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

                for i in range(101, block_destination):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time
            
            #Destination is located on sections A through F
            elif(block_destination >= 1 and block_destination <= 28):
                for i in range(63, 151):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

                #Section N is traversed twice
                for i in range(77, 86):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

                #Sections A through F are initially travelled in reverse
                for i in range(28, block_destination, -1):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

            #Destination is located on sections G through J
            elif(block_destination >= 29 and block_destination <= 62):
                for i in range(63, 151):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

                #Section N is traversed twice
                for i in range(77, 86):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

                for i in range(1, 29):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time
                
                #Sections D, E, and F are traversed twice
                for i in range(13, 29):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

                for i in range(29, block_destination):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

            #End if-elif block for Green line

        elif(TrackLineObj.color == "Red"):
            #Destination is located on sections A through C
            if(block_destination >= 1 and block_destination <= 9):
                #Sections A through C are initially travelled in reverse
                for i in range(9, block_destination, -1):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

            #Destination is located on sections F though N
            elif(block_destination >= 16 and block_destination <= 66):
                for i in range(1, 10):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

                for i in range(16, block_destination):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time
            
            #Destination is located on sections O through Q
            elif(block_destination >= 67 and block_destination <= 71):
                for i in range(1, 67):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

                #Section I and part of section J and H are traversed twice
                for i in range(43, 53):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

                for i in range(67, block_destination):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

            #Destination is located on sections R through T
            elif(block_destination >= 72 and block_destination <= 76):
                for i in range(1, 71):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

                #Section I and part of section J and H are traversed twice
                for i in range(43, 53):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

                #Part of section H is traversed twice
                for i in range(43, 46):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

                for i in range(72, block_destination):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

            #Destination is located on sections D or E
            elif(block_destination >= 10 and block_destination <= 15):
                for i in range(1, 77):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

                #Section I and part of section J and H are traversed twice
                for i in range(43, 53):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

                #Part of section H is traversed twice
                for i in range(43, 46):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

                #F, G, and part of section H are traversed twice
                for i in range(16, 28):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

                for i in range(15, block_destination, -1):
                    travel_time += TrackLineObj.block_list[i-1].min_traveral_time

        #End if-elif block for Red line

        #Return travel time back to calling environment
        return travel_time
    #End method

    #Define method to check if a scheduled train needs to be dispatched
    def CheckForDispatch(self, curr_time):
        #Loop through train list to inspect departure times
        for trainObj in self.train_list:
            if(int(trainObj.departure_time) == curr_time):
                #MUST COMPELTE: Inform Train Deployer of newly created train object
                signals.train_creation.emit(trainObj.HostTrackLine.color, trainObj.number)
                break

        

        #MUST COMPLETE: Send authority to track controller as the block number of destination
#End Schedule class defintion
    
    








