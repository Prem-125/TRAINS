
"""Module defining signals for communications"""

from PySide6.QtCore import QObject, Signal


#from src.common_def import *

# pylint: disable=too-few-public-methods
class SignalsClass(QObject):
    """Class to hold all the signals"""

    #Signal to exchange ticket sales information per track line
    station_ticket_sales = Signal(str, int) #Parameters are track line name and new ticket sales

    #Signal to inform train controller of new train instance
    train_creation = Signal(int) #Parameter is train number

    

#trackSelector <- linebox for track model QLineEdit


# Single instance to be used by other modules
signals = SignalsClass()
