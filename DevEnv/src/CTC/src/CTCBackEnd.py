import xlrd

#Global variable to serve as system-wide clock
gbl_seconds = 0
gbl_centiseconds = 0

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
        self.status = 1

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
        if self.curr_position == self.branch_1_num:
            self.curr_position = self.branch_2_num
        else:
            self.curr_position = self.branch_1_num
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

        #Initialize instance varialbe to hold the total number of tickets sold at the station
        self.ticket_sales = 0
    #End constructor

#End Station class definition


#Define Train class
class Train:

    #Constructor
    def __init__(self, train_number, block_destination, TrackLineObj, train_arrival_time, train_departure_time):
        #Initialize Block instance variables
        self.number = train_number
        self.destination = block_destination #Block Number
        self.track_line = TrackLineObj.color  #String
        self.arrival_time = train_arrival_time     #Seconds
        self.departure_time = train_departure_time #Seconds
    #End contructor

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

        #Initialize block composition of TrackLine
        self.TrackSetup(filepath, sheet_index)
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
            block_length = int(exl_sheet.cell_value(i, 3))               #Meters
            block_speed_limit = int(exl_sheet.cell_value(i, 5)) * .27778 #Converted to Meters/Second

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
                            root_block_num = temp_str
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
    def ManualSchedule(self, block_destination, train_arrival_time, TrackLineObj):
        global gbl_seconds
        
        #Assign train number
        train_number = len(self.train_list) + 1

        #Compute train travel time
        travel_time = self.ComputeTravelTime(block_destination, train_arrival_time, TrackLineObj)

        #Compute train departure time
        train_departure_time = train_arrival_time - travel_time

        #Determine if specified arrival time is valid
        if(train_departure_time < 0):
            return False

        #Determine if specified destination is valid
        if(TrackLineObj.color == "Green"):
            if(block_destination < 1 or block_destination > 150):
                print("HIT2")
                return False
        elif(TrackLineObj.color == "Red"):
            if(block_destination < 1 or block_destination > 76):
                print("HIT3")
                return False
        
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

                for i in range(1, block_destination):
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

#End Schedule class defintion
    
    








