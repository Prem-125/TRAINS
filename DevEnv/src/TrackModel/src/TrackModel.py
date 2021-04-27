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

#Train ends at yard by default
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
		signals.track_model_occupancy.emit(self.block, self.occupied)
	
		#if the block is becomming occupied, send signal to train model
		if(in_occupied == True and self.rail_condition == True):
			self.encode_track_circuit_signal()
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
		self.encodedBeacon += self.station_side << 1
		#self.encodedBeacon += (int(self.ui.leftDoorsFake.checkState()) >> 1) << 1
		#self.encodedBeacon += (int(self.ui.rightDoorsFake.checkState()) >> 1) << 2
		
		#if the time is between 7pm and 7am the lights should be on or if the track is underground
		
		#self.encodedBeacon += int(self.is_underground())
		
		self.encodedBeacon += (int(self.is_underground) >> 1) << 3
		
		#self.encodeBeacon+=self.station_name
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
					#self.generate_boarding()
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
						print(Track.switch_num)
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
	
	


#Code for the UI
class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		
		#instance variables
		self.track_list = [Track()]
		self.num_lines = 0
		self.current_block = 0
		self.route_queue_green = []
		
		
		
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

		self.ui.waySwitchBTN.clicked.connect(self.swap_switch)

	#function to load track from a file
	def load_track(self):

		#reset the table
		self.ui.green_line_table.setRowCount(0)
		self.ui.green_line_table.setColumnCount(0)


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
					self.track_list[self.num_lines].set_length(int(row[3]))
					self.track_list[self.num_lines].set_grade(float(row[4]))
					self.track_list[self.num_lines].set_speed_limit(int(row[5]))
					
					self.track_list[self.num_lines].set_station_side(row[7])
					self.track_list[self.num_lines].set_elevation(float(row[8]))
					self.track_list[self.num_lines].set_elevation_c(float(row[9]))
					
					#add base default values for each object 
					self.track_list[self.num_lines].set_heater_status(False)
					self.track_list[self.num_lines].set_rail_condition(True)
					self.track_list[self.num_lines].set_circuit_condition(True)
					self.track_list[self.num_lines].set_power_condition(True)
					self.track_list[self.num_lines].set_ambient_temp(70)
					
					#temporary simulated signals from wayside
					self.track_list[self.num_lines].set_commanded_speed(35)
					self.track_list[self.num_lines].set_authority(10)
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
		
		#make sure that all the switch legs have a corresponding switch_index
		for i in range(len(Track.switch_list)):
			print(Track.switch_list[i].get_y_zero())
			if self.track_list[Track.switch_list[i].get_y_zero()].get_switch_index() == 0:
				#print("setting index " + str(i))
				self.track_list[Track.switch_list[i].get_y_zero()].set_switch_index(i)
			if self.track_list[Track.switch_list[i].get_y_one()].get_switch_index() == 0:
				#print("setting index " + str(i))
				self.track_list[Track.switch_list[i].get_y_one()].set_switch_index(i)
		
		print("parsing completed")
		signals.need_new_block.connect(self.send_block_to_model)
		signals.wayside_to_track.connect(self.get_wayside_info)
		signals.train_creation.connect(self.set_occupied_initial)
		signals.wayside_block_open.connect(self.get_open_block)
		
		
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
				
		
		#initialize the table
		self.ui.green_line_table.setColumnCount(2)
		self.ui.green_line_table.setRowCount(len(self.track_list))
		#for i in range(0, len(self.track_list)+1):
			#self.ui.green_line_table.insertRow(i)
		
		#default load block 63
		self.update_track_info(63)
		
		
	#function to tell me where the train is
	def send_block_to_model(self,block,id):
		#print("sent block123")
		print("block length: " + str(self.track_list[block+1].get_length()))
		self.track_list[block].set_occupied(False)
		self.route_queue_green.pop(0)
		
		print("just left block " + str(block) + " next is " + str(self.route_queue_green[0]))
		self.track_list[self.route_queue_green[0]].set_occupied(True, id)
		if(self.track_list[self.route_queue_green[1]].is_station):
			self.track_list[self.route_queue_green[1]].encode_beacon()
			signals.Beacon_signal.emit(self.track_list[self.route_queue_green[1]].encodedBeacon, id) # ACTUALLY CALCULATE THE BEACON VAL AND BLOCK NUM
		self.update_track_info(self.current_block)
		
	
	#function for inital train spawn
	def set_occupied_initial(self, track_line, id):
		if (track_line == "Green"):
			self.route_queue_green.pop(0)
			self.track_list[63].set_occupied(True, id)
		else:
			self.track_list[9].set_occupied(True, id)

		
	#function to update from wayside
	def get_wayside_info(self, block_in, authority_in, commanded_speed_in):
		self.track_list[block_in].set_authority(authority_in)
		self.track_list[block_in].set_commanded_speed(commanded_speed_in*(5.0/18.0))
		print("Sending occupancy to wayside")

	def get_open_block(self, line_in, in_block): #add line field for when red line is added 
		self.track_list[in_block].set_rail_condition(True)
		self.track_list[in_block].set_circuit_condition(True)
		self.track_list[in_block].set_power_condition(True)

	def get_track_info(self):
		#get the text inputted by the user and check to see if it's a number
		try :
			inputTrackBlock=int(self.ui.trackSelector.text())
		except:
			print("Inputted Track Block Not a Number")
			self.ui.trackSelectorValid.setText("Invalid Input\nNot a Number")
		
		print("numlines:", self.num_lines)
		print("inputblock:", inputTrackBlock)
		
		if(inputTrackBlock > self.num_lines):
			print("Input Track Block too High")
			self.ui.trackSelectorValid.setText("Invalid Input\nBlock Number Too High")
			return

		
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
			self.track_list[self.current_block].set_occupied(True)
			self.update_track_info(self.current_block)
			print("CAUTION! RAIL FAILURE ON BLOCK ", self.current_block) 
		else:
			self.track_list[self.current_block].set_rail_condition(True)
			#make sure to send go if all track conditions are good
			if(self.track_list[self.current_block].get_circuit_condition() == True) and (self.track_list[self.current_block].get_power_condition() == True):
				self.track_list[self.current_block].set_signal_light('Go')
			self.track_list[self.current_block].set_occupied(False)
			self.update_track_info(self.current_block)
			print("RAIL Fixed on BLOCK ", self.current_block) 

	def cause_circuit_fail(self):
		#toggle status
		temp = not self.track_list[self.current_block].get_circuit_condition()
		
		if(temp == False):
			self.track_list[self.current_block].set_circuit_condition(False)
			self.track_list[self.current_block].set_signal_light('Stop')
			print("CAUTION! CIRCUIT FAILURE ON BLOCK ", self.current_block) 
			self.update_track_info(self.current_block)
		else:
			self.track_list[self.current_block].set_circuit_condition(True)
			#make sure to send go if all track conditions are good
			if(self.track_list[self.current_block].get_rail_condition() == True) and (self.track_list[self.current_block].get_power_condition() == True):
				self.track_list[self.current_block].set_signal_light('Go')
			print("CIRCUIT Fixed on BLOCK ", self.current_block) 
			self.update_track_info(self.current_block)

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
		for i in range(1, len(self.track_list)):	
			self.track_list[i].set_heater_status(temp)		
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
			for i in range(1, len(self.track_list)):	
				self.track_list[i].set_heater_status(True)
		else:
			for i in range(1, len(self.track_list)):	
				self.track_list[i].set_heater_status(False)
		
		for i in range(1, len(self.track_list)):	
			self.track_list[i].set_ambient_temp(inputTemp)
		
		self.update_track_info(self.current_block)
	
	def swap_switch(self): #change this to be inside the swtich class
		if(self.track_list[self.current_block].get_is_switch() == True):
			temp = not self.track_list[self.current_block].switch_list[Track.switch_num].get_switch_position()
			self.track_list[self.current_block].switch_list[Track.switch_num].set_switch_position(temp)
			self.update_track_info(self.current_block)
	
	def update_track_info(self,blckNum):
		
		#update the table with current occupied blocks
	
		
		#creat a variable that hold the number of occupied blocks
		#num_occupied_blocks = 0
		#loop through the whole track list to find if any occupied blocks
		#for(i=0, i<=len(self.track_list), i++)
		#	if(if(self.track_list[i-1].get_occupied == True)
		print("track model updating")
		self.ui.green_line_table.setItem(0,0, QTableWidgetItem("Block Number"))
		self.ui.green_line_table.setItem(0,1, QTableWidgetItem("Status"))	
		
		for i in range(1, len(self.track_list)):
			#print("in for loop for table " + str(i) + "and is currently " + str(self. 
			if(self.track_list[i].get_occupied() == True):
				print("occupied block is" + str(self.track_list[i]))
				self.ui.green_line_table.setItem(i,0, QTableWidgetItem(str(self.track_list[i].get_block())))
				self.ui.green_line_table.setItem(i,1, QTableWidgetItem("Occupied"))	
			else:
				self.ui.green_line_table.setItem(i,0, QTableWidgetItem(str(self.track_list[i].get_block())))
				self.ui.green_line_table.setItem(i,1, QTableWidgetItem("Unoccupied"))	

		#print("-----------------------------------------------------------------------------------")
		#update any connections
		#make track connections
		
		i=1
		while (i <= self.num_lines-1):
			#print(self.track_list[i].get_block())
			if self.track_list[i].get_is_switch()==False and  self.track_list[i].get_is_switch_leg()==False :						
				#print("block " + str(i) + " is not a switch")
				'''if i == 1:
					print("first block not a switch")
					self.track_list[i].set_connection_track_a(None)
					self.track_list[i].set_connection_track_b(self.track_list[i+1])
				
				if i == self.num_lines or self.track_list[i].get_is_station()==True:
					self.track_list[i].set_connection_track_a(self.track_list[i-1])
					self.track_list[i].set_connection_track_b(None)
				else:'''
				self.track_list[i].set_connection_track_a(self.track_list[i-1])
				self.track_list[i].set_connection_track_b(self.track_list[i+1])
							
			elif(self.track_list[i].get_is_switch()==True):
				#print("block " + str(i) + " is a switch or switch leg")
				if self.track_list[i].switch_list[self.track_list[i].get_switch_index()].get_switch_position() == False:
					print("switch index for block " + str(i)+" is " + str(self.track_list[i].get_switch_index()))
					
					if (self.track_list[i].switch_list[self.track_list[i].get_switch_index()].get_y_zero() < self.track_list[i].get_block()) or (self.track_list[i].switch_list[self.track_list[i].get_switch_index()].get_y_one() < self.track_list[i].get_block()):
						self.track_list[i].set_connection_track_b(self.track_list[i+1])
						self.track_list[i].set_connection_track_a(self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_zero()])
					else:	
						self.track_list[i].set_connection_track_a(self.track_list[i-1])
						self.track_list[i].set_connection_track_b(self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_zero()])
					
					#self.track_list[i].set_connection_track_a(self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_stem()])
					#self.track_list[i].set_connection_track_b(self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_zero()])
					#self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_one()].set_connection_track_a(None)
				
				if self.track_list[i].switch_list[self.track_list[i].get_switch_index()].get_switch_position() == True:

					'''self.track_list[i].set_connection_track_a(self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_stem()])
					self.track_list[i].set_connection_track_b(self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_one()])
					self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_zero()].set_connection_track_a(None)	'''
				
					if (self.track_list[i].switch_list[self.track_list[i].get_switch_index()].get_y_zero() < self.track_list[i].get_block()) or (self.track_list[i].switch_list[self.track_list[i].get_switch_index()].get_y_one() < self.track_list[i].get_block()):
						self.track_list[i].set_connection_track_b(self.track_list[i+1])
						self.track_list[i].set_connection_track_a(self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_one()])
					else:	
						self.track_list[i].set_connection_track_a(self.track_list[i-1])
						self.track_list[i].set_connection_track_b(self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_one()])					
				
			else:
				if self.track_list[i].switch_list[self.track_list[i].get_switch_index()].get_switch_position() == False:
					#ex switch 85 in default
					if self.track_list[i].switch_list[self.track_list[i].get_switch_index()].get_y_stem() < self.track_list[i].get_block():
						self.track_list[i].set_connection_track_a(self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_stem()])
						self.track_list[i].set_connection_track_b(self.track_list[i+1])
					#ex switch 77 in deafult
					else:
						self.track_list[i].set_connection_track_b(self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_stem()])
						self.track_list[i].set_connection_track_a(self.track_list[i-1])
						
				if self.track_list[i].switch_list[self.track_list[i].get_switch_index()].get_switch_position() == True:
					#ex switch 85 in swapped
					if self.track_list[i].switch_list[self.track_list[i].get_switch_index()].get_y_stem() < self.track_list[i].get_block() and  self.track_list[i].switch_list[self.track_list[i].get_switch_index()].get_y_zero() < self.track_list[i].switch_list[self.track_list[i].get_switch_index()].get_y_stem():
						self.track_list[i].set_connection_track_a(self.track_list[i-1])
						self.track_list[i].set_connection_track_b(self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_stem()])
					
					#ex switch 77 in swapped
					else:
						self.track_list[i].set_connection_track_b(self.track_list[Track.switch_list[self.track_list[i].get_switch_index()].get_y_stem()])
						self.track_list[i].set_connection_track_a(self.track_list[i-1])
				#CURRENTLY DO NOT SET NULL FOR LEGS
			
			i+=1
		
		'''for j in range (1,len(self.track_list)):
			#this prints all the connections for debug
			try:
				print(self.track_list[j].get_block()," Con A = ", self.track_list[j].get_connection_track_a().get_block(), " Con B = ",self.track_list[j].get_connection_track_b().get_block())
			except:
				print(self.track_list[j].get_block())'''

		#update every label with relevant information
		self.ui.selTrackSection.setText(str(self.track_list[blckNum].get_line()))
		
		
		self.ui.selTrackSpeed.display(self.track_list[blckNum].get_speed_limit()*0.6213711922)
		
		self.ui.selTrackGrade.setText(str(self.track_list[blckNum].get_grade()))
		self.ui.selTrackHeater.setText(str(self.track_list[blckNum].get_heater_status()))
		
		if(self.track_list[blckNum].get_is_station() == True):
			self.ui.selTrackStation.setText(self.track_list[blckNum].get_station_name())	
			#CTC outputs
			self.ui.ctcTicketO.display(self.track_list[blckNum].get_ticket_count())
			self.ui.ctcTrackUpO.setText("Tickets Updated")
			self.ui.train_people_boarding.display(self.track_list[blckNum].get_boarding_count())
			
			
			if(self.track_list[blckNum].get_station_side() == 0):
				self.ui.selTrackStationSide.setText("Left")
			if(self.track_list[blckNum].get_station_side() == 1):
				self.ui.selTrackStationSide.setText("Right")
			if(self.track_list[blckNum].get_station_side() == 3):
				self.ui.selTrackStationSide.setText("Left/Right")
			
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
		
		if(self.track_list[blckNum].get_is_underground() == True):
			self.ui.selTrackUnderground.setText('Yes')
		else:
			self.ui.selTrackUnderground.setText('No')	
		
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
		self.ui.wayAuthority.display(str(self.track_list[blckNum].get_authority()))
		self.ui.waySignal.setText(str(self.track_list[blckNum].get_signal_light()))
		
		#train outputs
		self.ui.trainSpeedLimitO.display(self.track_list[blckNum].get_speed_limit()*0.6213711922)
		self.ui.trainAuthorityO.display(self.track_list[blckNum].get_authority())
		self.ui.trainBeaconO.setText(str(self.track_list[blckNum].get_beacon()))
	
		
		#Wayside outputs
		self.ui.wayOccupiedO.setText(str(self.track_list[blckNum].get_occupied()))
		
		#check to see which blocks are occupied and show them in the list 
		'''occupied_string = ''
		for i in range(0,len(self.track_list)):
			if(self.track_list[i].get_occupied() == True):
				added_string = "Block " + self.track_list[i].get_block() + "\n"
		
		self.occupied_block_list.setText(occupied_string)'''
			

		
if __name__ == "__main__":
	app = QApplication(sys.argv)

	window = MainWindow()

	#put code here
	
	window.show()
		
	sys.exit(app.exec_())
	
	
	
	
	
	
	