import sys
import serial
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, QTimer
from test1 import Ui_TrainModelInterface

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.ui = Ui_TrainModelInterface()
		self.ui.setupUi(self)
		self.utimer = QTimer()
		self.utimer.timeout.connect(self.updateVal)
		self.utimer.start(1000)
		self.testval=0
		#self.arduino = serial.Serial(port='COM4', baudrate=115200)
		
	def updateVal(self):
		#status = self.arduino.read(2)	
		self.testval = self.testval + 1
		self.ui.PowerVal.setPlainText(str(self.testval))

if __name__ == "__main__":
	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()

	sys.exit(app.exec_())
