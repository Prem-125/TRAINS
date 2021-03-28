
import sys
import random 
import math 
import time 

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from UI import Ui_MainWindow
from Train import Train

newTrain= Train()
class MainWindow(QMainWindow):
	# newTrain= Train()
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #newTrain= Train()
        self.ui.pwrInput.textChanged.connect(self.set_power)
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
        self.ui.pushButton.clicked.connect(self.emergency_brake)
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


    def open_left_doors(self):
    	self.ui.leftDoorsOutput.setText("Open")
    	self.ui.leftDoorsOutput_4.setText("Open")
    	newTrain.lDoorsOpen = True
    def close_left_doors(self):
    	self.ui.leftDoorsOutput.setText("Closed")
    	self.ui.leftDoorsOutput_4.setText("Closed")
    	newTrain.lDoorsOpen = False
    def open_right_doors(self):
    	self.ui.rightDoorsOutput.setText("Open")
    	self.ui.rightDoorsOutput_4.setText("Open")
    	newTrain.rDoorsOpen = True
    def close_right_doors(self):
    	self.ui.rightDoorsOutput.setText("Closed")
    	self.ui.rightDoorsOutput_4.setText("Closed")
    	newTrain.rDoorsOpen = False
    def c_lights_on(self):
    	self.ui.cLightsOutput.setText("On")
    	newTrain.cLightsOn = True
    def c_lights_off(self):
    	self.ui.cLightsOutput.setText("Off")
    	newTrain.cLightsOn = False
    def t_lights_on(self):
    	self.ui.tLightsOutput.setText("On")
    	newTrain.tLightsOn = True
    def t_lights_off(self):
    	self.ui.tLightsOutput.setText("Off")
    	newTrain.tLightsOn = False
    def brake_failure_on(self):
    	newTrain.brakeFailure = True
    	self.ui.brakeFailureOutput.setText("Yes")
    	self.ui.brakeFailureOutput_4.setText("Yes")
    def brake_failure_off(self):
    	newTrain.brakeFailure = False
    	self.ui.brakeFailureOutput.setText("No")
    	self.ui.brakeFailureOutput_4.setText("No") 
    def circuit_failure_on(self):
    	newTrain.circuitFailure = True
    	self.set_command_speed(None)
    	self.set_authority(None)
    	self.ui.circuitFailureOutput.setText("Yes")
    	self.ui.circuitFailureOutput_4.setText("Yes")
    def circuit_failure_off(self):
    	newTrain.circuitFailure = False
    	self.set_command_speed(str(newTrain.cmdSpeed))
    	self.set_authority(str(newTrain.authority))
    	self.ui.circuitFailureOutput.setText("No")
    	self.ui.circuitFailureOutput_4.setText("No") 
    def set_command_speed(self,text):
    	if(newTrain.circuitFailure):
    		self.ui.cmdSpeedOutput.setText("???")
    	else:	
    		newTrain.cmdSpeed = float(text)
    		self.ui.cmdSpeedOutput.setText(text + " mph")
    def set_route(self, text):
    	self.ui.routeOutput.setText(text)
    def set_beacon(self, text):
    	self.ui.Beacon.setText(text)
    def set_announcments(self, text):
    	self.ui.announcmentOutput.setText(text)
    def emergency_brake(self):
    	if(newTrain.EmergencyBrake==False):
    		newTrain.EmergencyBrake = True
    		self.ui.emergencyBreakOuput.setText("On")
    		self.ui.pushButton.setStyleSheet("background-color : green")
    		self.ui.pushButton.setText("Turn Off Emergency Brake")
    	else:
    		newTrain.EmergencyBrake = False
    		self.ui.emergencyBreakOuput.setText("Off")
    		self.ui.pushButton.setStyleSheet("background-color : red")
    		self.ui.pushButton.setText("Emergency Brake")
    	self.set_velocity()
    def engine1_failure(self):
    	if(self.ui.engine1.isChecked()):
    		newTrain.engineFailure= newTrain.engineFailure + 1
    		self.ui.engineFailureOutput.setText("Yes")
    		self.ui.engineFailureOutput_4.setText("Yes")
    	else:
    		newTrain.engineFailure = newTrain.engineFailure - 1
    		if(newTrain.engineFailure == 0):
    			self.ui.engineFailureOutput.setText("No")
    			self.ui.engineFailureOutput_4.setText("No")
    	self.set_velocity()
    def engine2_failure(self):
    	if(self.ui.engine2.isChecked()):
    		newTrain.engineFailure= newTrain.engineFailure + 1
    		self.ui.engineFailureOutput.setText("Yes")
    		self.ui.engineFailureOutput_4.setText("Yes")
    	else:
    		newTrain.engineFailure = newTrain.engineFailure - 1
    		if(newTrain.engineFailure == 0):
    			self.ui.engineFailureOutput.setText("No")
    			self.ui.engineFailureOutput_4.setText("No")
    	self.set_velocity() 
    def engine3_failure(self):
    	if(self.ui.engine3.isChecked()):
    		newTrain.engineFailure= newTrain.engineFailure + 1
    		self.ui.engineFailureOutput.setText("Yes")
    		self.ui.engineFailureOutput_4.setText("Yes")
    	else:
    		newTrain.engineFailure = newTrain.engineFailure - 1
    		if(newTrain.engineFailure == 0):
    			self.ui.engineFailureOutput.setText("No")
    			self.ui.engineFailureOutput_4.setText("No")
    	self.set_velocity()
    def engine4_failure(self):
    	if(self.ui.engine4.isChecked()):
    		newTrain.engineFailure= newTrain.engineFailure + 1
    		self.ui.engineFailureOutput.setText("Yes")
    		self.ui.engineFailureOutput_4.setText("Yes")
    	else:
    		newTrain.engineFailure = newTrain.engineFailure - 1
    		if(newTrain.engineFailure == 0):
    			self.ui.engineFailureOutput.setText("No")
    			self.ui.engineFailureOutput_4.setText("No")
    	self.set_velocity()   		    		 
    def engine5_failure(self):
    	if(self.ui.engine5.isChecked()):
    		newTrain.engineFailure= newTrain.engineFailure + 1
    		self.ui.engineFailureOutput.setText("Yes")
    		self.ui.engineFailureOutput_4.setText("Yes")
    	else:
    		newTrain.engineFailure = newTrain.engineFailure - 1
    		if(newTrain.engineFailure == 0):
    			self.ui.engineFailureOutput.setText("No")
    			self.ui.engineFailureOutput_4.setText("No")
    	self.set_velocity()
    def set_authority(self,text):
    	if(newTrain.circuitFailure):
    		self.ui.authOutput.setText("???")
    	else:	
    		newTrain.authority = float(text)
    		self.ui.authOutput.setText(text + " meters") 
    def temp_changed(self):
   		self.ui.tempOuput.setText(str(self.ui.spinBox.value())+" °F")
    def s_brake_on(self):
   		newTrain.serviceBrake=True
   		self.ui.serviceBreakOuput.setText("On")
   		self.set_velocity()
    def s_brake_off(self):
   		newTrain.serviceBrake=False
   		self.ui.serviceBreakOuput.setText("Off")
   		self.set_velocity()


                                                  










    def set_velocity(self):
    	calcVelocity = (newTrain.power/2  * (1 - .2 * newTrain.engineFailure))
    	if((newTrain.EmergencyBrake or newTrain.serviceBrake) and not newTrain.brakeFailure):
    		newTrain.velocity = 0
    	elif(calcVelocity>newTrain.spdLimit):
    		newTrain.velocity = newTrain.spdLimit
    	else:
    		newTrain.velocity = calcVelocity
    	self.ui.veloOutput.setText(str(round(newTrain.velocity*2.23694,2))+ " mph")
    def set_power(self, text):
    	newTrain.power = float(text)
    	self.set_velocity()
    def set_speed_limit(self, text):
    	newTrain.spdLimit = float(text)
    	newTrain.spdLimit =newTrain.spdLimit * .44704
    	self.set_velocity()
    	#print(newTrain.spdLimit)
   

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

