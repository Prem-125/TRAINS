from MailSystem.py import MailSystem

class MessageQueue:
	
	def _init_(self):
		#declare anarraylist
		self.queue = ArrayList(Message)
		

	def remove(self):
		#remove the last list item
		self.queue.remove()
	
	def size(self):
		#return the arrayList length
		return len(self.queue)
		
	def peak(self)
		#return the last element of the arraylist
		return self.queue[-1]
	
	def add(self, messageIn)
		#add a new message to the list
		self.queue.append(messageIn)
	
	