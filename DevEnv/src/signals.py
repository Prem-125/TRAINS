
"""Module defining signals for communications"""

from PySide6.QtCore import QObject, Signal


#from src.common_def import *

# pylint: disable=too-few-public-methods
class SignalsClass(QObject):
    """Class to hold all the signals"""
    test = Signal(int) # Current day, hours, minutes, seconds

    TC_signal = Signal(int,int)
    Beacon_signal = Signal(int,int)
    time_signal = Signal(int)

    #Signal to exchange ticket sales information per track line
    station_ticket_sales = Signal(str, int) #Parameters are track line name and new ticket sales

    #Signal to inform train controller of new train instance
    train_creation = Signal(str, int) #Parameter is train number 


    #Signals exchanged between CTC and wayside
    CTC_occupancy = Signal(int) #Paramter is block number
    CTC_authority = Signal(int) #Paramter is block number

    track_model_occupancy = Signal(int, bool)
    wayside_to_track = Signal(int, int, float)
    
    #track_rail_condition = Signal(bool)
    #track_circuiit_condition = Signal(bool)

    need_new_block = Signal(int) #trainID train model sends to track model
    new_block = Signal(int, int, float, int) #block number, block length, block slope and trainID ---Track model sends to train model

    num_passengers_changed = Signal(int, int) #when at station and number of passengers change this is the result 
    #first int is delta passengers (can be pos or neg), second int is train id
    



#trackSelector <- linebox for track model QLineEdit


# Single instance to be used by other modules
signals = SignalsClass()
