import sys
import serial
import time
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, QTimer
from UI import Ui_TrainModelInterface

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.ui = Ui_TrainModelInterface()
		self.ui.setupUi(self)
		self.utimer = QTimer()
		self.utimer.timeout.connect(self.timerCallback)
		self.utimer.start(1000)
		self.testval = 0
		self.arduino = serial.Serial(port='COM3', baudrate=115200,timeout=1)
		self.ui.tcButton.clicked.connect(self.getTCInfo)
		self.ui.beaconButton.clicked.connect(self.getBeaconInfo)
		self.ui.speedButton.clicked.connect(self.getCurSpeed)

		self.cmdSpeed = ''
		self.curSpeed = ''
		self.authority = ''
		self.encodedB=0
		self.nFlag=0
		self.eol = '\n'.encode('utf-8')
		self.encodedTC=0
		
		
	def timerCallback(self):
		#self.arduino.write(str(self.testval).encode('utf-8')+ self.eol)
		#self.serialWrite()
		#self.serialRead()
		...
		
		
	def serialRead(self):
		print(self.arduino.in_waiting)
		raw = self.arduino.readline()
		#print(raw)
		status = raw.decode('ascii')#.strip('\r\n')
		print(status)
		self.ui.AnnounceVal.setPlainText(status)
		self.arduino.reset_input_buffer()
		
	def serialWrite(self):
		self.arduino.reset_output_buffer()
		self.arduino.write(str(self.nFlag).encode('utf-8')+ self.eol)
		self.arduino.write(str(self.encodedTC).encode('utf-8')+ self.eol)
		self.arduino.write(self.curSpeed.encode('utf-8')+ self.eol)
		self.arduino.write(str(self.encodedB).encode('utf-8')+ self.eol)
		self.nFlag=0

		
		
	def getTCInfo(self):
		self.cmdSpeed= self.ui.CommSpeedVal.toPlainText()
		self.curSpeed= self.ui.CurSpeedVal.toPlainText()
		self.authority= self.ui.AuthVal.toPlainText()
		cmdInt= int(float(self.cmdSpeed))
		cmdFloat= int(((float(self.cmdSpeed)-cmdInt)*10))
		authInt= int(float(self.authority))
		authFloat= int(((float(self.authority)-authInt)*10))
		if(self.ui.sigFail.checkState()):
			self.encodedTC = (cmdInt-6 & 255)
		else:
			self.encodedTC = (cmdInt & 255)
		self.encodedTC += (cmdFloat & 15) << 8
		self.encodedTC += (authInt & 255) << 12
		self.encodedTC += (authFloat & 15)<< 20
		self.encodedTC += ((cmdInt + cmdFloat + authFloat + authInt) & 1023) << 24
		
		#print(bin(cmdInt))
		#print(self.encodedTC)
		print(bin(self.encodedTC))
		self.nFlag|=2
		#print(self.cmdSpeed)
		self.arduino.write(str(2).encode('utf-8')+ self.eol)
		self.arduino.write(str(self.encodedTC).encode('utf-8')+ self.eol)

	def getBeaconInfo(self):
		beaconNum= self.ui.stationSel.currentIndex()
		print(int(self.ui.stationComing.checkState()))
		self.encodedB = int(self.ui.stationComing.checkState()  )>> 1
		print(bin(self.encodedB))
		self.encodedB += (int(self.ui.BLDoor.checkState()) >> 1) << 1
		self.encodedB += (int(self.ui.BRDoor.checkState()) >> 1) << 2
		self.encodedB += (int(self.ui.BExtLight.checkState()) >> 1) << 3
		self.encodedB += (beaconNum & 31) << 4
		print(bin(self.encodedB))		
		self.nFlag|=1
		self.arduino.write(str(3).encode('utf-8')+ self.eol)
		self.arduino.write(str(self.encodedB).encode('utf-8')+ self.eol)

	
	def getCurSpeed(self):
		self.curSpeed= self.ui.CurSpeedVal.toPlainText()
		self.arduino.write(str(1).encode('utf-8')+ self.eol)
		self.arduino.write(self.curSpeed.encode('utf-8')+ self.eol)


if __name__ == "__main__":
	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()
	sys.exit(app.exec_())
