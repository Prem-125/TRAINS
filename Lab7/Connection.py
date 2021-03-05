class Person:
	def __init__(self, mailSys, tel):
		self.system = mailSys
		self.phone = tel
		self.curMailbox
		self.curRec=''
		self.accKeys = ''
		self.state = 0
		
		self.DISCONNECTED = 0
		self.CONNECTED = 1
		self.RECORDING = 2
		self.MAILBOX_MENU = 3
		self.MESSAGE_MENU = 4
		self.CHANGE_PASSCODE = 5
		self.CHANGE_GREETING = 6
		
		self.INTIAL_PROMPT = "Enter mailbox number followed by #"
		self.MAILBOX_MENU_TEXT = "Enter 1 to listen to your messages\nEnter 2 to change your passcode\nEnter 3 to change your greeting"	 
		self.MESSAGE_MENU_TEXT = "Enter 1 to listen to the current message\nEnter 2 to save the current message\nEnter 3 to delete the current message\nEnter 4 to return to the main menu"

	def dial(self, key):
		if (self.state == self.CONNECTED):
			self.connect(key)
		elif (self.state == self.RECORDING):
			self.login(key)
		elif (self.state == self.CHANGE_PASSCODE):
			self.changePasscode(key)
		elif (self.state == self.CHANGE_GREETING):
			self.changeGreeting(key)
		elif (self.state == self.MAILBOX_MENU):
			self.mailboxMenu(key)
		elif (self.state == self.MESSAGE_MENU):
			self.messageMenu(key)
			
			
	def record (self,voice):
		if (self.state == self.RECORDING or self.state == self.CHANGE_GREETING):
			self.curRec += voice
			
	def hangup(self):
		if (self.state == self.RECORDING):
			self.curMailbox.addMessage(Message(self.curRec))
		self.resetConnection()
		
	def resetConnection(self):
		self.curRec = ''
		self.accKeys = ''
		self.state = self.CONNECTED
		self.phone.speak(self.INTIAL_PROMPT)
		
	def connect(self,key):
		if (key == '#'):
			self.curMailbox = self.system.findMailbox(self.accKeys)
			if (self.curMailbox != None):
				self.state = self.RECORDING
				self.phone.speak(self.curMailbox.getGreeting())
			else:
				self.phone.speak("Incorrect mailbox number. Try again!")
				self.accKeys=''
		else:
			accKeys+=key
			
	def login(self,key):
	   if(key == '#'):
		  if(self.currentMailbox.checkPasscode(self.accumulatedKeys)):
			 self.state = self.MAILBOX_MENU
			 self.phone.speak(self.MAILBOX_MENU_TEXT)
		  else:
			 self.phone.speak("Incorrect passcode. Try again!")
			 self.accumulatedKeys = ''
	   else:
		  self.accumulatedKeys += key

	def changePasscode(self,key):
	   if(key == '#'):
		  self.currentMailbox.setPasscode(self.accumulatedKeys)
		  self.state = self.MAILBOX_MENU
		  self.phone.speak(self.MAILBOX_MENU_TEXT)
		 self.accumulatedKeys = ""


	def changeGreeting(self,key):
	   if(key == '#'):
		  self.currentMailbox.setGreeting(self.currentRecording)
		  self.currentRecording = ""
		  self.state = self.MAILBOX_MENU
		  self.phone.speak(self.MAILBOX_MENU_TEXT)

	def mailboxMenu(self,key):
	   if(key == '1'):
		  self.state = self.MESSAGE_MENU
		  self.phone.speak(self.MESSAGE_MENU_TEXT)
	   elif(key == '2'):
		  self.state = self.CHANGE_PASSCODE
		  self.phone.speak("Enter new passcode followed by the # key")
	   elif(key == '3'):
		  self.state = self.CHANGE_GREETING
		  self.phone.speak("Record your greeting, then press the # key")


	def messageMenu(self,key):
	   if(key == '1'):
		  self.output = ''
		  self.m = self.currentMailbox.getCurrentMessage()
		  if(m == None):
			 self.output += 'No messages.\n'
		  else:
			 self.output += m.getText() + "\n"
		  self.output += self.MESSAGE_MENU_TEXT
		  self.phone.speak(self.output)
	   elif(key == '2'):
		  self.currentMailbox.saveCurrentMessage()
		  self.phone.speak(self.MESSAGE_MENU_TEXT)
	   elif(key == '3'):
		  self.currentMailbox.removeCurrentMessage()
		  self.phone.speak(self.MESSAGE_MENU_TEXT)
	   elif(key == '4'):
		  self.state = self.MAILBOX_MENU
		  self.phone.speak(self.MAILBOX_MENU_TEXT)	
			
			
			
			
			
			