import sys
import serial
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import QFile, QTimer
from .UI import Ui_TrainControllerHWInterface

class TrainControllerHWInterface(QMainWindow):
	def __init__(self,train_model,initalTC=25769816839, current_speed= 0, trainID=1):
		super(TrainControllerHWInterface, self).__init__()
		self.train_model = train_model
		self.ui = Ui_TrainControllerHWInterface()
		self.ui.setupUi(self)
		self.utimer = QTimer()
		self.utimer.timeout.connect(self.timerCallback)
		self.ui.setParams.clicked.connect(self.set_kp_ki)
		self.ui.IDVal.setPlainText(str(trainID))
		self.power = 0
		self.curSpeed = current_speed
		self.encodedB=0
		self.nFlag=0
		self.eol = '\n'.encode('utf-8')
		self.encodedTC=initalTC
		self.rawToggle = 0
		self.sBrakePull = False
		self.EBrakePull = False
		self.LDoorOpen = False
		self.RDoorOpen = False
		self.IntLightsOn = False
		self.ExtLightsOn = False
		self.temperature = 0
		self.announcement = ''
		self.connectArduino()
		self.run=False



	def connectArduino(self):
		try:
			self.arduino = serial.Serial(port='COM3', baudrate=115200,timeout=1)
			self.run=True
			self.utimer.start(500)
			self.show()

		except:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)

			msg.setText("The Arduino does not appear to be connected, please ensure it is connected and powered on. Also please make sure it is associated to COM3 in device manager. Then press Ok to retry.")
			msg.setWindowTitle("Connection Error")
			msg.setStandardButtons(QMessageBox.Ok)
			msg.buttonClicked.connect(self.connectArduino)
			retval = msg.exec_()

		
	def timerCallback(self):
		#self.serialWrite()
		self.serialRead()
		...
		
		
	def serialRead(self):
		while(self.arduino.in_waiting > 0):
			raw = self.arduino.readline()
			status = raw.decode('ascii').strip('\r\n')
			#print("Status Val is: ")
			#print(status)
			status = int(status)
			if (status == 1):
				raw = self.arduino.readline()
				status = raw.decode('ascii').strip('\r\n')
				#print(status)
				self.rawToggle = int(status)
				self.decodeToggleStates()
				self.updateToggleDisp()
			elif (status == 2):
				raw = self.arduino.readline()
				status = raw.decode('ascii').strip('\r\n')
				#print(status)
				self.power = float(status)
				self.ui.PowerVal.setPlainText(str(round(self.power/1000.0 , 2))+ " kW")
			elif(status ==3):
				raw = self.arduino.readline()
				status = raw.decode('ascii').strip('\r\n')
				#print(status)
				self.announcement = status
				self.ui.AnnounceVal.setPlainText(status)
			elif(status ==4):
				raw = self.arduino.readline()
				status = raw.decode('ascii').strip('\r\n')
				#print(status)
				self.temperature = int(status)
				self.ui.TemperatureVal.setPlainText(status + "°F")


	def serialWrite(self):
		self.arduino.reset_output_buffer()
		self.arduino.write(str(self.nFlag).encode('utf-8')+ self.eol)
		self.arduino.write(str(self.encodedTC).encode('utf-8')+ self.eol)
		self.arduino.write(self.curSpeed.encode('utf-8')+ self.eol)
		self.arduino.write(str(self.encodedB).encode('utf-8')+ self.eol)
		self.nFlag=0

		
		
	def set_track_circuit(self,TC):				
		print("SETTING TC")
		self.arduino.write(str(2).encode('utf-8')+ self.eol)
		self.arduino.write(str(TC).encode('utf-8')+ self.eol)

	def set_beacon(self,Beacon):
		print("SETTING Beacon")

		self.arduino.write(str(3).encode('utf-8')+ self.eol)
		self.arduino.write(str(Beacon).encode('utf-8')+ self.eol)

	
	def set_current_speed(self,speed):
		print("SETTING Current Speed" + str(speed))

		self.curSpeed= speed
		self.ui.CurSpeedVal.setPlainText(str(round(self.curSpeed,2)))
		self.arduino.write(str(1).encode('utf-8')+ self.eol)
		self.arduino.write(str(self.curSpeed).encode('utf-8')+ self.eol)

	def set_kp_ki(self):
		kp = float(self.ui.KpVal.toPlainText())
		ki = float(self.ui.KiVal.toPlainText())
		kpInt = int(kp)
		kpFloat = int((kp - float(kpInt))*1000.0)
		kiInt = int(ki)
		kiFloat = int((ki - float(kiInt))*1000.0)
		transmit = kpInt + (kpFloat << 16) + (kiInt << 32) + (kiFloat << 48)
		self.arduino.write(str(4).encode('utf-8')+ self.eol)
		self.arduino.write(str(transmit).encode('utf-8')+ self.eol)



	def get_power(self):
		return self.power

	def decodeToggleStates(self):
		self.ExtLightsOn = self.rawToggle & 1
		self.IntLightsOn = (self.rawToggle >> 1) & 1
		self.sBrakePull = (self.rawToggle >> 2) & 1
		self.RDoorOpen = (self.rawToggle >> 3) & 1
		self.LDoorOpen = (self.rawToggle >> 4) & 1
		self.EBrakePull = ((self.rawToggle >> 6) & 1) | ((self.rawToggle >> 7) & 1)

	def updateToggleDisp(self):
		if(self.ExtLightsOn):
			self.ui.ELightVal.setPlainText("ON")
			self.train_model.t_lights_on()
		else:
			self.ui.ELightVal.setPlainText("OFF")
			self.train_model.t_lights_off()

		if(self.IntLightsOn):
			self.ui.ILightVal.setPlainText("ON")
			self.train_model.c_lights_on()
		else:
			self.ui.ILightVal.setPlainText("OFF")
			self.train_model.c_lights_off()

		if(self.sBrakePull):
			self.ui.SBrakeVal.setPlainText("ACTIVE")
			self.train_model.s_brake_on()
		else:
			self.ui.SBrakeVal.setPlainText("INACTIVE")
			self.train_model.s_brake_off()

		if(self.RDoorOpen):
			self.ui.RDoorVal.setPlainText("OPEN")
			self.train_model.open_right_doors()
		else:
			self.ui.RDoorVal.setPlainText("CLOSE")
			self.train_model.close_right_doors()
		if(self.LDoorOpen):
			self.ui.LDoorVal.setPlainText("OPEN")
			self.train_model.open_left_doors()
		else:
			self.ui.LDoorVal.setPlainText("CLOSE")
			self.train_model.close_left_doors()

		if(self.EBrakePull):
			self.ui.EBrakeVal.setPlainText("ACTIVE")
			self.train_model.emergency_brake_on()
		else:
			self.ui.EBrakeVal.setPlainText("INACTIVE")
			self.train_model.emergency_brake_off()



if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = TrainControllerHWInterface()
	sys.exit(app.exec_())
