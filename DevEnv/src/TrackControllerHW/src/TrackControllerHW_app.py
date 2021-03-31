import sys
import serial
import time
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, QTimer
from UI import Ui_MainWindow
from array import *



#global variable arrays
train_data_arr = []
block_data_arr = [
[1,50, 50, False],
[2,50, 50, False],
[3,50, 50, False],
[4,50, 50, False],
[5,50, 50, False],
[6,50, 50, False],
[7,50, 50, False],
[8,50, 50, False],
[9,50, 50, False],
[10,50, 50, False],
[11,50, 50, False],
[12,50, 50, False],
[13,50, 50, False],
[14,50, 50, False],
[15,50, 50, False],
]
junction_position = '' #can be either 5-6 or 5-11






class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		#input test data
		self.ui.trainInputButton.clicked.connect(self.train_data_input_clicked)
		self.ui.blockInputButton.clicked.connect(self.block_data_input_clicked)

		#output sample
		self.ui.trainSelectButton.clicked.connect(self.train_select_clicked)
		self.ui.blockSelectButton.clicked.connect(self.block_select_clicked)

		#define junction pos
		self.ui.junctionPositionDisplay.setText('5-11')
		#junction buttons
		self.ui.button56.clicked.connect(self.button56_clicked)
		self.ui.button511.clicked.connect(self.button511_clicked)

		self.update_controller_info()

		#setup arduino
		self.utimer = QTimer()
		self.utimer.timeout.connect(self.timerCallback)
		self.utimer.start(500)
		self.testval = 0
		#self.arduino = serial.Serial(port='COM3', baudrate=115200,timeout=.5)
		self.eol = '\n'.encode('utf-8')
		self.nFlag=0
		self.encodedTC=0
		self.rawToggle = 0
		self.encodedB=0
		self.switch_state1 = None
		self.switch_state2 = None
		self.switch_state3 = None
		self.switch_state4 = None
		self.switch_state5 = None

	def timerCallback(self):
		#self.arduino.write(str(self.testval).encode('utf-8')+ self.eol)
		#self.serialWrite()
		self.serialRead()
		
		
		
	def serialRead(self):
		
		#print("test")
		#print(self.arduino.in_waiting)
		while(self.arduino.in_waiting > 0):

			raw = self.arduino.readline()
			raw2 = self.arduino.readline()
			raw3 = self.arduino.readline()
			raw4 = self.arduino.readline()
			raw5 = self.arduino.readline()


			status1 = raw.decode('ascii').strip('\r\n')
			status2 = raw2.decode('ascii').strip('\r\n')
			status3 = raw3.decode('ascii').strip('\r\n')
			status4 = raw4.decode('ascii').strip('\r\n')
			status5 = raw5.decode('ascii').strip('\r\n')

			#if(int(status1) == 0):

			if int(status1)== 1 and self.switch_state1 !=1:
				self.switch_state1 = 1
				#print(type(self.ui.junctionPositionDisplay.text()))

				if (self.ui.junctionPositionDisplay.text() == "5-11"):
					self.button56_clicked()
				elif (self.ui.junctionPositionDisplay.text() == "5-6"):
					self.button511_clicked()

			if int(status1)==0 and self.switch_state1 !=0:
				self.switch_state1 = 0

			

			

	def serialWrite(self):
		self.arduino.reset_output_buffer()
		self.arduino.write(str(self.nFlag).encode('utf-8')+ self.eol)
		self.arduino.write(str(self.encodedTC).encode('utf-8')+ self.eol)
		self.arduino.write(self.curSpeed.encode('utf-8')+ self.eol)
		self.arduino.write(str(self.encodedB).encode('utf-8')+ self.eol)
		self.nFlag=0





		

	def train_data_input_clicked(self):
		inp1 = self.ui.trainNumberInput.text()
		inp2 = self.ui.suggestedSpeedInput.text()
		inp3 = self.ui.authorityInput.text()
		
		train_data_arr.append([int(inp1), int(inp2), int(inp3)])

		#update tab widget
		if(len(train_data_arr) >= 1):
			self.ui.indTrainSuggestedSpeedDisplay.setText(str(train_data_arr[0][1] * .62)) #convert kph to mph
			self.ui.indTrainAuthorityDisplay.setText(str(train_data_arr[0][2] * 50 * 3.28)) #num of blocks * 50 *

		if(len(train_data_arr) >= 2):
			self.ui.indTrainSuggestedSpeedDisplay_2.setText(str(train_data_arr[1][1] * .62))
			self.ui.indTrainAuthorityDisplay_2.setText(str(train_data_arr[1][2] * 50 * 3.28))

		if(len(train_data_arr) >= 2):
			self.ui.indTrainSuggestedSpeedDisplay_3.setText(str(train_data_arr[2][1] * .62))
			self.ui.indTrainAuthorityDisplay_3.setText(str(train_data_arr[2][2] * 50 * 3.28))

	def block_data_input_clicked(self):
		inp1 = self.ui.blockNumberInput.text()
		inp2 = self.ui.blockLengthInput.text()
		inp3 = self.ui.speedLimitInput.text()
		inp4 = self.ui.occupancyInput.text()

		if(inp4 == 'Y'):
			inp4 = True
		else:
			inp4 = False

		block_data_arr[int(inp1) - 1] = [int(inp1), int(inp2), int(inp3), bool(inp4)]

		self.update_track_colors()
		self.update_controller_info()

	def train_select_clicked(self):
		inp1 = self.ui.trainNumberSelectInput.text()
		self.ui.commandedSpeedDisplay.setText(str(train_data_arr[int(inp1) - 1][1]))

	def block_select_clicked(self):
		inp1 = self.ui.blockNumberSelectInput.text()

		self.ui.occupancyDisplay.setText(str(block_data_arr[int(inp1)-1][3]))

	def button56_clicked(self):
		self.ui.junctionPositionDisplay.setText('5-6')
		#change colors
		self.ui.junction511.setStyleSheet("""background-color: rgb(255,0, 0)""")
		self.ui.junction56.setStyleSheet("""background-color: rgb(0, 170, 0)""")

	def button511_clicked(self):
		self.ui.junctionPositionDisplay.setText('5-11')

		self.ui.junction56.setStyleSheet("""background-color: rgb(255,0, 0)""")
		self.ui.junction511.setStyleSheet("""background-color: rgb(0, 170, 0)""")


	def update_controller_info(self):
		#block 1
		self.ui.block1controllerSpeedLimitDisplay.setText(str(block_data_arr[0][2] * .62))
		self.ui.block1controllerBlockLengthDisplay.setText(str("{:.2f}".format(block_data_arr[0][1] * 3.28)))
		#block 2
		self.ui.block2controllerSpeedLimitDisplay.setText(str(block_data_arr[1][2] * .62))
		self.ui.block2controllerBlockLengthDisplay.setText(str("{:.2f}".format(block_data_arr[1][1] * 3.28)))
		#block 3
		self.ui.block3controllerSpeedLimitDisplay.setText(str(block_data_arr[2][2] * .62))
		self.ui.block3controllerBlockLengthDisplay.setText(str("{:.2f}".format(block_data_arr[2][1] * 3.28)))
		#block 4
		self.ui.block4controllerSpeedLimitDisplay.setText(str(block_data_arr[3][2] * .62))
		self.ui.block4controllerBlockLengthDisplay.setText(str("{:.2f}".format(block_data_arr[3][1] * 3.28)))
		#block 5
		self.ui.block5controllerSpeedLimitDisplay.setText(str(block_data_arr[4][2] * .62))
		self.ui.block5controllerBlockLengthDisplay.setText(str("{:.2f}".format(block_data_arr[4][1] * 3.28)))
		#block 6
		self.ui.block6controllerSpeedLimitDisplay.setText(str(block_data_arr[5][2] * .62))
		self.ui.block6controllerBlockLengthDisplay.setText(str("{:.2f}".format(block_data_arr[5][1] * 3.28)))
		#block 7
		self.ui.block7controllerSpeedLimitDisplay.setText(str(block_data_arr[6][2] * .62))
		self.ui.block7controllerBlockLengthDisplay.setText(str("{:.2f}".format(block_data_arr[6][1] * 3.28)))
		#block 8
		self.ui.block8controllerSpeedLimitDisplay.setText(str(block_data_arr[7][2] * .62))
		self.ui.block8controllerBlockLengthDisplay.setText(str("{:.2f}".format(block_data_arr[7][1] * 3.28)))
		#block 9
		self.ui.block9controllerSpeedLimitDisplay.setText(str(block_data_arr[8][2] * .62))
		self.ui.block9controllerBlockLengthDisplay.setText(str("{:.2f}".format(block_data_arr[8][1] * 3.28)))
		#block 10
		self.ui.block10controllerSpeedLimitDisplay.setText(str(block_data_arr[9][2] * .62))
		self.ui.block10controllerBlockLengthDisplay.setText(str("{:.2f}".format(block_data_arr[9][1] * 3.28)))
		#block 11
		self.ui.block11controllerSpeedLimitDisplay.setText(str(block_data_arr[10][2] * .62))
		self.ui.block11controllerBlockLengthDisplay.setText(str("{:.2f}".format(block_data_arr[10][1] * 3.28)))
		#block 12
		self.ui.block12controllerSpeedLimitDisplay.setText(str(block_data_arr[11][2] * .62))
		self.ui.block12controllerBlockLengthDisplay.setText(str("{:.2f}".format(block_data_arr[11][1] * 3.28)))
		#block 13
		self.ui.block13controllerSpeedLimitDisplay.setText(str(block_data_arr[12][2] * .62))
		self.ui.block13controllerBlockLengthDisplay.setText(str("{:.2f}".format(block_data_arr[12][1] * 3.28)))
		#block 14
		self.ui.block14controllerSpeedLimitDisplay.setText(str(block_data_arr[13][2] * .62))
		self.ui.block14controllerBlockLengthDisplay.setText(str("{:.2f}".format(block_data_arr[13][1] * 3.28)))
		#block 15
		self.ui.block15controllerSpeedLimitDisplay.setText(str(block_data_arr[14][2] * .62))
		self.ui.block15controllerBlockLengthDisplay.setText(str("{:.2f}".format(block_data_arr[14][1] * 3.28)))




	def update_track_colors(self):
		#block 1
		if(block_data_arr[0][3] == True):
			self.ui.Block1.setStyleSheet("""background-color: rgb(255,0, 0)""")
			self.ui.Block1controllerOcc.setStyleSheet("""background-color: rgb(255,0, 0)""")
		else:
			self.ui.Block1.setStyleSheet("""background-color: rgb(0, 170, 0)""")
			self.ui.Block1controllerOcc.setStyleSheet("""background-color: rgb(0, 170, 0)""")
		#block 2
		if(block_data_arr[1][3] == True):
			self.ui.Block2.setStyleSheet("""background-color: rgb(255,0, 0)""")
			self.ui.Block2controllerOcc.setStyleSheet("""background-color: rgb(255,0, 0)""")
		else:
			self.ui.Block2.setStyleSheet("""background-color: rgb(0, 170, 0)""")
			self.ui.Block2controllerOcc.setStyleSheet("""background-color: rgb(0, 170, 0)""")
		#block 3
		if(block_data_arr[2][3] == True):
			self.ui.Block3.setStyleSheet("""background-color: rgb(255,0, 0)""")
			self.ui.Block3controllerOcc.setStyleSheet("""background-color: rgb(255,0, 0)""")
		else:
			self.ui.Block3.setStyleSheet("""background-color: rgb(0, 170, 0)""")
			self.ui.Block3controllerOcc.setStyleSheet("""background-color: rgb(0, 170, 0)""")
		#block 4
		if(block_data_arr[3][3] == True):
			self.ui.Block4.setStyleSheet("""background-color: rgb(255,0, 0)""")
			self.ui.Block4controllerOcc.setStyleSheet("""background-color: rgb(255,0, 0)""")
		else:
			self.ui.Block4.setStyleSheet("""background-color: rgb(0, 170, 0)""")
			self.ui.Block4controllerOcc.setStyleSheet("""background-color: rgb(0, 170, 0)""")
		#block 5
		if(block_data_arr[4][3] == True):
			self.ui.Block5.setStyleSheet("""background-color: rgb(255,0, 0)""")
			self.ui.Block5controllerOcc.setStyleSheet("""background-color: rgb(255,0, 0)""")
		else:
			self.ui.Block5.setStyleSheet("""background-color: rgb(0, 170, 0)""")
			self.ui.Block5controllerOcc.setStyleSheet("""background-color: rgb(0, 170, 0)""")
		#block 6
		if(block_data_arr[5][3] == True):
			self.ui.Block6.setStyleSheet("""background-color: rgb(255,0, 0)""")
			self.ui.Block6controllerOcc.setStyleSheet("""background-color: rgb(255,0, 0)""")
		else:
			self.ui.Block6.setStyleSheet("""background-color: rgb(0, 170, 0)""")
			self.ui.Block6controllerOcc.setStyleSheet("""background-color: rgb(0, 170, 0)""")
		#block 7
		if(block_data_arr[6][3] == True):
			self.ui.Block7.setStyleSheet("""background-color: rgb(255,0, 0)""")
			self.ui.Block7controllerOcc.setStyleSheet("""background-color: rgb(255,0, 0)""")
		else:
			self.ui.Block7.setStyleSheet("""background-color: rgb(0, 170, 0)""")
			self.ui.Block7controllerOcc.setStyleSheet("""background-color: rgb(0, 170, 0)""")
		#block 8
		if(block_data_arr[7][3] == True):
			self.ui.Block8.setStyleSheet("""background-color: rgb(255,0, 0)""")
			self.ui.Block8controllerOcc.setStyleSheet("""background-color: rgb(255,0, 0)""")
		else:
			self.ui.Block8.setStyleSheet("""background-color: rgb(0, 170, 0)""")
			self.ui.Block8controllerOcc.setStyleSheet("""background-color: rgb(0, 170, 0)""")
		#block 9
		if(block_data_arr[8][3] == True):
			self.ui.Block9.setStyleSheet("""background-color: rgb(255,0, 0)""")
			self.ui.Block9controllerOcc.setStyleSheet("""background-color: rgb(255,0, 0)""")
		else:
			self.ui.Block9.setStyleSheet("""background-color: rgb(0, 170, 0)""")
			self.ui.Block9controllerOcc.setStyleSheet("""background-color: rgb(0, 170, 0)""")
		#block 10
		if(block_data_arr[9][3] == True):
			self.ui.Block10.setStyleSheet("""background-color: rgb(255,0, 0)""")
			self.ui.Block10controllerOcc.setStyleSheet("""background-color: rgb(255,0, 0)""")
		else:
			self.ui.Block10.setStyleSheet("""background-color: rgb(0, 170, 0)""")
			self.ui.Block10controllerOcc.setStyleSheet("""background-color: rgb(0, 170, 0)""")
		#block 11
		if(block_data_arr[10][3] == True):
			self.ui.Block11.setStyleSheet("""background-color: rgb(255,0, 0)""")
			self.ui.Block11controllerOcc.setStyleSheet("""background-color: rgb(255,0, 0)""")
		else:
			self.ui.Block11.setStyleSheet("""background-color: rgb(0, 170, 0)""")
			self.ui.Block11controllerOcc.setStyleSheet("""background-color: rgb(0, 170, 0)""")
		#block 12
		if(block_data_arr[11][3] == True):
			self.ui.Block12.setStyleSheet("""background-color: rgb(255,0, 0)""")
			self.ui.Block12controllerOcc.setStyleSheet("""background-color: rgb(255,0, 0)""")
		else:
			self.ui.Block12.setStyleSheet("""background-color: rgb(0, 170, 0)""")
			self.ui.Block12controllerOcc.setStyleSheet("""background-color: rgb(0, 170, 0)""")
		#block 13
		if(block_data_arr[12][3] == True):
			self.ui.Block13.setStyleSheet("""background-color: rgb(255,0, 0)""")
			self.ui.Block13controllerOcc.setStyleSheet("""background-color: rgb(255,0, 0)""")
		else:
			self.ui.Block13.setStyleSheet("""background-color: rgb(0, 170, 0)""")
			self.ui.Block13controllerOcc.setStyleSheet("""background-color: rgb(0, 170, 0)""")
		#block 14
		if(block_data_arr[13][3] == True):
			self.ui.Block14.setStyleSheet("""background-color: rgb(255,0, 0)""")
			self.ui.Block14controllerOcc.setStyleSheet("""background-color: rgb(255,0, 0)""")
		else:
			self.ui.Block14.setStyleSheet("""background-color: rgb(0, 170, 0)""")
			self.ui.Block14controllerOcc.setStyleSheet("""background-color: rgb(0, 170, 0)""")
		#block 15
		if(block_data_arr[14][3] == True):
			self.ui.Block15.setStyleSheet("""background-color: rgb(255,0, 0)""")
			self.ui.Block15controllerOcc.setStyleSheet("""background-color: rgb(255,0, 0)""")
		else:
			self.ui.Block15.setStyleSheet("""background-color: rgb(0, 170, 0)""")
			self.ui.Block15controllerOcc.setStyleSheet("""background-color: rgb(0, 170, 0)""")

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())