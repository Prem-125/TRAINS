import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from UI import Ui_Dialog

#extra imported items
import csv
import ast


#switch class
class Switch:
	def _init_(self):	
		self.currentSwitchPos=currentSwitchPos
		self.yStem = yStem
		self.yZero = yZero
		self.yOne = yOne
	
	#declare set/get functions
	def getSwitchPosition(self):
		return self.currentSwitchPos
	def setSwitchPosition(self,pos):
		self.currentSwitchPos=pos

	def getYstem(self):
		return self.yStem
	def setYstem(self, newYstem):
		self.yStem=newYstem

	def getYzero(self):
		return self.yZero
	def setYzero(self, newYzero):
		self.yZero=newYzero

	def getYone(self):
		return self.yOne
	def setYone(self, newYone):
		self.yOne=newYone

#track class
class Track:

	switchList = [Switch()]
	switchNum = 0
	
	def _init_(self):	
		self.line = line
		self.section = section
		self.block = block
		self.length = length
		self.grade = grade
		self.infrastructure=infrastructure
		self.elevation=elevation
		self.elevationC=elevationC
		self.stationSide=stationSide
		self.speedLimit = speedLimit
		self.commandSpeed = commandSpeed #float w 2 decimal points
		self.beacon = beacon
		self.signalLight = signalLight
		self.occupied = occupied
		self.heaterStatus= heaterStatus
		self.connectionTrackA = connectionTrackA
		self.connectionTrackB = connectionTrackB
		
		self.railCondition = railCondition
		self.circuitCondition = circuitCondition
		self.powerCondition = powerCondition
		self.ambientTemp = ambientTemp
		self.authority = authority
		
		
		#station variables
		self.ticketCount = ticketCount
		self.isStation = isStation
		self.stationName = stationName
		
		#crossing Variables
		self.isCrossing = isCrossing
		
		#branch variable
		self.isBranch = isBranch
		
		#swithc variable
		self.isSwitch = isSwitch
		self.isSwitchLeg = isSwitchLeg
		
	#set and get functions for each variable 
	#make output signal variable for each module and have an update function to update them all
	def getLine(self):
		return self.line
	def setLine(self, inLine):
		self.line=inLine
	
	def getSection(self):
		return self.section
	def setSection(self, inSec):
		self.section=inSec
		
	def getBlock(self):
		return self.block
	def setBlock(self, inBlock):
		self.block=inBlock
	
	def getLength(self):
		return self.length
	def setLength(self, inLength):
		self.length=inLength
	
	def getGrade(self):
		return self.grade
	def setGrade(self, inGrade):
		self.grade=inGrade

	def getInfrastructure(self):
		return self.connectionTrackB
	def setInfrastructure(self, inInfra):
		self.infrastructure=inInfra
		self.infraParse()
		#do more
		
	def getStationSide(self):
		return self.stationSide
	def setStationSide(self, inSide):
		self.stationSide=inSide
		
	def getElevation(self):
		return self.elevation
	def setElevation(self, inElevation):
		self.elevation=inElevation
		
	def getElevationC(self):
		return self.elevationC
	def setElevationC(self, inElevationC):
		self.elevationC=inElevationC

	def getSpeedLimit(self):
		return self.speedLimit
	def setSpeedLimit(self, inSpeedLimit):
		self.speedLimit=inSpeedLimit
		
	def getCommandedSpeed(self):
		return self.commandSpeed
	def setCommandedSpeed(self, inCommandedSpeed):
		self.commandSpeed=inCommandedSpeed

	def getBeacon(self):
		return self.beacon
	def setBeacon(self, inBeacon):
		self.beacon=inBeacon

	def getSignalLight(self):
		return self.signalLight
	def setSignalLight(self, inSignalLight):
		self.signalLight=inSignalLight
		
	def getOccupied(self):
		return self.occupied
	def setOccupied(self, inOccupied):
		self.occupied=inOccupied

	def getConnectionTrackA(self):
		return self.connectionTrackA
	def setConnectionTrackA(self, inTrackA):
		self.connectionTrackA=inTrackA
		
	def getConnectionTrackB(self):
		return self.connectionTrackB
	def setConnectionTrackB(self, inTrackB):
		self.connectionTrackB=inTrackB

	def getHeaterStatus(self):
		return self.heaterStatus
	def setHeaterStatus(self, inHeat):
		self.heaterStatus=inHeat
	
	def getRailCondition(self):
		return self.railCondition
	def setRailCondition(self, inCondition):
		self.railCondition=inCondition

	def getCircuitCondition(self):
		return self.circuitCondition
	def setCircuitCondition(self, inCondition):
		self.circuitCondition=inCondition

	def getPowerCondition(self):
		return self.powerCondition
	def setPowerCondition(self, inCondition):
		self.powerCondition=inCondition

	def getAmbientTemp(self):
		return self.ambientTemp
	def setAmbientTemp(self, inCondition):
		self.ambientTemp=inCondition

	def getAuthority(self):
		return self.authority
	def setAuthority(self, inCondition):
		self.authority=inCondition
		
	def getTicketCount(self):
		return self.ticketCount
	def setTicketCount(self, inCondition):
		self.ticketCount=inCondition

	def getIsStation(self):
		return self.isStation
	def setIsStation(self, inCondition):
		self.isStation=inCondition		
	
	def getStationName(self):
		return self.stationName
	def setStationName(self, inCondition):
		self.stationName=inCondition
	
	def getIsCrossing(self):
		return self.isCrossing
	def setIsCrossing(self, inCondition):
		self.isCrossing=inCondition

	def getIsBranch(self):
		return self.isBranch
	def setIsBranch(self, inCondition):
		self.isBranch=inCondition
	
	def getIsSwitch(self):
		return self.isSwitch
	def setIsSwitch(self, inCondition):
		self.isSwitch=inCondition	

	def getIsSwitchLeg(self):
		return self.isSwitchLeg
	def setIsSwitchLeg(self, inCondition):
		self.isSwitchLeg=inCondition		
	
	#function parse the infrastructure input
	def infraParse(self):
		#print(self.infrastructure)
		#if there is no infrastructure, exit the function
		if self.infrastructure == '':
			self.setIsStation(False)
			self.setIsSwitch(False)
			self.setIsBranch(False)
			
			return None
	
		#this list contains atributes of infrastructure such a station/undergorund
		listAtrib=self.infrastructure.split(';')
		
		#if there is only one atribute
		if len(listAtrib) == 1:
			#split up atribute by the spacing
			atrib=listAtrib[0].split(' ')	
			#print(atrib)
				
			#check to see if atribute is a station:
			if(atrib[0] == 'Station'):
				self.setIsStation(True)
				self.setStationName(atrib[0]+' '+atrib[1])
				sampleString = self.getStationName()
				#print(sampleString)
				self.setBeacon('Welcome to ' + sampleString)
				#print(self.getBeacon())
				#print("Station is" ,self.getStationName())
			else:
				self.setIsStation(False)
			
			#check to see if atribute is a swtich
			if(atrib[0] == 'Switch'):	
				#check to see if it is the stem of the swtich
				if (len(atrib) > 5):
					self.setIsSwitch(True)
					Track.switchNum+=1
					#print("stem is ", self.getBlock())
					Track.switchList.append(Switch())
					Track.switchList[Track.switchNum].setYstem(self.getBlock())
					yZeroIn = int(atrib[3])
					yOneIn = int(atrib[8])
					Track.switchList[Track.switchNum].setSwitchPosition(False)
					Track.switchList[Track.switchNum].setYzero(yZeroIn)
					Track.switchList[Track.switchNum].setYone(yOneIn)
					#print("zero is ", Track.switchList[Track.switchNum].getYzero(), " and one is ", Track.switchList[Track.switchNum].getYone(), "and switch position is", Track.switchList[Track.switchNum].getSwitchPosition())
					self.setIsSwitchLeg(False)
					
				else: 
					self.setIsSwitch(False)
					self.setIsSwitchLeg(True)
					
			else:
				self.setIsSwitch(False)
				self.setIsSwitchLeg(False)
				

#Code for the UI
class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		
		#global instance variables
		self.trackList = [Track()]
		self.numLines = 0
		self.currentBlock = 0
		
		#if load track button is pressed
		self.ui.getTrackFileBTN.clicked.connect(self.loadTrack)
		
		#if get track is pressed then update all relvant information
		self.ui.getTrackBTN.clicked.connect(self.getTrackInfo)
		
		#if toggle heater is pressed 
		self.ui.heaterToggleBTN.clicked.connect(self.toggleHeater)
		
		#if button pressed then update the temperature
		self.ui.setTempBTN.clicked.connect(self.setTrackTemperature)
	
		#if buttons pressed cause a failure respective to the button
		self.ui.breakRailBTN.clicked.connect(self.causeRailFail)
		self.ui.breakCircuitBTN.clicked.connect(self.causeCircuitFail)
		self.ui.breakPowerBTN.clicked.connect(self.causePowerFail)
	
		#if button pressed swap switch
		self.ui.waySwitchBTN.clicked.connect(self.swapSwitch)
	
	#function to load track from a file
	def loadTrack(self):
		#if self.upTrackBlue.getChecked()==true
		inputFileName=self.ui.lineEdit.text();
		#open csv reader for inputFile
		try: 
			csv_file=open(inputFileName,'r')
		
		#check to see if the inputted file name is valid
		except OSError:
			print("Invalid File name")
			self.ui.trackFileValid.setText("Invalid File")
			
				
		with csv_file:
			self.ui.trackFileValid.setText("Valid File")
			csv_reader = csv.reader(csv_file, delimiter=',')
			
			#because python indexs by zero, i want a dummie object at trackList[0] since the file indexs the tracks by 1
				
			#assign every variable to each instance
			self.numLines=0
			for row in csv_reader:
				#because python indexs by zero, i want a dummie object at trackList[0] since the file indexs the tracks by 1
				#skip adding any values to track object at trackList[0]
				if self.numLines ==0:
					self.trackList.append(Track())	
					self.numLines+=1
				else:
					if(len(row) == 0):
						continue
					
					#add information to each track object
					#print(row)
					self.trackList.append(Track())
					self.trackList[self.numLines].setLine(row[0])
					self.trackList[self.numLines].setSection(row[1])
					self.trackList[self.numLines].setBlock(int(row[2]))
					self.trackList[self.numLines].setLength(row[3])
					self.trackList[self.numLines].setGrade(row[4])
					self.trackList[self.numLines].setSpeedLimit(row[5])
					
					self.trackList[self.numLines].setStationSide(row[7])
					self.trackList[self.numLines].setElevation(row[8])
					self.trackList[self.numLines].setElevationC(row[9])
					
					#add base default values for each object 
					self.trackList[self.numLines].setHeaterStatus(False)
					self.trackList[self.numLines].setRailCondition(True)
					self.trackList[self.numLines].setCircuitCondition(True)
					self.trackList[self.numLines].setPowerCondition(True)
					self.trackList[self.numLines].setAmbientTemp(70)
					
					#temporary simulated signals from wayside
					self.trackList[self.numLines].setCommandedSpeed(35)
					self.trackList[self.numLines].setAuthority(137)
					self.trackList[self.numLines].setSignalLight('Go')
					self.trackList[self.numLines].setBeacon('Have a nice day!')
					self.trackList[self.numLines].setTicketCount(17)
					self.trackList[self.numLines].setOccupied(False)
					self.trackList[self.numLines].setIsCrossing(False)
					self.trackList[self.numLines].setIsBranch(False)
					self.trackList[self.numLines].setIsSwitchLeg(False)
					
					#self.trackList[self.numLines].setConnectionTrackA(self.trackList[0])
					#self.trackList[self.numLines].setConnectionTrackB(self.trackList[0])
					
					#load infrastructure
					self.trackList[self.numLines].setInfrastructure(row[6])
					
					#print(self.trackList[self.numLines].getBlock())
					self.numLines+=1
					
					
		#close the opened file
		csv_file.close()			
			
	def getTrackInfo(self):
		#get the text inputted by the user and check to see if it's a number
		try :
			inputTrackBlock=int(self.ui.trackSelector.text())
		except:
			print("Inputted Track Block Not a Number")
			self.ui.trackSelectorValid.setText("Invalid Input\nNot a Number")
		
		if(inputTrackBlock > self.numLines):
			print("Input Track Block too High")
			self.ui.trackSelectorValid.setText("Invalid Input\nBlock Number Too High")
		
		#otherwise it is a valid input and update everything
		self.ui.trackSelectorValid.setText("Valid Input")
		self.currentBlock=inputTrackBlock
		self.updateTrackInfo(inputTrackBlock)
	
		# deafult update every output for block1
		#self.updateTrackInfo(1)
	
	
	def causeRailFail(self):
		#toggle status
		temp = not self.trackList[self.currentBlock].getRailCondition()
		
		if(temp == False):
			self.trackList[self.currentBlock].setRailCondition(False)
			self.trackList[self.currentBlock].setSignalLight('Stop')
			self.updateTrackInfo(self.currentBlock)
			print("CAUTION! RAIL FAILURE ON BLOCK ", self.currentBlock) 
		else:
			self.trackList[self.currentBlock].setRailCondition(True)
			#make sure to send go if all track conditions are good
			if(self.trackList[self.currentBlock].getCircuitCondition() == True) and (self.trackList[self.currentBlock].getPowerCondition() == True):
				self.trackList[self.currentBlock].setSignalLight('Go')
			self.updateTrackInfo(self.currentBlock)
			print("RAIL Fixed on BLOCK ", self.currentBlock) 

	def causeCircuitFail(self):
		#toggle status
		temp = not self.trackList[self.currentBlock].getCircuitCondition()
		
		if(temp == False):
			self.trackList[self.currentBlock].setCircuitCondition(False)
			self.trackList[self.currentBlock].setSignalLight('Stop')
			self.updateTrackInfo(self.currentBlock)
			print("CAUTION! CIRCUIT FAILURE ON BLOCK ", self.currentBlock) 
		else:
			self.trackList[self.currentBlock].setCircuitCondition(True)
			#make sure to send go if all track conditions are good
			if(self.trackList[self.currentBlock].getRailCondition() == True) and (self.trackList[self.currentBlock].getPowerCondition() == True):
				self.trackList[self.currentBlock].setSignalLight('Go')
			self.updateTrackInfo(self.currentBlock)
			print("CIRCUIT Fixed on BLOCK ", self.currentBlock) 

	def causePowerFail(self):
		#toggle status
		temp = not self.trackList[self.currentBlock].getPowerCondition()
		
		if(temp == False):
			self.trackList[self.currentBlock].setPowerCondition(False)
			self.trackList[self.currentBlock].setSignalLight('Stop')
			self.updateTrackInfo(self.currentBlock)
			print("CAUTION! POWER FAILURE ON BLOCK ", self.currentBlock) 
		else:
			self.trackList[self.currentBlock].setPowerCondition(True)
			#make sure to send go if all track conditions are good
			if(self.trackList[self.currentBlock].getRailCondition() == True) and (self.trackList[self.currentBlock].getCircuitCondition() == True):
				self.trackList[self.currentBlock].setSignalLight('Go')
			self.updateTrackInfo(self.currentBlock)
			print("POWER Fixed on BLOCK ", self.currentBlock) 
			
	
	def toggleHeater(self):
		temp = not self.trackList[self.currentBlock].getHeaterStatus()
		self.trackList[self.currentBlock].setHeaterStatus(temp)		
		self.updateTrackInfo(self.currentBlock)
	
	def setTrackTemperature(self):
		try :
			inputTemp=int(self.ui.tempSelector.text())
		except:
			print("Inputted Temperature Not a Number")
			self.ui.tempSelectorValid.setText("Invalid Input\nNot a Number")
		
		if(inputTemp > 118):
			print("Input Track Block too High")
			self.ui.tempSelectorValid.setText("Invalid Input\nTemp Too High")
	
		if(inputTemp < -50):
			print("Input Track Temp too Low")
			self.ui.tempSelectorValid.setText("Invalid Input\nTemp Too Low")
	
		if inputTemp<32:
			self.trackList[self.currentBlock].setHeaterStatus(True)
		else:
			self.trackList[self.currentBlock].setHeaterStatus(False)
		
		self.trackList[self.currentBlock].setAmbientTemp(inputTemp)
		self.updateTrackInfo(self.currentBlock)
	
	def swapSwitch(self): #change this to be inside the swtich class
		if(self.trackList[self.currentBlock].getIsSwitch() == True):
			temp = not self.trackList[self.currentBlock].switchList[Track.switchNum].getSwitchPosition()
			self.trackList[self.currentBlock].switchList[Track.switchNum].setSwitchPosition(temp)
			self.updateTrackInfo(self.currentBlock)
	
	def updateTrackInfo(self,blckNum):
		
		print("-----------------------------------------------------------------------------------")
		#update any connections
		#make track connections
		i=1
		while (i <= self.numLines-1):
			#print(self.trackList[i].getBlock())
			if self.trackList[i].getIsSwitch()==False and  self.trackList[i].getIsSwitchLeg()==False :						
				if i == 1:
					self.trackList[i].setConnectionTrackA(None)
					self.trackList[i].setConnectionTrackB(self.trackList[i+1])
				
				if i == self.numLines or self.trackList[i].getIsStation()==True:
					self.trackList[i].setConnectionTrackA(self.trackList[i-1])
					self.trackList[i].setConnectionTrackB(None)
				else:
					self.trackList[i].setConnectionTrackA(self.trackList[i-1])
					self.trackList[i].setConnectionTrackB(self.trackList[i+1])
								
			else:
				#print('d')
				if self.trackList[i].switchList[Track.switchNum].getSwitchPosition() == False:
					#print('h')
					self.trackList[i].setConnectionTrackA(self.trackList[Track.switchList[1].getYstem()])
					self.trackList[i].setConnectionTrackB(self.trackList[Track.switchList[1].getYzero()])
					self.trackList[Track.switchList[1].getYone()].setConnectionTrackA(None)
				
				if self.trackList[i].switchList[Track.switchNum].getSwitchPosition() == True:
					self.trackList[i].setConnectionTrackA(self.trackList[Track.switchList[1].getYstem()])
					self.trackList[i].setConnectionTrackB(self.trackList[Track.switchList[1].getYone()])
					self.trackList[Track.switchList[1].getYzero()].setConnectionTrackA(None)				
				
				
			
			print(self.trackList[i].getBlock()," Con A = ", self.trackList[i].getConnectionTrackA(), "Con B = ",self.trackList[i].getConnectionTrackB())
			
			i+=1
		
		#update every label with relevant information
		self.ui.selTrackSection.setText(str(self.trackList[blckNum].getLine()))
		
		
		self.ui.selTrackSpeed.display(self.trackList[blckNum].getSpeedLimit())
		
		self.ui.selTrackGrade.setText(str(self.trackList[blckNum].getGrade()))
		self.ui.selTrackHeater.setText(str(self.trackList[blckNum].getHeaterStatus()))
		
		if(self.trackList[blckNum].getIsStation() == True):
			self.ui.selTrackStation.setText(self.trackList[blckNum].getStationName())	
			#CTC outputs
			self.ui.ctcTicketO.display(self.trackList[blckNum].getTicketCount())
			self.ui.ctcTrackUpO.setText("Tickets Updated")
		else:
			self.ui.selTrackStation.setText('Not a Station')
			self.ui.ctcTicketO.display(0)
			self.ui.ctcTrackUpO.setText("Not a Station")
			
		if(self.trackList[blckNum].getIsCrossing() == True):
			self.ui.selTrackCross.setText('Yes')
		else:
			self.ui.selTrackCross.setText('No')
		
		if(self.trackList[blckNum].getIsCrossing() == True):
			self.ui.selTrackBranch.setText('Yes')
		else:
			self.ui.selTrackBranch.setText('No')	

		if(self.trackList[blckNum].getIsSwitch() == True):
			self.ui.selTrackSW.setText('Yes')
			self.ui.waySwitch.setText(str(self.trackList[blckNum].getConnectionTrackB().getBlock()))
			#SET CONNECTIONS BOYOY
		else:
			self.ui.selTrackSW.setText('No')	
			self.ui.waySwitch.setText('Not a switch')
		
		
		#railStatus
		self.ui.selTrackRailStat.setText(str(self.trackList[blckNum].getRailCondition()))
		self.ui.selTrackCircStat.setText(str(self.trackList[blckNum].getCircuitCondition()))
		self.ui.selTrackPowerStat.setText(str(self.trackList[blckNum].getPowerCondition()))
		
	
		
		#railSignal
		if(self.trackList[blckNum].getSignalLight() == 'Go'):
			self.ui.sigGo.setChecked(True)
			self.ui.sigSlow.setChecked(False)
			self.ui.sigStop.setChecked(False)
		elif(self.trackList[blckNum].getSignalLight() == 'Slow'):
			self.ui.sigGo.setChecked(False)
			self.ui.sigSlow.setChecked(True)
			self.ui.sigStop.setChecked(False)
		elif(self.trackList[blckNum].getSignalLight() == 'Stop'):
			self.ui.sigGo.setChecked(False)
			self.ui.sigSlow.setChecked(False)
			self.ui.sigStop.setChecked(True)
		
		#temperature
		self.ui.ambTemp.display(self.trackList[blckNum].getAmbientTemp())
		
		#wayside input
		self.ui.wayCommandedSpeed.display(self.trackList[blckNum].getCommandedSpeed())
		self.ui.wayAuthority.display(self.trackList[blckNum].getAuthority())
		self.ui.waySignal.setText(self.trackList[blckNum].getSignalLight())
		
		#train outputs
		self.ui.trainSpeedLimitO.display(self.trackList[blckNum].getSpeedLimit())
		self.ui.trainAuthorityO.display(self.trackList[blckNum].getAuthority())
		self.ui.trainBeaconO.setText(self.trackList[blckNum].getBeacon())
	
		
		#Wayside outputs
		self.ui.wayOccupiedO.setText(str(self.trackList[blckNum].getOccupied()))
		
		
if __name__ == "__main__":
	app = QApplication(sys.argv)

	window = MainWindow()

	#put code here
	
	window.show()
		
	sys.exit(app.exec_())
	
	
	
	
	
	
	