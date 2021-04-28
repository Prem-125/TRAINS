
"""Module defining signals for communications"""

from PySide6.QtCore import QObject, Signal
import xlrd

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
        signals.backend_occupancy.connect(self.UpdateOccupancy)

        #Obtain switch position from wayside controller
        signals.CTC_switch_position.connect(self.UpdateSwitchPos)

        #Initialize block composition of TrackLine
        self.TrackSetup(filepath, sheet_index)

        #Initialize instance variable to hold the total number of tickets sold on track line
        self.ticket_sales = 0

        #Declare a list of closed blocks
        self.closed_blocks = []

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
            block_speed_limit = int(exl_sheet.cell_value(i, 5)) #Kilometers/Hour

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
        #Search switch list
        for SwitchObj in self.switch_list:
            if(SwitchObj.root == root_block_num):
                SwitchObj.curr_position = branch_block_num
            #End if
        #End for loop
    #End method

#End TrackLine class definition

#from src.common_def import *

# pylint: disable=too-few-public-methods
class SignalsClass(QObject):
    """Class to hold all the signals"""
    test = Signal(int) # Current day, hours, minutes, seconds

    TC_signal = Signal(int,int)
    Beacon_signal = Signal(int,int)
    time_signal = Signal(int,int)

    #Signal to exchange ticket sales information per track line
    station_ticket_sales = Signal(str, int) #Parameters are track line name and new ticket sales

    #Signal to inform train controller of new train instance
    train_creation = Signal(str, int) #Parameter is train number 


    #Signals exchanged between CTC and wayside
    backend_occupancy = Signal(TrackLine, int, bool)
    CTC_occupancy = Signal(str, int, bool) #Paramter is block number
    CTC_authority = Signal(str, int) #Paramter is block number
    CTC_failure = Signal(str, int, int) #Paramters are track line, track block, and failure mode
    CTC_suggested_speed = Signal(str, int, int)  #Parameters are track line, track block, and suggested speed
    wayside_block_status = Signal(str, int, bool) #Parameters are track line, block number, block status
    CTC_switch_position = Signal(str, int, int) #Parameters are track line, switch stem, current branch
    CTC_toggle_switch = Signal(str, int) #Parameters are track line, switch stem


    #Signals exchanged between wayside and track model
    track_model_occupancy = Signal(int, bool)
    wayside_to_track = Signal(int, int, float) # Block Num, Auth, Cmd Speed
    #functions to send to wayside telling the line, block number, and failure type 
    #0=rail failure, 1=circuit failure, 2=power_failure
    track_break = Signal(str, int, int)
    wayside_block_open = Signal(str, int)
    track_switch_position = Signal(str, int, int) # Parameters are Line Name, switch stem, current branch


    need_new_block = Signal(int,int) #block num and trainID train model sends to track model
    new_block = Signal(int, int, float, int) #block number, block length, block slope and trainID ---Track model sends to train model

    num_passengers_changed = Signal(int, int) #when at station and number of passengers change this is the result 
    #first int is delta passengers (can be pos or neg), second int is train id
    
    #need signal for beacon




#trackSelector <- linebox for track model QLineEdit


# Single instance to be used by other modules
signals = SignalsClass()
