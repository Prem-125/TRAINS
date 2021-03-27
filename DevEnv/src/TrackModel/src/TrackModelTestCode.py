import sys
import unittest
import csv
import ast
from TrackModel import *

class TestTackModel(unittest.TestCase)
	
	def test_speed_limit(self):
		trackBoi = Track()
		trackBoi.setLine("Blue")
		self.assert(trackBoi.getLine() == "Blue")
			
	def test_block(self):
		trackBoi = Track()
		trackBoi.setBlock(5)
		self.assert(trackBoi.getBlock() == 5)
			
	def test_grade(self):
		trackBoi = Track()
		trackBoi.setGrade(0.1)
		self.assert(trackBoi.getGrade() == 0.1)
		
	
	def test_speed_limit(self):
		trackBoi = Track()
		trackBoi.setSpeedLimit(31)
		self.assert(trackBoi.getSpeedLimit() == 31)
	
	def test_file_parsing(self):
		input_file = "BlueLine.txt"
		csv_file=open(input_file,'r')
		trackList = [Track()]
		with csv_file:
			
			csv_reader = csv.reader(csv_file, delimiter=',')
			
			#because python indexs by zero, i want a dummie object at trackList[0] since the file indexs the tracks by 1
				
			#assign every variable to each instance
			numLines=0
			for row in csv_reader:
				#because python indexs by zero, i want a dummie object at trackList[0] since the file indexs the tracks by 1
				#skip adding any values to track object at trackList[0]
				if numLines ==0:
					trackList.append(Track())	
					numLines+=1
				else:
					if(len(row) == 0):
						continue
					
					#add information to each track object
					
					trackList.append(Track())
					trackList[numLines].setLine(row[0])
					trackList[numLines].setSection(row[1])
					trackList[numLines].setBlock(int(row[2]))
					trackList[numLines].setLength(row[3])
					trackList[numLines].setGrade(row[4])
					trackList[numLines].setSpeedLimit(row[5])
					
					trackList[numLines].setStationSide(row[7])
					trackList[numLines].setElevation(row[8])
					trackList[numLines].setElevationC(row[9])
					
					#add base default values for each object 
					trackList[numLines].setHeaterStatus(False)
					trackList[numLines].setRailCondition(True)
					trackList[numLines].setCircuitCondition(True)
					trackList[numLines].setPowerCondition(True)
					trackList[numLines].setAmbientTemp(70)
					
					#temporary simulated signals from wayside
					trackList[numLines].setCommandedSpeed(35)
					trackList[numLines].setAuthority(137)
					trackList[numLines].setSignalLight('Go')
					trackList[numLines].setBeacon('Have a nice day!')
					trackList[numLines].setTicketCount(17)
					trackList[numLines].setOccupied(False)
					trackList[numLines].setIsCrossing(False)
					trackList[numLines].setIsBranch(False)
					trackList[numLines].setIsSwitchLeg(False)
					
			
					#load infrastructure
					trackList[numLines].setInfrastructure(row[6])
					
					#print(self.trackList[self.numLines].getBlock())
					numLines+=1
					
		
		
		self.assert(trackList[4].getBlock()==4)
		self.assert(trackList[4].getLine()=="Blue")
		self.assert(trackList[4].getSection()=='A')
		self.assert(trackList[4].getLength()==50)
		self.assert(trackList[4].getGrade() == 0)
		self.assert(trackList[4].getSpeed_limit()==50)
		self.assert(trackList[4].getInfrastructure()=='')
		self.assert(trackList[4].getElevation()==0)
		
		#close the opened file
		csv_file.close()	
		 
	def test_rail_failure(self):
		trackBoi = Track()
		trackBoi.setRailCondition(False)
		self.assert(trackBoi.getRailCondition() == False)	
		self.assert(trackBoi.getOccupied()==True)
		trackBoi.setRailCondition(True)
		self.assert(trackBoi.getRailCondition() == True)	
		self.assert(trackBoi.getOccupied()==False)

	def test_circuit_failure(self):
		trackBoi = Track()
		trackBoi.setCircuitCondition(False)
		self.assert(trackBoi.getCircuitCondition() == False)	
		trackBoi.setCircuitCondition(True)
		self.assert(trackBoi.getCircuitCondition() == True)		
	
	def test_power_failure(self):
		trackBoi = Track()
		trackBoi.setPowerCondition(False)
		self.assert(trackBoi.getPowerCondition() == False)	
		trackBoi.setPowerCondition(True)
		self.assert(trackBoi.getPowerCondition() == True)	
	
	def test_rail_failure(self):
		trackBoi = Track()
		infrastructure_string="Switch ( 5 6 ) or ( 5 11 )"
		trackBoi.set_infrastructure(infrastructure_string)
		self.assert(trackBoi.getIsSwitch()==True)
		self.assert(trackBoi.switchNum==1)
		
	def test_commanded_speed(self):
		trackBoi = Track()
		trackBoi.setCommandedSpeed(34.3)
		self.assert(trackBio.getCommandedSpeed==34.3)
		
if __name__ == '__main__':
    unittest.main()