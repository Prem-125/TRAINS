
"""Module defining signals for communications"""

from PySide6.QtCore import QObject, Signal


#from src.common_def import *

# pylint: disable=too-few-public-methods
class SignalsClass(QObject):
    """Class to hold all the signals"""
    station_ticket_sales = Signal(str, int) # Current day, hours, minutes, seconds

#trackSelector <- linebox for track model QLineEdit


# Single instance to be used by other modules
signals = SignalsClass()
