import sys
import random 

class Telephone:
	
	def speak(output):
		print output

	def run(c):
		more = True
		while(more):
			inputInfo = input()
			if(inputInfo==None):
				return
			elif(inputInfo.upper() == "H"):
				c.hangup()
			elif(inputInfo.upper()=="Q"):
				more=False
			elif(len(inputInfo)== 1 and "1234567890#".find(inputInfo)>=0):
				c.dial(inputInfo)
			else:
				c.record(inputInfo)

