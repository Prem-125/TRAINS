
"""Module defining signals for communications"""

from PySide6.QtCore import QObject, Signal

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
    CTC_occupancy = Signal(str, int, bool) #Paramter is block number
    CTC_authority = Signal(str, int) #Paramter is block number
    CTC_reset_train = Signal(str, int, bool) #Parameters are
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
