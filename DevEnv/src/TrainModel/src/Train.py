import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from UI import Ui_MainWindow

class Train:

	def __init__(self):

		#basic train information
		self.length = 32.2 #meters
		self.width = 2.65
		self.height = 3.42
		self.weight = 40.9 #tons

		self.power = 0.0
		self.velocity = 0.0
		self.authority = 0
		self.cmdSpeed = 0.0
		self.spdLimit= 19.44 #70km/h to m/s
		self.accLimit = 0.5 #m/s
		self.decLimit = -2.73
		self.temperature = 70 # farenheit 

		self.lDoorsOpen = False
		self.rDoorsOpen = False
		self.tLightsOn = False
		self.cLightsOn = True 
		self.serviceBrake = False
		self.EmergencyBrake = False


		#Failures
		self.brakeFailure = False
		self.engineFailure = 0
		self.circuitFailure = False


