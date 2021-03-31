import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from TrackModel.src.UI import Ui_Dialog
from signals import signals


#extra imported items
import csv
import ast
import random

#i currently need to change the function to that of which will match the coding standards

#switch class
class Switch:
	def _init_(self):	
		self.current_switch_pos=current_switch_pos
		self.y_stem = y_stem
		self.y_zero = y_zero
		self.y_one = y_one
	
	#declare set/get functions
	def get_switch_position(self):
		return self.current_switch_pos
	def set_switch_position(self,pos):
		self.current_switch_pos=pos

	def get_y_stem(self):
		return self.y_stem
	def set_y_stem(self, newy_stem):
		self.y_stem=newy_stem

	def get_y_zero(self):
		return self.y_zero
	def set_y_zero(self, newy_Zero):
		self.y_zero=newy_Zero

	def get_y_one(self):
		return self.y_one
	def set_y_one(self, newy_One):
		self.y_one=newy_One

#track class
class Track:

	switch_list = [Switch()]
	switch_num = 0
	
	def _init_(self):	
		self.line = line
		self.section = section
		self.block = block
		self.length = length
		self.grade = grade
		self.infrastructure=infrastructure
		self.elevation=elevation
		self.elevation_c=elevation_c
		self.station_side=station_side
		self.speed_limit = speed_limit
		self.commanded_speed = commanded_speed #float w 2 decimal points
		self.beacon = beacon
		self.signal_light = signal_light
		self.occupied = occupied
		self.heater_status= heater_status
		self.connection_track_a = connection_track_a
		self.connection_track_b = connection_track_b
		
		self.rail_condition = rail_condition
		self.circuit_condition = circuit_condition
		self.power_condition = power_condition
		self.ambient_temp = ambient_temp
		self.authority = authority
		
		
		#station variables
		self.ticket_count = ticket_count
		self.is_station = is_station
		self.station_name = station_name
		self.boarding_count = boarding_count
		
		#crossing Variables
		self.is_crossing = is_crossing
		
		#branch variable
		self.is_branch = is_branch
		
		#swithc variable
		self.is_switch = is_switch
		self.is_switch_leg = is_switch_leg
		
	#set and get functions for each variable 
	#make output signal variable for each module and have an update function to update them all
	def get_line(self):
		return self.line
	def set_line(self, in_line):
		self.line=in_line
	
	def get_section(self):
		return self.section
	def set_section(self, in_sec):
		self.section=in_sec
		
	def get_block(self):
		return self.block
	def set_block(self, in_block):
		self.block=in_block
	
	def get_length(self):
		return self.length
	def set_length(self, in_length):
		self.length=in_length
	
	def get_grade(self):
		return self.grade
	def set_grade(self, in_grade):
		self.grade=in_grade

	def get_infrastructure(self):
		return self.connection_track_b
	def set_infrastructure(self, in_infra):
		self.infrastructure=in_infra
		self.infra_parse()
		#do more
		
	def get_station_side(self):
		return self.station_side
	def set_station_side(self, in_side):
		self.station_side=in_side
		
	def get_elevation(self):
		return self.elevation
	def set_elevation(self, in_elevation):
		self.elevation=in_elevation
		
	def get_elevation_c(self):
		return self.elevation_c
	def set_elevation_c(self, in_elevation_c):
		self.elevation_c=in_elevation_c

	def get_speed_limit(self):
		return self.speed_limit
	def set_speed_limit(self, in_speed_limit):
		self.speed_limit=in_speed_limit
		
	def get_commanded_speed(self):
		return self.commanded_speed
	def set_commanded_speed(self, in_commanded_speed):
		self.commanded_speed=in_commanded_speed

	def get_beacon(self):
		return self.beacon
	def set_beacon(self, in_beacon):
		self.beacon=in_beacon

	def get_signal_light(self):
		return self.signal_light
	def set_signal_light(self, in_signal_light):
		self.signal_light=in_signal_light
		
	def get_occupied(self):
		return self.occupied
	def set_occupied(self, in_occupied):
		self.occupied=in_occupied

	def get_connection_track_a(self):
		return self.connection_track_a
	def set_connection_track_a(self, in_track_a):
		self.connection_track_a=in_track_a
		
	def get_connection_track_b(self):
		return self.connection_track_b
	def set_connection_track_b(self, in_track_b):
		self.connection_track_b=in_track_b

	def get_heater_status(self):
		return self.heater_status
	def set_heater_status(self, in_heat):
		self.heater_status=in_heat
	
	def get_rail_condition(self):
		return self.rail_condition
	def set_rail_condition(self, in_condition):
		self.rail_condition=in_condition

	def get_circuit_condition(self):
		return self.circuit_condition
	def set_circuit_condition(self, in_condition):
		self.circuit_condition=in_condition

	def get_power_condition(self):
		return self.power_condition
	def set_power_condition(self, in_condition):
		self.power_condition=in_condition

	def get_ambient_temp(self):
		return self.ambient_temp
	def set_ambient_temp(self, inCondition):
		self.ambient_temp=inCondition

	def get_authority(self):
		return self.authority
	def set_authority(self, in_condition):
		self.authority=in_condition
		
	def get_ticket_count(self):
		return self.ticket_count
	def set_ticket_count(self, in_condition):
		self.ticket_count=in_condition

	def get_is_station(self):
		return self.is_station
	def set_is_station(self, in_condition):
		self.is_station=in_condition		
	
	def get_station_name(self):
		return self.station_name
	def set_station_name(self, in_condition):
		self.station_name=in_condition
	
	def get_is_crossing(self):
		return self.is_crossing
	def set_is_crossing(self, in_condition):
		self.is_crossing=in_condition

	def get_is_branch(self):
		return self.is_branch
	def set_is_branch(self, in_condition):
		self.is_branch=in_condition
	
	def get_is_switch(self):
		return self.is_switch
	def set_is_switch(self, in_condition):
		self.is_switch=in_condition	

	def get_is_switch_leg(self):
		return self.is_switch_leg
	def set_is_switch_leg(self, in_condition):
		self.is_switch_leg=in_condition	

	def get_boarding_count(self):
		return self.boarding_count
	def set_boarding_count(self, in_condition):
		self.boarding_count=in_condition
	
	#function parse the infrastructure input
	def infra_parse(self):
		#print(self.infrastructure)
		#if there is no infrastructure, exit the function
		if self.infrastructure == '':
			self.set_is_station(False)
			self.set_is_switch(False)
			self.set_is_branch(False)
			
			return None
	
		#this list contains atributes of infrastructure such a station/undergorund
		list_atrib=self.infrastructure.split(';')
		
		#if there is only one atribute
		if len(list_atrib) == 1:
			#split up atribute by the spacing
			atrib=list_atrib[0].split(' ')	
			#print(atrib)
				
			#check to see if atribute is a station:
			if(atrib[0] == 'Station'):
				self.set_is_station(True)
				self.set_station_name(atrib[0]+' '+atrib[1])
				sample_string = self.get_station_name()
				#print(sample_string)
				self.set_beacon('Welcome to ' + sample_string)
				self.generate_random_ticket()
				self.generate_boarding()
				#print(self.get_beacon())
				#print("Station is" ,self.get_station_name())
			else:
				self.set_is_station(False)
			
			#check to see if atribute is a swtich
			if(atrib[0] == 'Switch'):	
				#check to see if it is the stem of the swtich
				if (len(atrib) > 5):
					self.set_is_switch(True)
					Track.switch_num+=1
					#print("stem is ", self.get_block())
					Track.switch_list.append(Switch())
					Track.switch_list[Track.switch_num].set_y_stem(self.get_block())
					y_zero_in = int(atrib[3])
					y_one_in = int(atrib[8])
					Track.switch_list[Track.switch_num].set_switch_position(False)
					Track.switch_list[Track.switch_num].set_y_zero(y_zero_in)
					Track.switch_list[Track.switch_num].set_y_one(y_one_in)
					#print("zero is ", Track.switch_list[Track.switch_num].set_y_zero(), " and one is ", Track.switch_list[Track.switch_num].set_y_one(), "and switch position is", Track.switch_list[Track.switch_num].get_switch_position())
					self.set_is_switch_leg(False)
					
				else: 
					self.set_is_switch(False)
					self.set_is_switch_leg(True)
					
			else:
				self.set_is_switch(False)
				self.set_is_switch_leg(False)
				
	#function to generate a random amount of tickets
	def generate_random_ticket(self):
		self.set_ticket_count(random.randint(1,30))
		self.generate_boarding()
		
	#function to generate the amount of people boarding
	def generate_boarding(self):
		self.set_boarding_count(random.randint(1, self.get_ticket_count()))
		
	
#Code for the UI
class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		
		#global instance variables
		self.track_list = [Track()]
		self.num_lines = 0
		self.current_block = 0
		
		#if load track button is pressed
		self.ui.getTrackFileBTN.clicked.connect(self.load_track)
		
		#if get track is pressed then update all relvant information
		self.ui.getTrackBTN.clicked.connect(self.get_track_info)
		
		#if toggle heater is pressed 
		self.ui.heaterToggleBTN.clicked.connect(self.toggle_heater)
		
		#if button pressed then update the temperature
		self.ui.setTempBTN.clicked.connect(self.set_track_temperature)
	
		#if buttons pressed cause a failure respective to the button
		self.ui.breakRailBTN.clicked.connect(self.cause_rail_fail)
		self.ui.breakCircuitBTN.clicked.connect(self.cause_circuit_fail)
		self.ui.breakPowerBTN.clicked.connect(self.cause_power_fail)
	
		#if button pressed swap switch

		self.ui.waySwitchBTN.clicked.connect(self.swapSwitch)
		signals.test.connect(self.signalTest)
	#function to load track from a file
	def signalTest(self,input):
		self.ui.trackFileValid.setText(str(input))
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
			
			#because python indexs by zero, i want a dummie object at track_list[0] since the file indexs the tracks by 1
				
			#assign every variable to each instance
			self.num_lines=0
			for row in csv_reader:
				#because python indexs by zero, i want a dummie object at track_list[0] since the file indexs the tracks by 1
				#skip adding any values to track object at track_list[0]
				if self.num_lines ==0:
					self.track_list.append(Track())	
					self.num_lines+=1
				else:
					if(len(row) == 0):
						continue
					
					#add information to each track object
					#print(row)
					self.track_list.append(Track())
					self.track_list[self.num_lines].set_line(row[0])
					self.track_list[self.num_lines].set_section(row[1])
					self.track_list[self.num_lines].set_block(int(row[2]))
					self.track_list[self.num_lines].set_length(row[3])
					self.track_list[self.num_lines].set_grade(row[4])
					self.track_list[self.num_lines].set_speed_limit(row[5])
					
					self.track_list[self.num_lines].set_station_side(row[7])
					self.track_list[self.num_lines].set_elevation(row[8])
					self.track_list[self.num_lines].set_elevation_c(row[9])
					
					#add base default values for each object 
					self.track_list[self.num_lines].set_heater_status(False)
					self.track_list[self.num_lines].set_rail_condition(True)
					self.track_list[self.num_lines].set_circuit_condition(True)
					self.track_list[self.num_lines].set_power_condition(True)
					self.track_list[self.num_lines].set_ambient_temp(70)
					
					#temporary simulated signals from wayside
					self.track_list[self.num_lines].set_commanded_speed(35)
					self.track_list[self.num_lines].set_authority(137.1)
					self.track_list[self.num_lines].set_signal_light('Go')
					self.track_list[self.num_lines].set_beacon('Have a nice day!')
					#self.track_list[self.num_lines].set_ticket_count(17)
					self.track_list[self.num_lines].set_occupied(False)
					self.track_list[self.num_lines].set_is_crossing(False)
					self.track_list[self.num_lines].set_is_branch(False)
					self.track_list[self.num_lines].set_is_switch_leg(False)
					
					#self.track_list[self.num_lines].set_connection_track_a(self.track_list[0])
					#self.track_list[self.num_lines].set_connection_track_b(self.track_list[0])
					
					#load infrastructure
					self.track_list[self.num_lines].set_infrastructure(row[6])
					
					#print(self.track_list[self.num_lines].get_block())
					self.num_lines+=1
					
					
		#close the opened file
		csv_file.close()			
			
	def get_track_info(self):
		#get the text inputted by the user and check to see if it's a number
		try :
			inputTrackBlock=int(self.ui.trackSelector.text())
		except:
			print("Inputted Track Block Not a Number")
			self.ui.trackSelectorValid.setText("Invalid Input\nNot a Number")
			return 
		
		print("numlines:", self.num_lines)
		print("inputblock:", inputTrackBlock)
		
		if(inputTrackBlock > self.num_lines):
			print("Input Track Block too High")
			self.ui.trackSelectorValid.setText("Invalid Input\nBlock Number Too High")

		
		#otherwise it is a valid input and update everything
		self.ui.trackSelectorValid.setText("Valid Input")
		self.current_block=inputTrackBlock
		self.update_track_info(inputTrackBlock)
	
		# deafult update every output for block1
		#self.update_track_info(1)
	
	
	def cause_rail_fail(self):
		#toggle status
		temp = not self.track_list[self.current_block].get_rail_condition()
		
		if(temp == False):
			self.track_list[self.current_block].set_rail_condition(False)
			self.track_list[self.current_block].set_signal_light('Stop')
			self.update_track_info(self.current_block)
			print("CAUTION! RAIL FAILURE ON BLOCK ", self.current_block) 
		else:
			self.track_list[self.current_block].set_rail_condition(True)
			#make sure to send go if all track conditions are good
			if(self.track_list[self.current_block].get_circuit_condition() == True) and (self.track_list[self.current_block].get_power_condition() == True):
				self.track_list[self.current_block].set_signal_light('Go')
			self.update_track_info(self.current_block)
			print("RAIL Fixed on BLOCK ", self.current_block) 

	def cause_circuit_fail(self):
		#toggle status
		temp = not self.track_list[self.current_block].get_circuit_condition()
		
		if(temp == False):
			self.track_list[self.current_block].set_circuit_condition(False)
			self.track_list[self.current_block].set_signal_light('Stop')
			self.update_track_info(self.current_block)
			print("CAUTION! CIRCUIT FAILURE ON BLOCK ", self.current_block) 
		else:
			self.track_list[self.current_block].set_circuit_condition(True)
			#make sure to send go if all track conditions are good
			if(self.track_list[self.current_block].get_rail_condition() == True) and (self.track_list[self.current_block].get_power_condition() == True):
				self.track_list[self.current_block].set_signal_light('Go')
			self.update_track_info(self.current_block)
			print("CIRCUIT Fixed on BLOCK ", self.current_block) 

	def cause_power_fail(self):
		#toggle status
		temp = not self.track_list[self.current_block].get_power_condition()
		
		if(temp == False):
			self.track_list[self.current_block].set_power_condition(False)
			self.track_list[self.current_block].set_signal_light('Stop')
			self.update_track_info(self.current_block)
			print("CAUTION! POWER FAILURE ON BLOCK ", self.current_block) 
		else:
			self.track_list[self.current_block].set_power_condition(True)
			#make sure to send go if all track conditions are good
			if(self.track_list[self.current_block].get_rail_condition() == True) and (self.track_list[self.current_block].get_circuit_condition() == True):
				self.track_list[self.current_block].set_signal_light('Go')
			self.update_track_info(self.current_block)
			print("POWER Fixed on BLOCK ", self.current_block) 
			
	
	def toggle_heater(self):
		temp = not self.track_list[self.current_block].get_heater_status()
		self.track_list[self.current_block].set_heater_status(temp)		
		self.update_track_info(self.current_block)
	
	def set_track_temperature(self):
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
			self.track_list[self.current_block].set_heater_status(True)
		else:
			self.track_list[self.current_block].set_heater_status(False)
		
		self.track_list[self.current_block].set_ambient_temp(inputTemp)
		self.update_track_info(self.current_block)
	
	def swap_switch(self): #change this to be inside the swtich class
		if(self.track_list[self.current_block].get_is_switch() == True):
			temp = not self.track_list[self.current_block].switch_list[Track.switch_num].get_switch_position()
			self.track_list[self.current_block].switch_list[Track.switch_num].set_switch_position(temp)
			self.update_track_info(self.current_block)
	
	def update_track_info(self,blckNum):
		
		print("-----------------------------------------------------------------------------------")
		#update any connections
		#make track connections
		i=1
		
		#loop to update all connections in between the tracks
		while (i <= self.num_lines-1):
			#print(self.track_list[i].get_block())
			if self.track_list[i].get_is_switch()==False and  self.track_list[i].get_is_switch_leg()==False :						
				if i == 1:
					self.track_list[i].set_connection_track_a(None)
					self.track_list[i].set_connection_track_b(self.track_list[i+1])
				
				if i == self.num_lines or self.track_list[i].get_is_station()==True:
					self.track_list[i].set_connection_track_a(self.track_list[i-1])
					self.track_list[i].set_connection_track_b(None)
				else:
					self.track_list[i].set_connection_track_a(self.track_list[i-1])
					self.track_list[i].set_connection_track_b(self.track_list[i+1])
								
			else:
				#print('d')
				if self.track_list[i].switch_list[Track.switch_num].get_switch_position() == False:
					#print('h')
					self.track_list[i].set_connection_track_a(self.track_list[Track.switch_list[1].get_y_stem()])
					self.track_list[i].set_connection_track_b(self.track_list[Track.switch_list[1].get_y_zero()])
					self.track_list[Track.switch_list[1].get_y_one()].set_connection_track_a(None)
				
				if self.track_list[i].switch_list[Track.switch_num].get_switch_position() == True:
					self.track_list[i].set_connection_track_a(self.track_list[Track.switch_list[1].get_y_stem()])
					self.track_list[i].set_connection_track_b(self.track_list[Track.switch_list[1].get_y_one()])
					self.track_list[Track.switch_list[1].get_y_zero()].set_connection_track_a(None)				
				
				
			
			print(self.track_list[i].get_block()," Con A = ", self.track_list[i].get_connection_track_a(), "Con B = ",self.track_list[i].get_connection_track_b())
			
			i+=1
		
		#update every label with relevant information
		self.ui.selTrackSection.setText(str(self.track_list[blckNum].get_line()))
		
		
		self.ui.selTrackSpeed.display(self.track_list[blckNum].get_speed_limit())
		
		self.ui.selTrackGrade.setText(str(self.track_list[blckNum].get_grade()))
		self.ui.selTrackHeater.setText(str(self.track_list[blckNum].get_heater_status()))
		
		if(self.track_list[blckNum].get_is_station() == True):
			self.ui.selTrackStation.setText(self.track_list[blckNum].get_station_name())	
			#CTC outputs
			self.ui.ctcTicketO.display(self.track_list[blckNum].get_ticket_count())
			self.ui.ctcTrackUpO.setText("Tickets Updated")
			self.ui.train_people_boarding.display(self.track_list[blckNum].get_boarding_count())
		else:
			self.ui.selTrackStation.setText('Not a Station')
			self.ui.ctcTicketO.display(0)
			self.ui.train_people_boarding.display(0)
			self.ui.ctcTrackUpO.setText("Not a Station")
			
		if(self.track_list[blckNum].get_is_crossing() == True):
			self.ui.selTrackCross.setText('Yes')
		else:
			self.ui.selTrackCross.setText('No')
		
		if(self.track_list[blckNum].get_is_crossing() == True):
			self.ui.selTrackBranch.setText('Yes')
		else:
			self.ui.selTrackBranch.setText('No')	

		if(self.track_list[blckNum].get_is_switch() == True):
			self.ui.selTrackSW.setText('Yes')
			self.ui.waySwitch.setText(str(self.track_list[blckNum].get_connection_track_b().get_block()))
			#SET CONNECTIONS BOYOY
		else:
			self.ui.selTrackSW.setText('No')	
			self.ui.waySwitch.setText('Not a switch')
		
		
		#for occupied blocks
		
		
		
		#railStatus
		self.ui.selTrackRailStat.setText(str(self.track_list[blckNum].get_rail_condition()))
		self.ui.selTrackCircStat.setText(str(self.track_list[blckNum].get_circuit_condition()))
		self.ui.selTrackPowerStat.setText(str(self.track_list[blckNum].get_power_condition()))
		
	
		
		#railSignal
		if(self.track_list[blckNum].get_signal_light() == 'Go'):
			self.ui.sigGo.setChecked(True)
			self.ui.sigSlow.setChecked(False)
			self.ui.sigStop.setChecked(False)
		elif(self.track_list[blckNum].get_signal_light() == 'Slow'):
			self.ui.sigGo.setChecked(False)
			self.ui.sigSlow.setChecked(True)
			self.ui.sigStop.setChecked(False)
		elif(self.track_list[blckNum].get_signal_light() == 'Stop'):
			self.ui.sigGo.setChecked(False)
			self.ui.sigSlow.setChecked(False)
			self.ui.sigStop.setChecked(True)
		
		#temperature
		self.ui.ambTemp.display(self.track_list[blckNum].get_ambient_temp())
		
		#wayside input
		self.ui.wayCommandedSpeed.display(self.track_list[blckNum].get_commanded_speed())
		self.ui.wayAuthority.display(self.track_list[blckNum].get_authority())
		self.ui.waySignal.setText(self.track_list[blckNum].get_signal_light())
		
		#train outputs
		self.ui.trainSpeedLimitO.display(self.track_list[blckNum].get_speed_limit())
		self.ui.trainAuthorityO.display(self.track_list[blckNum].get_authority())
		self.ui.trainBeaconO.setText(self.track_list[blckNum].get_beacon())
	
		
		#Wayside outputs
		self.ui.wayOccupiedO.setText(str(self.track_list[blckNum].get_occupied()))
		
		
if __name__ == "__main__":
	app = QApplication(sys.argv)

	window = MainWindow()

	#put code here
	
	window.show()
		
	sys.exit(app.exec_())
	
	
	
	
	
	
	