import sys
import random 
import math 
import time 

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, QTimer
from TrainModel.src.UI import Ui_MainWindow
from TrainModel.src.Train import Train as TrainModel
from TrainControllerSW.src.TrainControllerSW import TrainController as TrainControllerSW
from TrainControllerHW.src.TrainControllerHWInterface import TrainControllerHWInterface as TrainControllerHW
from signals import signals


class MainWindow(QMainWindow):
	
	def __init__(self, commanded_speed, current_speed, authority, soft_or_hard, line, trainID):
		super(MainWindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.train= TrainModel()
		#if soft_or_hard is true, it is software, if false, it is hard
		#self.train.cmdSpeed = commanded_speed
		self.train.velocity = float(current_speed)
		self.train.trainID = trainID

		if(soft_or_hard):
			self.train_controller = TrainControllerSW(self, commanded_speed, current_speed, 1, trainID)
		else:
			self.train_controller = TrainControllerHW(self,trainID = trainID)


		self.ui.pwrInput.textChanged.connect(self.get_power)
		self.ui.speedLimit.textChanged.connect(self.set_speed_limit)
		#self.ui.speedLimit.textChanged.connect(self.set_velocity)
		self.ui.leftDoorOpen.clicked.connect(self.open_left_doors)
		self.ui.leftDoorsClose.clicked.connect(self.close_left_doors)
		self.ui.rightDoorsOpen.clicked.connect(self.open_right_doors)
		self.ui.rightDoorClose.clicked.connect(self.close_right_doors)
		self.ui.cLightsOn.clicked.connect(self.c_lights_on)
		self.ui.cLightsOff.clicked.connect(self.c_lights_off)
		self.ui.tLightsOn.clicked.connect(self.t_lights_on)
		self.ui.tLightsOff.clicked.connect(self.t_lights_off)
		self.ui.brakeFailureOn.clicked.connect(self.brake_failure_on)
		self.ui.brakeFailureOff.clicked.connect(self.brake_failure_off)
		self.ui.cmdSpeed.textChanged.connect(self.set_command_speed)
		self.ui.announcmentsInput.textChanged.connect(self.set_announcments)
		self.ui.beacInput.textChanged.connect(self.set_beacon)
		self.ui.routeInput.textChanged.connect(self.set_route)
		#self.ui.pushButton.clicked.connect(self.emergency_brake)
		self.ui.circuitFailureOn.clicked.connect(self.circuit_failure_on)
		self.ui.circuitFailureOff.clicked.connect(self.circuit_failure_off)
		self.ui.engine1.clicked.connect(self.engine1_failure)
		self.ui.engine2.clicked.connect(self.engine2_failure)
		self.ui.engine3.clicked.connect(self.engine3_failure)
		self.ui.engine4.clicked.connect(self.engine4_failure)
		self.ui.engine5.clicked.connect(self.engine5_failure)
		self.ui.authInput.textChanged.connect(self.set_authority)
		self.ui.spinBox.valueChanged.connect(self.temp_changed)
		self.ui.serviceBreakOn.clicked.connect(self.s_brake_on)
		self.ui.serviceBreakOff.clicked.connect(self.s_brake_off)

		self.powerTimer = QTimer()
		self.powerTimer.timeout.connect(self.get_power)
		self.powerTimer.start(500) 
		self.currPosition = 0.0

		if(line == 'Green'):
			self.blockLen = 50
			self.blockNum = 58
			self.blockSlope = 0.0
		else:
			self.blockLen = 75
			self.blockNum = 9
			self.blockSlope = 0.0



	def set_time(self, time):
		timer = time
		

	def open_left_doors(self):
		self.ui.leftDoorsOutput.setText("Open")
		self.ui.leftDoorsOutput_4.setText("Open")
		self.train.lDoorsOpen = True
	def close_left_doors(self):
		self.ui.leftDoorsOutput.setText("Closed")
		self.ui.leftDoorsOutput_4.setText("Closed")
		self.train.lDoorsOpen = False
	def open_right_doors(self):
		self.ui.rightDoorsOutput.setText("Open")
		self.ui.rightDoorsOutput_4.setText("Open")
		self.train.rDoorsOpen = True
	def close_right_doors(self):
		self.ui.rightDoorsOutput.setText("Closed")
		self.ui.rightDoorsOutput_4.setText("Closed")
		self.train.rDoorsOpen = False
	def c_lights_on(self):
		self.ui.cLightsOutput.setText("On")
		self.train.cLightsOn = True
	def c_lights_off(self):
		self.ui.cLightsOutput.setText("Off")
		self.train.cLightsOn = False
	def t_lights_on(self):
		self.ui.tLightsOutput.setText("On")
		self.train.tLightsOn = True
	def t_lights_off(self):
		self.ui.tLightsOutput.setText("Off")
		self.train.tLightsOn = False
	def brake_failure_on(self):
		self.train.brakeFailure = True
		self.ui.brakeFailureOutput.setText("Yes")
		self.ui.brakeFailureOutput_4.setText("Yes")
	def brake_failure_off(self):
		self.train.brakeFailure = False
		self.ui.brakeFailureOutput.setText("No")
		self.ui.brakeFailureOutput_4.setText("No") 
	def circuit_failure_on(self):
		self.train.circuitFailure = True
		self.set_command_speed(None)
		self.set_authority(None)
		self.ui.circuitFailureOutput.setText("Yes")
		self.ui.circuitFailureOutput_4.setText("Yes")
	def circuit_failure_off(self):
		self.train.circuitFailure = False
		self.set_command_speed(str(self.train.cmdSpeed))
		self.set_authority(str(self.train.authority))
		self.ui.circuitFailureOutput.setText("No")
		self.ui.circuitFailureOutput_4.setText("No") 
	def set_command_speed(self,text):
		if(self.train.circuitFailure):
			self.ui.cmdSpeedOutput.setText("???")
		else:	
			self.train.cmdSpeed = float(text)
			self.ui.cmdSpeedOutput.setText(text + " mph")
	def set_route(self, text):
		self.ui.routeOutput.setText(text)
	def set_beacon(self, text):
		self.ui.Beacon.setText(text)
	def set_announcments(self, text):
		self.ui.announcmentOutput.setText(text)
	# def emergency_brake(self):
	# 	if(self.train.EmergencyBrake==False):
	# 		self.train.EmergencyBrake = True
	# 		self.ui.emergencyBreakOuput.setText("On")
	# 		self.ui.pushButton.setStyleSheet("background-color : green")
	# 		self.ui.pushButton.setText("Turn Off Emergency Brake")
	# 	else:
	# 		self.train.EmergencyBrake = False
	# 		self.ui.emergencyBreakOuput.setText("Off")
	# 		self.ui.pushButton.setStyleSheet("background-color : red")
	# 		self.ui.pushButton.setText("Emergency Brake")
	# 	self.set_velocity()


	def emergency_brake_on(self):
		self.train.EmergencyBrake = True
		self.ui.emergencyBreakOuput.setText("On")
		#self.ui.pushButton.setText("Turn Off Emergency Brake")
		
		#self.set_velocity()

	def emergency_brake_off(self):
		
		self.train.EmergencyBrake = False
		self.ui.emergencyBreakOuput.setText("Off")
		#self.ui.pushButton.setText("Emergency Brake")
		#self.set_velocity()

	def engine1_failure(self):
		if(self.ui.engine1.isChecked()):
			self.train.engineFailure= self.train.engineFailure + 1
			self.ui.engineFailureOutput.setText("Yes")
			self.ui.engineFailureOutput_4.setText("Yes")
		else:
			self.train.engineFailure = self.train.engineFailure - 1
			if(self.train.engineFailure == 0):
				self.ui.engineFailureOutput.setText("No")
				self.ui.engineFailureOutput_4.setText("No")
		self.set_velocity()
	def engine2_failure(self):
		if(self.ui.engine2.isChecked()):
			self.train.engineFailure= self.train.engineFailure + 1
			self.ui.engineFailureOutput.setText("Yes")
			self.ui.engineFailureOutput_4.setText("Yes")
		else:
			self.train.engineFailure = self.train.engineFailure - 1
			if(self.train.engineFailure == 0):
				self.ui.engineFailureOutput.setText("No")
				self.ui.engineFailureOutput_4.setText("No")
		self.set_velocity() 
	def engine3_failure(self):
		if(self.ui.engine3.isChecked()):
			self.train.engineFailure= self.train.engineFailure + 1
			self.ui.engineFailureOutput.setText("Yes")
			self.ui.engineFailureOutput_4.setText("Yes")
		else:
			self.train.engineFailure = self.train.engineFailure - 1
			if(self.train.engineFailure == 0):
				self.ui.engineFailureOutput.setText("No")
				self.ui.engineFailureOutput_4.setText("No")
		self.set_velocity()
	def engine4_failure(self):
		if(self.ui.engine4.isChecked()):
			self.train.engineFailure= self.train.engineFailure + 1
			self.ui.engineFailureOutput.setText("Yes")
			self.ui.engineFailureOutput_4.setText("Yes")
		else:
			self.train.engineFailure = self.train.engineFailure - 1
			if(self.train.engineFailure == 0):
				self.ui.engineFailureOutput.setText("No")
				self.ui.engineFailureOutput_4.setText("No")
		self.set_velocity()   					 
	def engine5_failure(self):
		if(self.ui.engine5.isChecked()):
			self.train.engineFailure= self.train.engineFailure + 1
			self.ui.engineFailureOutput.setText("Yes")
			self.ui.engineFailureOutput_4.setText("Yes")
		else:
			self.train.engineFailure = self.train.engineFailure - 1
			if(self.train.engineFailure == 0):
				self.ui.engineFailureOutput.setText("No")
				self.ui.engineFailureOutput_4.setText("No")
		self.set_velocity()
	
	def set_authority(self,text):
		if(self.train.circuitFailure):
			self.ui.authOutput.setText("???")
		else:	
			self.train.authority = float(text)
			self.ui.authOutput.setText(text + " meters") 
	def temp_changed(self):
   		self.ui.tempOuput.setText(str(self.ui.spinBox.value())+" °F")
		   
	def s_brake_on(self):
   		self.train.serviceBrake=True
   		self.ui.serviceBreakOuput.setText("On")
   		self.set_velocity()
	def s_brake_off(self):
   		self.train.serviceBrake=False
   		self.ui.serviceBreakOuput.setText("Off")
   		self.set_velocity()



	def	set_track_circuit(self,TrackInt):
	    self.train_controller.set_track_circuit(TrackInt)

	def	set_beacon(self,BeaconInt):
		self.train_controller.set_beacon(BeaconInt)	

	def set_acceleration_limit(self, accLimit):
		self.train.accLimit = accLimit












	def set_velocity(self):
		# find force on train
		try:
			force = (self.train.power/self.train.velocity)
			#calculate the force in the opposite direction based on slope of track
			force -= self.train.fricCoef * self.train.mass * self.train.gravity * math.sin(self.blockSlope)
			force -= .01 * self.train.mass * self.train.gravity
		except ZeroDivisionError: #catches if train is stationary 
			if(not self.train.serviceBrake and not self.train.EmergencyBrake and (self.train.power != 0.0)):
				force = 1000000 #chose arbitrary amount to get train moving
				#calculate the force in the opposite direction based on slope of track
				force -= self.train.fricCoef * self.train.mass * self.train.gravity * math.sin(self.blockSlope)
			else:
				force = 0.0
		
		#find acceleration of the train
		previousAcc = self.train.acceleration
		self.train.acceleration = force/self.train.mass
		if(self.train.acceleration > self.train.accLimit):
			self.train.acceleration = self.train.accLimit
		elif(self.train.EmergencyBrake):
			self.train.acceleration = self.train.decLimitE
		elif(self.train.serviceBrake):
			self.train.acceleration = self.train.decLimitS


		#calculate teh velocity (in meters per sec)
		calcVelocity = (self.train.velocity + ( (self.train.samplePeriod /2) * (self.train.acceleration + previousAcc)  * (1 - .2 * self.train.engineFailure)))

		if(calcVelocity>self.train.spdLimit):
			self.train.velocity = self.train.spdLimit
		else:
			self.train.velocity = calcVelocity

		if(self.train.velocity<0.0):
			self.train.velocity = 0.0

		self.ui.veloOutput.setText(str(round(self.train.velocity*2.23694,2))+ " mph")
		print("the speedbeing sent to train controler " + str(self.train.velocity))
		self.train_controller.set_current_speed(self.train.velocity)

		disCovered = (self.train.velocity * self.train.samplePeriod)

		self.currPosition += disCovered

		if(self.currPosition > self.blockLen):
			self.currPosition -= self.blockLen
			signals.need_new_block.emit(self.blockNum,self.train.trainID)

	

    
	def get_power(self):
		self.train.power = self.train_controller.get_power()
		self.set_velocity()
    

	def set_speed_limit(self, text):
		self.train.spdLimit = float(text)
		self.train.spdLimit =self.train.spdLimit * .44704
		#self.set_velocity()
		#print(self.train.spdLimit)

	def set_block_info(self, blockNum, blockLen, blockSlope):
		self.blockLen = blockLen
		self.blockNum = blockNum
		self.blockSlope = blockSlope
		self.currPosition = 0.0

	def change_passengers(self, delta):
		self.train.passengers += delta
		self.change_mass()

	def change_mass(self):
		self.train.mass = 37103.86 + (70*self.train.passengers) # average mass of a human = 70 kg

   

if __name__ == "__main__":
	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()

	sys.exit(app.exec_())