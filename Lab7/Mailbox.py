from MessageQueue.py import MessageQueue
from Message.py import Message

class Mailbox:

    self.passCode = ""
    self.greeting = ""
    self.newMessage
    self.keptMessages
    #newMessages MessageQueue
    #keptMessages MessageQueue
    #greeting string
    #passcodenewMessages
    def __init__(self, aPasscode, aGreeting):
        self.passcode = aPasscode
        self.greeting = aGreeting
        self.newMessages = MessageQueue()
        self.keptMessages = MessageQueue()

    def checkPasscode(self, pscode):
        return(pscode == self.passCode)

    def addMessage(self, aMessage):
        newMessages.add(aMessage)
    
    def getCurrentMessage(self):
        if(self.newMessages.size()>0):
                return self.newMessages.peek()
        elif(keptMessages.size()>0):
                return self.keptMessages.peek()   
        else:
            return None

    def removeCurrentMessage(self):
        if(self.newMessages.size()>0):
            return (self.newMessages.remove())
        elif(self.keptMessages.size()>0):
            return (self.keptMessages.remove())
        else:
            return None
    
    def saveCurrentMessage(self):
        m = removeCurrentMessage()
        if(not m == None):
            self.keptMessages.add(m)
    
    def setGreeting(self, newGreetingString):
        self.greeting = newGreetingString

    def setPasscode(self, newPasscode):
        self.passcode = newPasscode
    
    def getGreeting(self):
        return self.greeting

