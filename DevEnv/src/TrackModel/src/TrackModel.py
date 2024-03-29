import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import QFile
from TrackModel.src.UI import Ui_Dialog
#from UI import Ui_Dialog
from signals import signals


#extra imported items
import csv
import ast
import random

#Code to generate Green route

'''
#Train always begins at yard
self.route_queue_green.append(0)

#Specify blocks for track sections K through Q
for block_num in range(63, 101):
	self.route_queue_green.append(block_num)

#Specify blocks for track section N in reverse
for block_num in range(85, 76, -1):
	self.route_queue_green.append(block_num)

#Specify blocks for track secionts R through Z
for block_num in range(101, 151):
	self.route_queue_green.append(block_num)

#Specify blocks for track sections A through F in reverse
for block_num in range(28, 0, -1):
	self.route_queue_green.append(block_num)

#Specify blocks for track sections D through I
for block_num in range(13, 58):
	self.route_queue_green.append(block_num)

#Train ends at yard by defaulti
self.route_queue_green.append(0)
'''

#Code to generate Red route

'''
#Train always begins at yard
self.route_queue_green.append(0)

#Specify blocks for track sections A, B, C in reverse
for block_num in range(9, 0, -1):
	self.route_queue_green.append(block_num)

#Specify blocks for track sections F through N
for block_num in range(16, 67):
	self.route_queue_green.append(block_num)

#Specify blocks for part of H, I, and part of J in reverse
for block_num in range(52, 42, -1):
	self.route_queue_green.append(block_num)

#Specify blocks for track sections O through Q
for block_num in range(67, 72):
	self.route_queue_green.append(block_num)

#Specify blocks for part of H in reverse
for block_num in range(38, 31, -1):
	self.route_queue_green.append(block_num)

#Specify blocks for track sections R through T
for block_num in range(72, 77):
	self.route_queue_green.append(block_num)

#Specify blocks for F, G, and part of H in reverse
for block_num in range(27, 15, -1):
	self.route_queue_green.append(block_num)

#Specify blocks for track sections D and E in reverse
for block_num in range(15, 9, -1):
	self.route_queue_green.append(block_num)

#Train ends always ends at yard
self.route_queue_green.append(0)
'''

#i currently need to change the function to that of which will match the coding standards

#switch class
class Switch:
	def __init__(self):	
		self.current_switch_pos= 0
		self.y_stem = 0
		self.y_zero = 0
		self.y_one = 0
	
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
	
	def __init__(self):

		self.stationArray = ("SHADYSIDE","HERRONAVE","SWISSVILLE","PENNSTATION","STEELPLAZA","FIRSTAVE","STATIONSQUARE","SOUTHILLSJUNCTION", 
                            "PIONEER","EDGEBROOK","WHITED","SOUTHBANK","CENTRAL","INGLEWOOD","OVERBROOK","GLENBURY","DORMONT","MTLEBANON", "POPLAR","CASTLESHANNON")
		#print("got here 1")
		self.line = 0
		self.section = 0
		self.block = 0
		self.length = 0
		self.grade = 0
		self.infrastructure=0
		self.elevation=0
		self.elevation_c=0
		self.station_side=0
		self.speed_limit = 0
		self.commanded_speed = 0 #float w 2 decimal points
		self.beacon = 0
		self.signal_light = 0
		self.occupied = False
		self.heater_status= 0
		self.connection_track_a = 0
		self.connection_track_b = 0
		self.direction = ''
		self.rail_condition = 0
		self.circuit_condition = 0
		self.power_condition = 0 #power_condition
		self.condition_list=[True,True,True]
		self.condition_int = 0 
		self.ambient_temp = 0 #ambient_temp
		self.authority = 0  #authority
		self.is_underground = 0
		
		#station variables
		self.ticket_count = 0 #ticket_count
		self.is_station = 0 #is_station
		self.station_name = 0 #station_name
		self.station_side = 0 #station_side
        
		self.boarding_count = 0 #boarding_count
		
		#crossing Variables
		self.is_crossing = 0
		self.crossing_status = 0
		self.crossing_light = 0

		#branch variable
		self.is_branch = 0
		
		#swithc variable
		self.is_switch = 0 #is_switch
		self.is_switch_leg = 0 #is_switch_leg
		self.switch_index = 0 #which switch in the list it corresponds to


		#variables for send train model signal
		self.encoded_TC = 0 #encoded_TC
		self.cmd_Int = 0 #cmd_Int
		self.cmd_Float = 0 #cmd_Float
		self.auth_Int = 0 #a0 uth_Int
		self.auth_Float = 0
		#print("got here 1")

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
	
	def get_direction(self):
		return self.direction
	def set_direction(self, in_direction):
		self.direction = in_direction

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

	
	def set_occupied(self, in_occupied, id = 0):
		#every time a train leaves a block with a  station on it, it regenerates the tickets
		if(self.get_occupied()==True):
			if(self.get_is_station() == True):	#maybe add in if "&& in_occupied == False"
				self.generate_random_ticket()
		self.occupied=in_occupied
		
		if(self.get_authority() == 1):
			signals.track_model_occupancy.emit(self.line, self.block, self.occupied)
	
		#if the block is becomming occupied, send signal to train model
		if(in_occupied == True and self.rail_condition == True):
			self.encode_track_circuit_signal()
			print("sned tc at 275, id is" + str(id) )
			
			signals.TC_signal.emit(self.encoded_TC, id)
			#send beacon
			#if(self.block == 4):
			#sned block 
			#print("Sending Block Len of:" + str(self.length))
			#print("type of length is " + str(type(self.length)))
			signals.new_block.emit(self.block, int(self.length), self.grade, id)

	def encode_beacon(self):
		   #encoding my beacon
		self.encodedBeacon = int(self.is_station) 
		#self.encodedBeacon = int(self.ui.stationUpcoming.checkState()) >> 1
		print(bin(self.encodedBeacon))
		print(self.station_side)
		if(self.is_station):
			self.encodedBeacon += self.station_side << 1
		#self.encodedBeacon += (int(self.ui.leftDoorsFake.checkState()) >> 1) << 1
		#self.encodedBeacon += (int(self.ui.rightDoorsFake.checkState()) >> 1) << 2
		
		#if the time is between 7pm and 7am the lights should be on or if the track is underground
		
		#self.encodedBeacon += int(self.is_underground())
		
		self.encodedBeacon += (int(self.is_underground)) << 3
		
		#self.encodeBeacon+=self.station_name
		if(self.is_station):
			print(self.station_name)
			self.encodedBeacon += (self.stationArray.index(self.station_name) & 31) << 4

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
		if(self.rail_condition == False):
			signals.track_break.emit(self.line, self.block, 0)

	def get_circuit_condition(self):
		return self.circuit_condition
	def set_circuit_condition(self, in_condition):
		self.circuit_condition=in_condition
		if(self.circuit_condition == False):
			signals.track_break.emit(self.line, self.block, 1)

	def get_power_condition(self):
		return self.power_condition
	def set_power_condition(self, in_condition):
		self.power_condition= in_condition
		if(self.power_condition == False):
			signals.track_break.emit(self.line, self.block, 2)

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
		if(self.get_is_station()==True):
			print("in ticket if")
			signals.station_ticket_sales.emit(self.line, self.ticket_count)
			#print("emitting ticket sales for " + self.station_name)

	def get_is_underground(self):
		return self.is_underground
	def set_is_underground(self, in_condition):
		self.is_underground = in_condition

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

	def get_crossing_status(self):
		return self.crossing_status
	def set_crossing_status(self, in_condition):
		self.crossing_status = in_condition

	def get_crossing_light(self):
		return self.crossing_light
	def set_crossing_light(self, in_condition):
		self.crossing_light = in_condition

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

	def get_switch_index(self):
		return self.switch_index
	def set_switch_index(self, in_condition):
		self.switch_index = in_condition

	def get_boarding_count(self):
		return self.boarding_count
	def set_boarding_count(self, in_condition):
		#print("YA WE ENTERED SET BOARDING COUNT")
		self.boarding_count=in_condition
	
	#function parse the infrastructure input
	def infra_parse(self):
		print(self.infrastructure)
		#if there is no infrastructure, exit the function
		if self.infrastructure == '':
			self.set_is_station(False)
			self.set_is_switch(False)
			self.set_is_branch(False)
			
			return None
	
		#this list contains atributes of infrastructure such a station/undergorund
		list_atrib=self.infrastructure.split(';')
		
		#create flag variables
		station_done = False
		underground_done = False
		switch_done = False
		#print(str(len(list_atrib))+" list_atrib length")
		#if there is only one atribute
		for i in range(0, len(list_atrib)):
			#split up atribute by the spacing
			atrib=list_atrib[i].split(' ')	
			#print(str(len(atrib)) + " atrib length")
			#print(atrib)
			for j in range(0,len(atrib)):	
				
				if(atrib[j] == 'RAILWAY'):
					self.set_is_crossing(True)
					self.set_signal_light('Slow')
				
				
				
				#check to see if atribute is a station:
				if(atrib[j] == 'STATION'):
					self.set_is_station(True)
					#self.set_station_name(atrib[j]+' '+atrib[j+1])
					self.set_station_name(atrib[j+1])

					sample_string = self.get_station_name()
					#print(sample_string)
					self.set_beacon('Welcome to ' + sample_string)
					self.generate_random_ticket() 
					if(self.station_side == 'Left'):
						self.set_station_side(1)
					if(self.station_side == 'Right'):
						self.set_station_side(2)
					if(self.station_side == 'Left/Right'):
						self.set_station_side(3)
					
					#set the flag
					station_done = True
					#print(atrib)
				
					#print(self.get_beacon())
					#print("Station is" ,self.get_station_name())
				elif station_done == False:
					self.set_is_station(False)
				
				#check to see if it is underground
				if(atrib[j] == 'UNDERGROUND'):
					self.set_is_underground(True)
					underground_done = True
				elif underground_done == False:
					self.set_is_underground(False)
				
				#check to see if atribute is a swtich
				if(atrib[j] == 'SWITCH'):	
					#check to see if it is the stem of the swtich
					if (len(atrib) > 5):
						self.set_is_switch(True)
						#print("stem is ", self.get_block())
						Track.switch_list.append(Switch())
						self.set_switch_index(Track.switch_num)
						
						Track.switch_list[Track.switch_num].set_y_stem(self.get_block())
						y_zero_in = int(atrib[3])
						if(atrib[8] == 'YARD'):
							y_one_in = 0
						else:
							y_one_in = int(atrib[8])
						#print("Block "+ str(self.block) + ": y_zero_in) is " + str(y_zero_in) + " and y_one_in is " + str(y_one_in))
						
						Track.switch_list[Track.switch_num].set_switch_position(False)
						Track.switch_list[Track.switch_num].set_y_zero(y_zero_in)
						Track.switch_list[Track.switch_num].set_y_one(y_one_in)
						#print("zero is ", Track.switch_list[Track.switch_num].set_y_zero(), " and one is ", Track.switch_list[Track.switch_num].set_y_one(), "and switch position is", Track.switch_list[Track.switch_num].get_switch_position())
						self.set_is_switch_leg(False)
						Track.switch_num+=1
						#print(Track.switch_num)
					else: 
						self.set_is_switch(False)
						self.set_is_switch_leg(True)
					#set the flag
					switch_done = True
						
				elif switch_done == False:
					self.set_is_switch(False)
					self.set_is_switch_leg(False)
				
	#function to generate a random amount of tickets
	def generate_random_ticket(self):
		self.set_ticket_count(random.randint(1,40))
		self.generate_boarding()
		
	#function to generate the amount of people boarding
	def generate_boarding(self):
		#print("YA WE ENTERED GENERATE BOARDING")
		self.set_boarding_count(random.randint(1, self.get_ticket_count()))
		
	def encode_track_circuit_signal(self):
		#function to encode a track signal 
		cmd_Int= int(float(self.get_commanded_speed()))
		cmd_Float= int(((float(self.get_commanded_speed())-cmd_Int)*10))
		auth_Int= int(float(self.get_authority()))
		auth_Float= int(((float(self.get_authority())-auth_Int)*10))

		if(self.get_circuit_condition()==False):
			self.encoded_TC = (cmd_Int-6 & 255)
		else:
			self.encoded_TC = (cmd_Int & 255)
			self.encoded_TC += (cmd_Float & 15) << 8
			self.encoded_TC += (auth_Int & 255) << 12
			self.encoded_TC += (auth_Float & 15)<< 20
			self.encoded_TC += ((cmd_Int + cmd_Float + auth_Float + auth_Int) & 1023) << 24	
		#sned the signal 
		#prem can you rerun the code pls
	
	
#-----------------------------------------------------------------------------------------------------------------------#

#Code for the UI
class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		
		#instance variables
		self.track_list = [Track()]
		self.track_list_green = [Track()]
		self.track_list_red = [Track()]
		self.switch_increment = 0
		self.num_lines = 0
		self.current_block_green = 0
		self.current_block_red = 0
		self.route_queue_green = []
		self.route_queue_red = []
		self.id_list = [0]
		
		
		#if load track button is pressed
		self.ui.getTrackFileBTN.clicked.connect(self.load_track)
		
		#if get track is pressed then update all relvant information
		self.ui.getTrackBTN.clicked.connect(self.get_track_info_green)
		self.ui.getTrackBTN_red.clicked.connect(self.get_track_info_red)
		
		
		#same but for red line
		#self.ui.getTrackBTN_red.clicked.connect(self.)

		#if toggle heater is pressed 
		self.ui.heaterToggleBTN.clicked.connect(self.toggle_heater_green)
		self.ui.heaterToggleBTN_red.clicked.connect(self.toggle_heater_red)
		
		#if button pressed then update the temperature
		self.ui.setTempBTN.clicked.connect(self.set_track_temperature_green)
		self.ui.setTempBTN_red.clicked.connect(self.set_track_temperature_red)
		
		
		#if buttons pressed cause a failure respective to the button
		self.ui.breakRailBTN.clicked.connect(self.cause_rail_fail_green)
		self.ui.breakRailBTN_red.clicked.connect(self.cause_rail_fail_red)

		self.ui.breakCircuitBTN.clicked.connect(self.cause_circuit_fail_green)
		self.ui.breakCircuitBTN_red.clicked.connect(self.cause_circuit_fail_red)
		
		self.ui.breakPowerBTN.clicked.connect(self.cause_power_fail_green)
		self.ui.breakPowerBTN_red.clicked.connect(self.cause_power_fail_red)

		#if button pressed swap switch

		#self.ui.waySwitchBTN.clicked.connect(self.swap_switch)

	#function to load track from a file
	def load_track(self):

		#reset the table
		
		while (self.ui.green_line_table.rowCount() > 0):
			#print("removing rows")
			self.ui.green_line_table.removeRow(0)
		self.ui.green_line_table.reset()
		self.ui.red_line_table.reset()

		#self.ui.green_line_table.setRowCount(0)
		#self.ui.green_line_table.setColumnCount(0)

		#reset the lists
		#set corresponding track
		if self.ui.upTrackGreen.isChecked() == True:
			self.track_list_green.clear()
		else:	
			self.track_list_red.clear()
		self.track_list.clear()
		
		#if self.upTrackBlue.getChecked()==true
		inputFileName=self.ui.lineEdit.text()
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
				#first block is track_lisst[1]
				if self.num_lines ==0:
					#print("adding first track obj")
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
					#print("making block num " + str(self.track_list[self.num_lines].get_block()))
					self.track_list[self.num_lines].set_length(int(row[3]))
					self.track_list[self.num_lines].set_grade(float(row[4]))
					self.track_list[self.num_lines].set_speed_limit(int(row[5]))
					
					self.track_list[self.num_lines].set_station_side(row[7])
					self.track_list[self.num_lines].set_elevation(float(row[8]))
					self.track_list[self.num_lines].set_elevation_c(float(row[9]))
					#print( str(self.track_list[self.num_lines].get_block()) + " track  is "+ str(row[8]))
					self.track_list[self.num_lines].set_direction(row[11])
					
					
					#add base default values for each object 
					self.track_list[self.num_lines].set_heater_status(False)
					self.track_list[self.num_lines].set_rail_condition(True)
					self.track_list[self.num_lines].set_circuit_condition(True)
					self.track_list[self.num_lines].set_power_condition(True)
					self.track_list[self.num_lines].set_ambient_temp(70)
					
					#temporary simulated signals from wayside
					self.track_list[self.num_lines].set_commanded_speed(0)
					self.track_list[self.num_lines].set_authority(1)
					self.track_list[self.num_lines].set_signal_light('Go')
					self.track_list[self.num_lines].set_beacon(' ')
					self.track_list[self.num_lines].set_is_crossing(False)
					self.track_list[self.num_lines].set_is_branch(False)
					self.track_list[self.num_lines].set_is_switch_leg(False)
					self.track_list[self.num_lines].set_occupied(False)
					
					#self.track_list[self.num_lines].set_connection_track_a(self.track_list[0])
					#self.track_list[self.num_lines].set_connection_track_b(self.track_list[0])
					self.track_list[self.num_lines].set_is_station(False)
					self.track_list[self.num_lines].set_ticket_count(0)
					
					#load infrastructure
					self.track_list[self.num_lines].set_infrastructure(row[6])
					
					#print(self.track_list[self.num_lines].get_block())
					self.num_lines+=1

		#close the opened file
		csv_file.close()
		self.track_list.append(Track())
		
		
		#make sure that all the switch legs have a corresponding switch_index
		for self.switch_increment in range(len(Track.switch_list)):
			#print(Track.switch_list[i].get_y_zero())
			if self.track_list[Track.switch_list[self.switch_increment].get_y_zero()].get_switch_index() == 0:
				#print("setting index " + str(i))
				self.track_list[Track.switch_list[self.switch_increment].get_y_zero()].set_switch_index(self.switch_increment)
			if self.track_list[Track.switch_list[self.switch_increment].get_y_one()].get_switch_index() == 0:
				#print("setting index " + str(i))
				self.track_list[Track.switch_list[self.switch_increment].get_y_one()].set_switch_index(self.switch_increment)
		
		#set corresponding track
		if self.ui.upTrackGreen.isChecked() == True:
			self.track_list_green = self.track_list
			self.switch_increment+=6
		else:	
			self.track_list_red = self.track_list
			self.switch_increment+=7
		
		print("parsing completed")
		signals.need_new_block.connect(self.send_block_to_model)
		signals.wayside_to_track.connect(self.get_wayside_info)
		signals.train_creation.connect(self.set_occupied_initial)
		signals.wayside_block_open.connect(self.get_open_block)
		signals.track_switch_position.connect(self.swap_switch)
		signals.wayside_signal_light.connect(self.get_wayside_signals)
		signals.crossing_gate_activation.connect(self.get_wayside_crossing_barrier)
		signals.crossing_light_activation.connect(self.get_wayside_crossing_light)

		#if green line 
		#Code to generate Green route		
		#Train always begins at yard
		self.route_queue_green.append(0)

		#Specify blocks for track sections K through Q
		for block_num in range(63, 101):
			self.route_queue_green.append(block_num)

		#Specify blocks for track section N in reverse
		for block_num in range(85, 76, -1):
			self.route_queue_green.append(block_num)

		#Specify blocks for track secionts R through Z
		for block_num in range(101, 151):
			self.route_queue_green.append(block_num)

		#Specify blocks for track sections A through F in reverse
		for block_num in range(28, 0, -1):
			self.route_queue_green.append(block_num)

		#Specify blocks for track sections D through I
		for block_num in range(13, 58):
			self.route_queue_green.append(block_num)

		#Train ends at yard by default
		self.route_queue_green.append(0)
		#----red---
		#Code to generate Red route
		#Train always begins at yard
		self.route_queue_red.append(0)

		#Specify blocks for track sections A, B, C in reverse
		for block_num in range(9, 0, -1):
			self.route_queue_red.append(block_num)

		#Specify blocks for track sections F through N
		for block_num in range(16, 67):
			self.route_queue_red.append(block_num)

		#Specify blocks for part of H, I, and part of J in reverse
		for block_num in range(52, 42, -1):
			self.route_queue_red.append(block_num)

		#Specify blocks for track sections O through Q
		for block_num in range(67, 72):
			self.route_queue_red.append(block_num)

		#Specify blocks for part of H in reverse
		for block_num in range(38, 31, -1):
			self.route_queue_red.append(block_num)

		#Specify blocks for track sections R through T
		for block_num in range(72, 77):
			self.route_queue_red.append(block_num)

		#Specify blocks for F, G, and part of H in reverse
		for block_num in range(27, 15, -1):
			self.route_queue_red.append(block_num)

		#Specify blocks for track sections D and E in reverse
		for block_num in range(15, 9, -1):
			self.route_queue_red.append(block_num)

		#Train ends always ends at yard
		self.route_queue_red.append(0)

		#initialize the table
		self.ui.green_line_table.setColumnCount(2)
		self.ui.green_line_table.setRowCount(len(self.track_list_green))
		
		self.ui.red_line_table.setColumnCount(2)
		self.ui.red_line_table.setRowCount(len(self.track_list_red))
				
		#default load block 63 on the geen line and 9 on the red line
		if self.ui.upTrackGreen.isChecked() == True:
			self.update_track_info_green(63)
		else:	
			self.update_track_info_red(9)
		
		
	#function to tell me where the train is
	def send_block_to_model(self,line_in, block, id):   #NEED LINE ARGUMENT
		#print("sent block123")
		if(line_in == "Green"):
			#print("block length: " + str(self.track_list_green[block+1].get_length()))
			self.track_list_green[block].set_occupied(False)
			#self.route_queue_green.pop(0)
			self.id_list[id]+=1

			#print("just left block " + str(block) + " next is " + str(self.route_queue_green[self.id_list[id]]))
			self.track_list_green[self.route_queue_green[self.id_list[id]]].set_occupied(True, id)

			#send the beacon if there is a station or tunnel ahead 
			if(self.track_list_green[self.route_queue_green[self.id_list[id]+1]].is_station == True or self.track_list_green[self.route_queue_green[self.id_list[id]+1]].is_underground == True):
				
				self.track_list_green[self.route_queue_green[self.id_list[id]+1]].encode_beacon()
				signals.Beacon_signal.emit(self.track_list_green[self.route_queue_green[self.id_list[id]+1]].encodedBeacon, id) # ACTUALLY CALCULATE THE BEACON VAL AND BLOCK NUM
			
			self.update_track_info_green(self.current_block_green)
		else:
			#print("block length: " + str(self.track_list_red[block+1].get_length()))
			self.track_list_red[block].set_occupied(False)
			#self.route_queue_green.pop(0)
			self.id_list[id]+=1

			#print("just left block " + str(block) + " next is " + str(self.route_queue_red[self.id_list[id]]))
			self.track_list_red[self.route_queue_red[self.id_list[id]]].set_occupied(True, id)

			#send the beacon if there is a station or tunnel ahead 
			if(self.track_list_red[self.route_queue_red[self.id_list[id]+1]].is_station == True or self.track_list_red[self.route_queue_red[self.id_list[id]+1]].is_underground == True):
				
				self.track_list_red[self.route_queue_red[self.id_list[id]+1]].encode_beacon()
				signals.Beacon_signal.emit(self.track_list_red[self.route_queue_red[self.id_list[id]+1]].encodedBeacon, id) # ACTUALLY CALCULATE THE BEACON VAL AND BLOCK NUM
			
			self.update_track_info_red(self.current_block_red)
	

	#function for inital train spawn
	def set_occupied_initial(self, track_line, id):
		if (track_line == "Green"):
			#self.route_queue_green.pop(0)
			self.id_list.append(1)
			self.track_list_green[63].set_occupied(True, id)
			self.update_track_info_green(self.current_block_green)

		else:
			self.track_list_red[9].set_occupied(True, id)
			self.update_track_info_red(self.current_block_red)

		
	#function to update from wayside commanded speed and authroity
	def get_wayside_info(self, line_in, block_in, authority_in, commanded_speed_in): 
		
		
		self.track_list_green[block_in].set_authority(authority_in)
		self.track_list_green[block_in].set_commanded_speed(commanded_speed_in*(5.0/18.0))
		#self.track_list[block_in].set_occupied(1)
		if line_in == "Green":
			for i in range(0, len(self.id_list)):
				#print("id_list[i] = " + str(self.route_queue_green[self.id_list[i]]))
				#print("block_in = " + str(block_in))
				if(self.route_queue_green[self.id_list[i]] == block_in):
					self.track_list_green[block_in].encode_track_circuit_signal()
					#print("tc emit at 856")
					signals.TC_signal.emit(self.track_list_green[block_in].encoded_TC, i)
			self.update_track_info_green(self.current_block_green)
		else:
			for i in range(0, len(self.id_list)):
				print("id_list[i] = " + str(self.route_queue_red[self.id_list[i]]))
				print("block_in = " + str(block_in))
				if(self.route_queue_red[self.id_list[i]] == block_in):
					self.track_list_red[block_in].encode_track_circuit_signal()
					print("tc emit at 856")
					signals.TC_signal.emit(self.track_list_red[block_in].encoded_TC, i)
			self.update_track_info_red(self.current_block_red)
		
		print("Sending occupancy to wayside")

	#signal for getting the track lights from the wayside
	def get_wayside_signals(self, line_in, block_in, signal_in):
		if(signal_in == 0):
			temp = 'Go'
		elif(signal_in == 1):
			temp = 'Slow'
		else: 
			temp = 'Stop'

		if(line_in == "Green"):
			if(len(self.track_list_green)!= 1):
				self.track_list_green[block_in].set_signal_light(temp)
				self.update_track_info_green(self.current_block_green)
		else:
			#print('_________________________________' + str(len(self.track_list_red)))
			if(len(self.track_list_red)!= 1):
				self.track_list_red[block_in].set_signal_light(temp)
				self.update_track_info_red(self.current_block_red)

	def get_wayside_crossing_barrier(self, line_in, block_in, status_in):		
		if(line_in == "Green"):
			if(len(self.track_list_green)!= 1):	
				self.track_list_green[block_in].set_crossing_status(status_in)
				self.update_track_info_green(self.current_block_green)
		else:
			if(len(self.track_list_red)!= 1):
				self.track_list_red[block_in].set_crossing_status(status_in)
				self.update_track_info_red(self.current_block_red)

		
	def get_wayside_crossing_light(self, line_in, block_in, status_in):
		if(line_in == "Green"):
			if(len(self.track_list_green)!= 1):
				self.track_list_green[block_in].set_crossing_light(status_in)
				self.update_track_info_green(self.current_block_green)
		else:
			if(len(self.track_list_red)!= 1):
				self.track_list_red[block_in].set_crossing_light(status_in)
				self.update_track_info_red(self.current_block_red)


	#signal from the ctc that reopens a block
	def get_open_block(self, line_in, in_block): 
		if(line_in == "Green"):
			self.track_list_green[in_block].set_rail_condition(True)
			self.track_list_green[in_block].set_circuit_condition(True)
			self.track_list_green[in_block].set_power_condition(True)
			self.update_track_info_green(self.current_block_green)
		else:
			self.track_list_red[in_block].set_rail_condition(True)
			self.track_list_red[in_block].set_circuit_condition(True)
			self.track_list_red[in_block].set_power_condition(True)
			self.update_track_info_red(self.current_block_red)

	def get_track_info_green(self):
		#get the text inputted by the user and check to see if it's a number
		try :
			inputTrackBlock=int(self.ui.trackSelector.text())
		except:
			print("Inputted Track Block Not a Number")
			self.ui.trackSelectorValid.setText("Invalid Input\nNot a Number")
		
		#print("numlines:", self.num_lines)
		#print("inputblock:", inputTrackBlock)
		
		if(inputTrackBlock > len(self.track_list_green)):
			print("Input Track Block too High")
			self.ui.trackSelectorValid.setText("Invalid Input\nBlock Number Too High")
			return

		
		#otherwise it is a valid input and update everything
		self.ui.trackSelectorValid.setText("Valid Input")
		self.current_block_green=inputTrackBlock
		self.update_track_info_green(inputTrackBlock)
	
	#
	def cause_rail_fail_green(self):
		#toggle status
		temp = not self.track_list_green[self.current_block_green].get_rail_condition()
		
		if(temp == False):
			self.track_list_green[self.current_block_green].set_rail_condition(False)
			self.track_list_green[self.current_block_green].set_signal_light('Stop')
			self.track_list_green[self.current_block_green].set_occupied(True)
			self.update_track_info_green(self.current_block_green)
			print("CAUTION! RAIL FAILURE ON BLOCK ", self.current_block_green) 
		else:
			self.track_list_green[self.current_block_green].set_rail_condition(True)
			#make sure to send go if all track conditions are good
			if(self.track_list_green[self.current_block_green].get_circuit_condition() == True) and (self.track_list_green[self.current_block_green].get_power_condition() == True):
				self.track_list_green[self.current_block_green].set_signal_light('Go')
			self.track_list_green[self.current_block_green].set_occupied(False)
			self.update_track_info_green(self.current_block_green)
			print("RAIL Fixed on BLOCK ", self.current_block_green) 
	
	#function to cuase a circuit failure
	def cause_circuit_fail_green(self):
		#toggle status
		temp = not self.track_list_green[self.current_block_green].get_circuit_condition()
		
		if(temp == False):
			self.track_list_green[self.current_block_green].set_circuit_condition(False)
			self.track_list_green[self.current_block_green].set_signal_light('Stop')
			print("CAUTION! CIRCUIT FAILURE ON BLOCK ", self.current_block_green) 
			self.update_track_info_green(self.current_block_green)
		else:
			self.track_list_green[self.current_block_green].set_circuit_condition(True)
			#make sure to send go if all track conditions are good
			if(self.track_list_green[self.current_block_green].get_rail_condition() == True) and (self.track_list_green[self.current_block_green].get_power_condition() == True):
				self.track_list_green[self.current_block_green].set_signal_light('Go')
			print("CIRCUIT Fixed on BLOCK ", self.current_block_green) 
			self.update_track_info_green(self.current_block_green)

	def cause_power_fail_green(self):
		#toggle status
		temp = not self.track_list_green[self.current_block_green].get_power_condition()
		
		if(temp == False):
			self.track_list_green[self.current_block_green].set_power_condition(False)
			self.track_list_green[self.current_block_green].set_signal_light('Stop')
			self.update_track_info_green(self.current_block_green)
			print("CAUTION! POWER FAILURE ON BLOCK ", self.current_block_green) 
		else:
			self.track_list_green[self.current_block_green].set_power_condition(True)
			#make sure to send go if all track conditions are good
			if(self.track_list_green[self.current_block_green].get_rail_condition() == True) and (self.track_list_green[self.current_block_green].get_circuit_condition() == True):
				self.track_list_green[self.current_block_green].set_signal_light('Go')
			self.update_track_info_green(self.current_block_green)
			print("POWER Fixed on BLOCK ", self.current_block_green) 
			
	#function to toggle the track heater 
	def toggle_heater_green(self):
		temp = not self.track_list_green[self.current_block_green].get_heater_status()
		for i in range(1, len(self.track_list_green)):	
			self.track_list_green[i].set_heater_status(temp)		
		self.update_track_info_green(self.current_block_green)
	
	def set_track_temperature_green(self):
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
			for i in range(1, len(self.track_list_green)):	
				self.track_list_green[i].set_heater_status(True)
		else:
			for i in range(1, len(self.track_list_green)):	
				self.track_list_green[i].set_heater_status(False)
		
		for i in range(1, len(self.track_list_green)):	
			self.track_list_green[i].set_ambient_temp(inputTemp)
		self.update_track_info_green(self.current_block_green)
		#since temp will be the same for both lines
		#self.set_track_temperature_red()
		
	
	def swap_switch(self, line_in, stem_in, branch_in): 
		print("swapping switch")
		
		if line_in == "Green":
			if(len(self.track_list_green)!= 1):	
				self.track_list_green[stem_in].set_connection_track_b(self.track_list_green[branch_in])	
				#print("new switch position is " + str(self.track_list_green[stem_in].get_connection_track_b().get_block()))
				self.update_track_info_green(self.current_block_green)
		else:
			if(len(self.track_list_red)!= 1):
				self.track_list_red[stem_in].set_connection_track_b(self.track_list_green[branch_in])	
				#print("new switch position is " + str(self.track_list_red[stem_in].get_connection_track_b().get_block()))
				self.update_track_info_red(self.current_block_red)
		
	def update_track_info_green(self,blckNum):
		
		#update the table with current occupied blocks
		#print("track model updating green line")
		self.ui.green_line_table.setItem(0,0, QTableWidgetItem("Block Number"))
		self.ui.green_line_table.setItem(0,1, QTableWidgetItem("Status"))	
		
		for i in range(1, len(self.track_list_green)-1):
			#print("in for loop for table " + str(i) + "and is currently " + str(self. 
			if(self.track_list_green[i].get_occupied() == True):
				#print("occupied block is" + str(self.track_list_green[i]))
				self.ui.green_line_table.setItem(i,0, QTableWidgetItem(str(self.track_list_green[i].get_block())))
				self.ui.green_line_table.setItem(i,1, QTableWidgetItem("Occupied"))	
			else:
				self.ui.green_line_table.setItem(i,0, QTableWidgetItem(str(self.track_list_green[i].get_block())))
				self.ui.green_line_table.setItem(i,1, QTableWidgetItem("Unoccupied"))	
		#update any connections
		#make track connections
		
		i=1
		while (i <= self.num_lines-1):
			#print(self.track_list[i].get_block())
			if self.track_list_green[i].get_is_switch()==False and  self.track_list_green[i].get_is_switch_leg()==False :						
				#print("block " + str(i) + " is not a switch")
			
				self.track_list_green[i].set_connection_track_a(self.track_list_green[i-1])
				self.track_list_green[i].set_connection_track_b(self.track_list_green[i+1])
							
			elif(self.track_list_green[i].get_is_switch()==True):
				#print("block " + str(i) + " is a switch or switch leg")
				if self.track_list_green[i].switch_list[self.track_list_green[i].get_switch_index()].get_switch_position() == False:
					#print("switch index for block " + str(i)+" is " + str(self.track_list[i].get_switch_index()))
					
					if (self.track_list_green[i].switch_list[self.track_list_green[i].get_switch_index()].get_y_zero() < self.track_list_green[i].get_block()) or (self.track_list_green[i].switch_list[self.track_list_green[i].get_switch_index()].get_y_one() < self.track_list_green[i].get_block()):
						self.track_list_green[i].set_connection_track_b(self.track_list_green[i+1])
						self.track_list_green[i].set_connection_track_a(self.track_list_green[Track.switch_list[self.track_list_green[i].get_switch_index()].get_y_zero()])
					else:	
						self.track_list_green[i].set_connection_track_a(self.track_list_green[i-1])
						self.track_list_green[i].set_connection_track_b(self.track_list_green[Track.switch_list[self.track_list_green[i].get_switch_index()].get_y_zero()])
				
				
				if self.track_list_green[i].switch_list[self.track_list_green[i].get_switch_index()].get_switch_position() == True:

					if (self.track_list_green[i].switch_list[self.track_list_green[i].get_switch_index()].get_y_zero() < self.track_list_green[i].get_block()) or (self.track_list_green[i].switch_list[self.track_list_green[i].get_switch_index()].get_y_one() < self.track_list_green[i].get_block()):
						self.track_list_green[i].set_connection_track_b(self.track_list_green[i+1])
						self.track_list_green[i].set_connection_track_a(self.track_list_green[Track.switch_list[self.track_list_green[i].get_switch_index()].get_y_one()])
					else:	
						self.track_list_green[i].set_connection_track_a(self.track_list_green[i-1])
						self.track_list_green[i].set_connection_track_b(self.track_list_green[Track.switch_list[self.track_list_green[i].get_switch_index()].get_y_one()])					
				
			else:
				if self.track_list_green[i].switch_list[self.track_list_green[i].get_switch_index()].get_switch_position() == False:
					#ex switch 85 in default
					if self.track_list_green[i].switch_list[self.track_list_green[i].get_switch_index()].get_y_stem() < self.track_list_green[i].get_block():
						self.track_list_green[i].set_connection_track_a(self.track_list_green[Track.switch_list[self.track_list_green[i].get_switch_index()].get_y_stem()])
						self.track_list_green[i].set_connection_track_b(self.track_list_green[i+1])
					#ex switch 77 in deafult
					else:
						self.track_list_green[i].set_connection_track_b(self.track_list_green[Track.switch_list[self.track_list_green[i].get_switch_index()].get_y_stem()])
						self.track_list_green[i].set_connection_track_a(self.track_list_green[i-1])
						
				if self.track_list_green[i].switch_list[self.track_list_green[i].get_switch_index()].get_switch_position() == True:
					#ex switch 85 in swapped
					if self.track_list_green[i].switch_list[self.track_list_green[i].get_switch_index()].get_y_stem() < self.track_list_green[i].get_block() and  self.track_list_green[i].switch_list[self.track_list_green[i].get_switch_index()].get_y_zero() < self.track_list_green[i].switch_list[self.track_list_green[i].get_switch_index()].get_y_stem():
						self.track_list_green[i].set_connection_track_a(self.track_list_green[i-1])
						self.track_list_green[i].set_connection_track_b(self.track_list_green[Track.switch_list[self.track_list_green[i].get_switch_index()].get_y_stem()])
					
					#ex switch 77 in swapped
					else:
						self.track_list_green[i].set_connection_track_b(self.track_list_green[Track.switch_list[self.track_list_green[i].get_switch_index()].get_y_stem()])
						self.track_list_green[i].set_connection_track_a(self.track_list_green[i-1])
				#CURRENTLY DO NOT SET NULL FOR LEGS
			
			i+=1

		#update every label with relevant information
		self.ui.selTrackSection.setText(str(self.track_list_green[blckNum].get_line()))
		
		
		self.ui.selTrackSpeed.display(self.track_list_green[blckNum].get_speed_limit()*0.6213711922)
		
		self.ui.selTrackGrade.setText(str(self.track_list_green[blckNum].get_grade()))
		self.ui.selTrackHeater.setText(str(self.track_list_green[blckNum].get_heater_status()))
		
		if(self.track_list_green[blckNum].get_is_station() == True):
			self.ui.selTrackStation.setText(self.track_list_green[blckNum].get_station_name())	
			#CTC outputs
			self.ui.ctcTicketO.display(self.track_list_green[blckNum].get_ticket_count())
			self.ui.ctcTrackUpO.setText("Tickets Updated")
			if(self.track_list_green[blckNum].get_occupied() == True):
				self.ui.train_people_boarding.display(self.track_list_green[blckNum].get_boarding_count())
			else:
				self.ui.train_people_boarding.display(0)
				
			#print(str(self.track_list_green[blckNum].get_station_side()))
			if(self.track_list_green[blckNum].get_station_side() == 1):
				self.ui.selTrackStationSide.setText("Left")
			if(self.track_list_green[blckNum].get_station_side() == 2):
				self.ui.selTrackStationSide.setText("Right")
			if(self.track_list_green[blckNum].get_station_side() == 3):
				self.ui.selTrackStationSide.setText("Left/Right")
			
		else:
			self.ui.selTrackStation.setText('Not a Station')
			self.ui.ctcTicketO.display(0)
			self.ui.train_people_boarding.display(0)
			self.ui.ctcTrackUpO.setText("Not a Station")
			self.ui.selTrackStationSide.setText("Not a Station")
			self.ui.train_people_boarding.display(0)
			
		if(self.track_list_green[blckNum].get_is_crossing() == True):
			self.ui.sigCrossBarrier.setChecked(self.track_list_green[blckNum].get_crossing_status())
			self.ui.sigCrossLights.setChecked(self.track_list_green[blckNum].get_crossing_light())
		
		if(self.track_list_green[blckNum].get_is_crossing() == True):
			self.ui.selTrackCross.setText('Yes')
		else:
			self.ui.selTrackCross.setText('No')	


		if(self.track_list_green[blckNum].get_is_branch() == True):
			self.ui.selTrackBranch.setText('Yes')
		else:
			self.ui.selTrackBranch.setText('No')	

		if(self.track_list_green[blckNum].get_is_switch() == True):
			self.ui.selTrackSW.setText('Yes')
			self.ui.waySwitch.setText(str(self.track_list_green[blckNum].get_connection_track_b().get_block()))
		else:
			self.ui.selTrackSW.setText('No')	
			self.ui.waySwitch.setText('Not a switch')
		
		if(self.track_list_green[blckNum].get_is_underground() == True):
			self.ui.selTrackUnderground.setText('Yes')
		else:
			self.ui.selTrackUnderground.setText('No')	
		
		
		self.ui.selTrackDirection.setText(str(self.track_list_green[blckNum].get_direction()))
		self.ui.selTrackElevation.setText(str(self.track_list_green[blckNum].get_elevation()))
		self.ui.selTrackElevationCumulative.setText(str(self.track_list_green[blckNum].get_elevation_c()))

		
		#railStatus
		self.ui.selTrackRailStat.setText(str(self.track_list_green[blckNum].get_rail_condition()))
		self.ui.selTrackCircStat.setText(str(self.track_list_green[blckNum].get_circuit_condition()))
		self.ui.selTrackPowerStat.setText(str(self.track_list_green[blckNum].get_power_condition()))
		
		
		#railSignal
		if(self.track_list_green[blckNum].get_signal_light() == 'Go'):
			self.ui.sigGo.setChecked(True)
			self.ui.sigSlow.setChecked(False)
			self.ui.sigStop.setChecked(False)
		elif(self.track_list_green[blckNum].get_signal_light() == 'Slow'):
			self.ui.sigGo.setChecked(False)
			self.ui.sigSlow.setChecked(True)
			self.ui.sigStop.setChecked(False)
		elif(self.track_list_green[blckNum].get_signal_light() == 'Stop'):
			self.ui.sigGo.setChecked(False)
			self.ui.sigSlow.setChecked(False)
			self.ui.sigStop.setChecked(True)
		
		#temperature
		self.ui.ambTemp.display(self.track_list_green[blckNum].get_ambient_temp())
		
		#wayside input
		self.ui.wayCommandedSpeed.display(self.track_list_green[blckNum].get_commanded_speed())
		self.ui.wayAuthority.display(str(self.track_list_green[blckNum].get_authority()))
		self.ui.waySignal.setText(str(self.track_list_green[blckNum].get_signal_light()))
		
		#train outputs
			
		self.ui.trainSpeedLimitO.display(self.track_list_green[blckNum].get_speed_limit()*0.6213711922)
		self.ui.trainAuthorityO.display(self.track_list_green[blckNum].get_authority())
		self.ui.trainBeaconO.setText(str(self.track_list_green[blckNum].get_beacon()))
		self.ui.trainCommandedSpeedO.display(self.track_list_green[blckNum].get_commanded_speed()*2.23694)
		
		#Wayside outputs
		self.ui.wayOccupiedO.setText(str(self.track_list_green[blckNum].get_occupied()))
			
#----------------RED LINE-------------------------------------------------------------------------------------

	

	def update_track_info_red(self,blckNum):
		
		#update the table with current occupied blocks
		#print("track model updating red line")
		self.ui.red_line_table.setItem(0,0, QTableWidgetItem("Block Number"))
		self.ui.red_line_table.setItem(0,1, QTableWidgetItem("Status"))	
		
		for i in range(1, len(self.track_list_red)-1):
			#print("in for loop for table " + str(i) + "and is currently " + str(self. 
			if(self.track_list_red[i].get_occupied() == True):
				print("occupied block is" + str(self.track_list_red[i]))
				self.ui.red_line_table.setItem(i,0, QTableWidgetItem(str(self.track_list_red[i].get_block())))
				self.ui.red_line_table.setItem(i,1, QTableWidgetItem("Occupied"))	
			else:
				self.ui.red_line_table.setItem(i,0, QTableWidgetItem(str(self.track_list_red[i].get_block())))
				self.ui.red_line_table.setItem(i,1, QTableWidgetItem("Unoccupied"))	
		#update any connections
		#make track connections
		
		i=1
		while (i <= self.num_lines-1):
			#print(self.track_list[i].get_block())
			if self.track_list_red[i].get_is_switch()==False and  self.track_list_red[i].get_is_switch_leg()==False :						
				#print("block " + str(i) + " is not a switch")
				'''if i == 1:
					print("first block not a switch")
					self.track_list[i].set_connection_track_a(None)
					self.track_list[i].set_connection_track_b(self.track_list[i+1])
				
				if i == self.num_lines or self.track_list[i].get_is_station()==True:
					self.track_list[i].set_connection_track_a(self.track_list[i-1])
					self.track_list[i].set_connection_track_b(None)
				else:'''
				self.track_list_red[i].set_connection_track_a(self.track_list_red[i-1])
				self.track_list_red[i].set_connection_track_b(self.track_list_red[i+1])
							
			elif(self.track_list_red[i].get_is_switch()==True):
				#print("block " + str(i) + " is a switch or switch leg")
				if self.track_list_red[i].switch_list[self.track_list_red[i].get_switch_index()].get_switch_position() == False:
					#print("switch index for block " + str(i)+" is " + str(self.track_list[i].get_switch_index()))
					
					if (self.track_list_red[i].switch_list[self.track_list_red[i].get_switch_index()].get_y_zero() < self.track_list_red[i].get_block()) or (self.track_list_red[i].switch_list[self.track_list_red[i].get_switch_index()].get_y_one() < self.track_list_red[i].get_block()):
						self.track_list_red[i].set_connection_track_b(self.track_list_red[i+1])
						self.track_list_red[i].set_connection_track_a(self.track_list_red[Track.switch_list[self.track_list_red[i].get_switch_index()].get_y_zero()])
					else:	
						self.track_list_red[i].set_connection_track_a(self.track_list_red[i-1])
						self.track_list_red[i].set_connection_track_b(self.track_list_red[Track.switch_list[self.track_list_red[i].get_switch_index()].get_y_zero()])
					
					#self.track_list[i].set_connection_track_a(self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_stem()])
					#self.track_list[i].set_connection_track_b(self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_zero()])
					#self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_one()].set_connection_track_a(None)
				
				if self.track_list_red[i].switch_list[self.track_list_red[i].get_switch_index()].get_switch_position() == True:

					'''self.track_list[i].set_connection_track_a(self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_stem()])
					self.track_list[i].set_connection_track_b(self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_one()])
					self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_zero()].set_connection_track_a(None)	'''
				
					if (self.track_list_red[i].switch_list[self.track_list_red[i].get_switch_index()].get_y_zero() < self.track_list_red[i].get_block()) or (self.track_list_red[i].switch_list[self.track_list_red[i].get_switch_index()].get_y_one() < self.track_list_red[i].get_block()):
						self.track_list_red[i].set_connection_track_b(self.track_list_red[i+1])
						self.track_list_red[i].set_connection_track_a(self.track_list_red[Track.switch_list[self.track_list_red[i].get_switch_index()].get_y_one()])
					else:	
						self.track_list_red[i].set_connection_track_a(self.track_list_red[i-1])
						self.track_list_red[i].set_connection_track_b(self.track_list_red[Track.switch_list[self.track_list_red[i].get_switch_index()].get_y_one()])					
				
			else:
				if self.track_list_red[i].switch_list[self.track_list_red[i].get_switch_index()].get_switch_position() == False:
					#ex switch 85 in default
					if self.track_list_red[i].switch_list[self.track_list_red[i].get_switch_index()].get_y_stem() < self.track_list_red[i].get_block():
						self.track_list_red[i].set_connection_track_a(self.track_list_red[Track.switch_list[self.track_list_red[i].get_switch_index()].get_y_stem()])
						self.track_list_red[i].set_connection_track_b(self.track_list_red[i+1])
					#ex switch 77 in deafult
					else:
						self.track_list_red[i].set_connection_track_b(self.track_list_red[Track.switch_list[self.track_list_red[i].get_switch_index()].get_y_stem()])
						self.track_list_red[i].set_connection_track_a(self.track_list_red[i-1])
						
				if self.track_list_red[i].switch_list[self.track_list_red[i].get_switch_index()].get_switch_position() == True:
					#ex switch 85 in swapped
					if self.track_list_red[i].switch_list[self.track_list_red[i].get_switch_index()].get_y_stem() < self.track_list_red[i].get_block() and  self.track_list_red[i].switch_list[self.track_list_red[i].get_switch_index()].get_y_zero() < self.track_list_red[i].switch_list[self.track_list_red[i].get_switch_index()].get_y_stem():
						self.track_list_red[i].set_connection_track_a(self.track_list_red[i-1])
						self.track_list_red[i].set_connection_track_b(self.track_list_red[Track.switch_list[self.track_list_red[i].get_switch_index()].get_y_stem()])
					
					#ex switch 77 in swapped
					else:
						self.track_list_red[i].set_connection_track_b(self.track_list_red[Track.switch_list[self.track_list_red[i].get_switch_index()].get_y_stem()])
						self.track_list_red[i].set_connection_track_a(self.track_list_red[i-1])
				#CURRENTLY DO NOT SET NULL FOR LEGS
			
			i+=1
		
		'''for j in range (1,len(self.track_list)):
			#this prints all the connections for debug
			try:
				print(self.track_list[j].get_block()," Con A = ", self.track_list[j].get_connection_track_a().get_block(), " Con B = ",self.track_list[j].get_connection_track_b().get_block())
			except:
				print(self.track_list[j].get_block())'''

		#update every label with relevant information
		self.ui.selTrackSection_red.setText(str(self.track_list_red[blckNum].get_line()))
		
		
		self.ui.selTrackSpeed_red.display(self.track_list_red[blckNum].get_speed_limit()*0.6213711922)
		
		self.ui.selTrackGrade_red.setText(str(self.track_list_red[blckNum].get_grade()))
		self.ui.selTrackHeater_red.setText(str(self.track_list_red[blckNum].get_heater_status()))
		
		if(self.track_list_red[blckNum].get_is_station() == True):
			self.ui.selTrackStation_red.setText(self.track_list_red[blckNum].get_station_name())	
			#CTC outputs
			self.ui.ctcTicketO_red.display(self.track_list_red[blckNum].get_ticket_count())
			self.ui.ctcTrackUpO_red.setText("Tickets Updated")
			if(self.track_list_red[blckNum].get_occupied() == True):
				self.ui.train_people_boarding_red.display(self.track_list_red[blckNum].get_boarding_count())
			else:
				self.ui.train_people_boarding_red.display(0)
				
			#print(str(self.track_list[blckNum].get_station_side()))
			if(self.track_list_red[blckNum].get_station_side() == 1):
				self.ui.selTrackStationSide_red.setText("Left")
			if(self.track_list_red[blckNum].get_station_side() == 2):
				self.ui.selTrackStationSide_red.setText("Right")
			if(self.track_list_red[blckNum].get_station_side() == 3):
				self.ui.selTrackStationSide_red.setText("Left/Right")
			
		else:
			self.ui.selTrackStation_red.setText('Not a Station')
			self.ui.ctcTicketO_red.display(0)
			self.ui.train_people_boarding_red.display(0)
			self.ui.ctcTrackUpO_red.setText("Not a Station")
			self.ui.selTrackStationSide_red.setText("Not a Station")
			self.ui.train_people_boarding_red.display(0)
			
		if(self.track_list_red[blckNum].get_is_crossing() == True):
			self.ui.sigCrossBarrier_red.setChecked(self.track_list_red[blckNum].get_crossing_status())
			self.ui.sigCrossLights_red.setChecked(self.track_list_red[blckNum].get_crossing_light())
			self.ui.selTrackCross_red.setText('Yes')
		else:
			self.ui.selTrackCross_red.setText('No')
		
		if(self.track_list_red[blckNum].get_is_branch() == True):
			self.ui.selTrackBranch_red.setText('Yes')
		else:
			self.ui.selTrackBranch_red.setText('No')	

		if(self.track_list_red[blckNum].get_is_switch() == True):
			self.ui.selTrackSW_red.setText('Yes')
			self.ui.waySwitch_red.setText(str(self.track_list_red[blckNum].get_connection_track_b().get_block()))
		else:
			self.ui.selTrackSW_red.setText('No')	
			self.ui.waySwitch_red.setText('Not a switch')
		
		if(self.track_list_red[blckNum].get_is_underground() == True):
			self.ui.selTrackUnderground_red.setText('Yes')
		else:
			self.ui.selTrackUnderground_red.setText('No')	
		
		
		self.ui.selTrackDirection_red.setText(str(self.track_list_red[blckNum].get_direction()))
		self.ui.selTrackElevation_red.setText(str(self.track_list_red[blckNum].get_elevation()))
		self.ui.selTrackElevationCumulative_red.setText(str(self.track_list_red[blckNum].get_elevation_c()))

		
		#railStatus
		self.ui.selTrackRailStat_red.setText(str(self.track_list_red[blckNum].get_rail_condition()))
		self.ui.selTrackCircStat_red.setText(str(self.track_list_red[blckNum].get_circuit_condition()))
		self.ui.selTrackPowerStat_red.setText(str(self.track_list_red[blckNum].get_power_condition()))
		
		if(self.track_list_red[blckNum].get_is_crossing()):
			self.track_list_red[blckNum].set_signal_light == 'Slow'
		
		#railSignal
		if(self.track_list_red[blckNum].get_signal_light() == 'Go'):
			self.ui.sigGo_red.setChecked(True)
			self.ui.sigSlow_red.setChecked(False)
			self.ui.sigStop_red.setChecked(False)
		elif(self.track_list_red[blckNum].get_signal_light() == 'Slow'):
			self.ui.sigGo_red.setChecked(False)
			self.ui.sigSlow_red.setChecked(True)
			self.ui.sigStop_red.setChecked(False)
		elif(self.track_list_red[blckNum].get_signal_light() == 'Stop'):
			self.ui.sigGo_red.setChecked(False)
			self.ui.sigSlow_red.setChecked(False)
			self.ui.sigStop_red.setChecked(True)
		
		#temperature
		self.ui.ambTemp_red.display(self.track_list_red[blckNum].get_ambient_temp())
		
		#wayside input
		self.ui.wayCommandedSpeed_red.display(self.track_list_red[blckNum].get_commanded_speed())
		self.ui.wayAuthority_red.display(str(self.track_list_red[blckNum].get_authority()))
		self.ui.waySignal_red.setText(str(self.track_list_red[blckNum].get_signal_light()))
		
		#train outputs
			
		self.ui.trainSpeedLimitO_red.display(self.track_list_red[blckNum].get_speed_limit()*0.6213711922)
		self.ui.trainAuthorityO_red.display(self.track_list_red[blckNum].get_authority())
		self.ui.trainBeaconO_red.setText(str(self.track_list_red[blckNum].get_beacon()))
		self.ui.trainCommandedSpeedO_red.display(self.track_list_red[blckNum].get_commanded_speed()*2.23694)
		
		#Wayside outputs
		self.ui.wayOccupiedO_red.setText(str(self.track_list_red[blckNum].get_occupied()))

	def set_track_temperature_red(self):
		try :
			inputTemp=int(self.ui.tempSelector_red.text())
		except:
			print("Inputted Temperature Not a Number")
			self.ui.tempSelectorValid_red.setText("Invalid Input\nNot a Number")
		
		if(inputTemp > 118):
			print("Input Track Block too High")
			self.ui.tempSelectorValid_red.setText("Invalid Input\nTemp Too High")
	
		if(inputTemp < -50):
			print("Input Track Temp too Low")
			self.ui.tempSelectorValid_red.setText("Invalid Input\nTemp Too Low")
	
		if inputTemp<32:
			for i in range(1, len(self.track_list_red)):	
				self.track_list_red[i].set_heater_status(True)
		else:
			for i in range(1, len(self.track_list_red)):	
				self.track_list_red[i].set_heater_status(False)
		
		for i in range(1, len(self.track_list_red)):	
			self.track_list_red[i].set_ambient_temp(inputTemp)
		self.update_track_info_red(self.current_block_red)
	
	def toggle_heater_red(self):
		temp = not self.track_list_red[self.current_block_red].get_heater_status()
		for i in range(1, len(self.track_list_red)):	
			self.track_list_red[i].set_heater_status(temp)		
		self.update_track_info_red(self.current_block_red)
	
	def cause_power_fail_red(self):
		#toggle status
		temp = not self.track_list_red[self.current_block_red].get_power_condition()
		
		if(temp == False):
			self.track_list_red[self.current_block_red].set_power_condition(False)
			self.track_list_red[self.current_block_red].set_signal_light('Stop')
			self.update_track_info_red(self.current_block_red)
			print("CAUTION! POWER FAILURE ON BLOCK ", self.current_block_red) 
		else:
			self.track_list_red[self.current_block_red].set_power_condition(True)
			#make sure to send go if all track conditions are good
			if(self.track_list_red[self.current_block_red].get_rail_condition() == True) and (self.track_list_red[self.current_block_red].get_circuit_condition() == True):
				self.track_list_red[self.current_block_red].set_signal_light('Go')
			self.update_track_info_red(self.current_block_red)
			print("POWER Fixed on BLOCK ", self.current_block_red) 

	def cause_circuit_fail_red(self):
		#toggle status
		temp = not self.track_list_red[self.current_block_red].get_circuit_condition()
		
		if(temp == False):
			self.track_list_red[self.current_block_red].set_circuit_condition(False)
			self.track_list_red[self.current_block_red].set_signal_light('Stop')
			print("CAUTION! CIRCUIT FAILURE ON BLOCK ", self.current_block_red) 
			self.update_track_info_red(self.current_block_red)
		else:
			self.track_list_red[self.current_block_red].set_circuit_condition(True)
			#make sure to send go if all track conditions are good
			if(self.track_list_red[self.current_block_red].get_rail_condition() == True) and (self.track_list_red[self.current_block_red].get_power_condition() == True):
				self.track_list_red[self.current_block_red].set_signal_light('Go')
			print("CIRCUIT Fixed on BLOCK ", self.current_block_red) 
			self.update_track_info_red(self.current_block_red)

	def cause_rail_fail_red(self):
		#toggle status
		temp = not self.track_list_red[self.current_block_red].get_rail_condition()
		
		if(temp == False):
			self.track_list_red[self.current_block_red].set_rail_condition(False)
			self.track_list_red[self.current_block_red].set_signal_light('Stop')
			self.track_list_red[self.current_block_red].set_occupied(True)
			self.update_track_info_red(self.current_block_red)
			print("CAUTION! RAIL FAILURE ON BLOCK ", self.current_block_red) 
		else:
			self.track_list_red[self.current_block_red].set_rail_condition(True)
			#make sure to send go if all track conditions are good
			if(self.track_list_red[self.current_block_red].get_circuit_condition() == True) and (self.track_list_red[self.current_block_red].get_power_condition() == True):
				self.track_list_red[self.current_block_red].set_signal_light('Go')
			self.track_list_red[self.current_block_red].set_occupied(False)
			self.update_track_info_red(self.current_block_red)
			print("RAIL Fixed on BLOCK ", self.current_block_red) 
	
	def get_track_info_red(self):
		#get the text inputted by the user and check to see if it's a number
		try :
			inputTrackBlock=int(self.ui.trackSelector_red.text())
		except:
			print("Inputted Track Block Not a Number")
			self.ui.trackSelectorValid_red.setText("Invalid Input\nNot a Number")
		
		#print("numlines:", self.num_lines)
		#print("inputblock:", inputTrackBlock)
		
		if(inputTrackBlock > len(self.track_list_red)):
			print("Input Track Block too High")
			self.ui.trackSelectorValid_red.setText("Invalid Input\nBlock Number Too High")
			return

		
		#otherwise it is a valid input and update everything
		self.ui.trackSelectorValid_red.setText("Valid Input")
		self.current_block_red=inputTrackBlock
		self.update_track_info_red(inputTrackBlock)
	
	
if __name__ == "__main__":
	app = QApplication(sys.argv)

	window = MainWindow()

	#put code here
	
	window.show()
		
	sys.exit(app.exec_())
	
	
	
	
	
	
	