import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, QTimer
from UI import Ui_TrainControllerSW
from simple_pid import PID

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_TrainControllerSW()
        self.ui.setupUi(self)

        #automatic mode stuff
        self.autoMode = True
        self.ui.automaticMode.toggled.connect(self.onAutoManual)

        #commanded speed stuff
        self.setPointSpeed = 43.5
        self.ui.setPointSpeedVal.display(self.setPointSpeed)
        self.ui.speedUpButton.clicked.connect(self.increaseSetPoint)
        self.ui.speedDownButton.clicked.connect(self.decreaseSetPoint)

        #service brake stuff
        self.serviceBrake = False
        self.ui.serviceBrake.pressed.connect(self.serviceBrakeActivated)
        self.ui.serviceBrake.released.connect(self.serviceBrakeDeactivated)

        #service Brake Failure Stuff
        self.ui.causeBrakeFailure.clicked.connect(self.causeBrakeFailure)

        #emergency brake stuff
        self.ui.emergencyBrake.pressed.connect(self.onEmergencyBrake)
        self.ui.emergencyBrake.released.connect(self.onEmergencyBrakeOff)
        self.emergencyBrake = False
        #encoded Track Circuit stuff
        self.actualSpeed = 0
        self.actualSpeedLast = 0
        self.actualSpeedSecond = 0
        self.commandedSpeed = 0
        self.authority = 0
        self.encodedTC = 0
        self.ui.updateTCFake.clicked.connect(self.onUpdateTCFake)
        self.power = 0

        #passenger brake fake stuff
        self.ui.causePassenger.clicked.connect(self.onPassengerBrakeActivated)

        #actual speed fake stuff
        self.ui.updateActualFake.clicked.connect(self.onUpdateActualFake)

        #beacon stuff
        self.ui.updateBeaconFake.clicked.connect(self.onUpdateBeaconFake)
        self.encodedBeacon = 0
        self.upcomingStation = False 
        self.leftDoorsOpen = False
        self.rightDoorsOpen = False
        self.exteriorLightsOn = False
        self.station = "Undefined"
        #setting up stations
        self.stationArray = ("Shadyside","Herron Ave","Swissville","Penn Station","Steel Plaza","First Ave","Station Square","South Hills Junction", 
                            "Pioneer","Edgebrook","Whited","South Bank","Central","Inglewood","Overbrook","Glenburry","Dormont","Mt Lebanon", "Poplar","Castle Shannon")

        #pid loop updates
        self.ui.updatePID.clicked.connect(self.onUpdateKpKi)

        #pid loop stuff
        self.kp = 0
        self.ki = 0
        self.pid = PID(self.kp, self.ki, 0)
        self.pid.output_limits = (0, 120000)
        self.pidTimer = QTimer()
        self.pidTimer.timeout.connect(self.pidLoop)
        self.pidTimer.start(1000)

        #cause engine failure
        self.ui.causeEngineFailure.clicked.connect(self.causeEngineFailure)

        #Announcements
        self.announcement=""
        self.ui.intercom.clicked.connect(self.onAnnouncement)




    def increaseSetPoint(self):
        self.setPointSpeed = self.setPointSpeed + 1
        print(self.setPointSpeed)
        self.displayUpdate()

    def decreaseSetPoint(self):
        if(self.setPointSpeed>0):
            self.setPointSpeed = self.setPointSpeed - 1
        print(self.setPointSpeed)
        self.displayUpdate()

    def displayUpdate(self):
        self.ui.setPointSpeedVal.display(self.setPointSpeed)
        self.ui.commandedSpeedVal.display(self.commandedSpeed)
        self.ui.authority.display(self.authority)
        self.ui.actualSpeedVal.display(self.actualSpeed)
        self.ui.encodedTC.setPlainText(str(bin(self.encodedTC)))
        self.ui.leftDoors.setChecked(self.leftDoorsOpen)
        self.ui.rightDoors.setChecked(self.rightDoorsOpen)
        self.ui.exteriorLights.setChecked(self.exteriorLightsOn)
        self.ui.upcomingStation.setPlainText(str(self.station))
        self.ui.encodedBeacon.setPlainText(str(bin(self.encodedBeacon)))
        self.ui.power.display(self.power)
        if(self.upcomingStation):
            self.ui.upcomingStation.setStyleSheet(u"background-color: rgb(124,252,0);")
        else:
            self.ui.upcomingStation.setStyleSheet(u"background-color: rgb(255,255,255);")
        
    def onEmergencyBrake(self):
        print("Emergency Brake Activated")
        self.commandedSpeed = 0
        self.setpointSpeed = 0
        self.emergencyBrake = True
        self.displayUpdate()

    def onEmergencyBrakeOff(self):
        print("Emergency Brake Released")
        self.emergencyBrake = False


    def serviceBrakeActivated(self):
        self.serviceBrake = True
        print("Service Brake Activated")
        self.setPointSpeed=0
        self.displayUpdate()
    
    def serviceBrakeDeactivated(self):
        self.serviceBrake = False
        print("Service Brake Released")
        self.displayUpdate

    def onPassengerBrakeActivated(self):
        print("Passenger Brake Activated!")
        self.ui.textBrowser_16.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.setPointSpeed=0
        self.commandedSpeed=0

    def onUpdateTCFake(self):
        self.commandedSpeed = float(self.ui.inputCommanded.toPlainText())
        self.authority = float(self.ui.inputAuthority.toPlainText())
        
        print("Fake Commanded" + str(self.commandedSpeed))
        print("Fake Authority" + str(self.authority))
       
        #encoding the track circuit stuff
        cmdInt= int(float(self.commandedSpeed))
        cmdFloat= int(((float(self.commandedSpeed)-cmdInt)*10))
        authInt= int(float(self.authority))
        authFloat= int(((float(self.authority)-authInt)*10))

        if(self.ui.causePickupFailure.checkState()):
            self.encodedTC = (cmdInt-6 & 255)
        else:
            self.encodedTC = (cmdInt & 255)
        self.encodedTC += (cmdFloat & 15) << 8
        self.encodedTC += (authInt & 255) << 12
        self.encodedTC += (authFloat & 15)<< 20
        self.encodedTC += ((cmdInt + cmdFloat + authFloat + authInt) & 1023) << 24
       
        print(self.encodedTC)
        self.decodeTC()

        #updating the display
        self.displayUpdate()

    def onUpdateActualFake(self):
        self.actualSpeedSecond = self.actualSpeedLast
        self.actualSpeedLast = self.actualSpeed
        self.actualSpeed = float(self.ui.actualSpeed.toPlainText())

        #checking to see if there is train engine failure
        self.detectEngineFailure()
        self.detectBrakeFailure()
        self.displayUpdate()

    def detectEngineFailure(self):
        #defined by Train Model
        #stephen send a value as our current velocity symbolizing problem with engine
        if(self.actualSpeed==666):
            self.onEngineFailure()
    
    def causeEngineFailure(self):
        self.actualSpeed=666
        self.detectEngineFailure()

    def onEngineFailure(self):
        self.ui.textBrowser_13.setStyleSheet(u"background-color: rgb(255, 0, 0);")

    def detectBrakeFailure(self):
        # a brake failure is actually when the brakes are stuck on, so if we're slowing down, no brakes are applied and power is not 0 
        print("Brake Failure Detection Occuring")
        print("Service Brake: " + str(self.serviceBrake))
        if(not self.serviceBrake and (self.actualSpeedSecond >= self.actualSpeedLast and self.actualSpeedLast >= self.actualSpeed) and not self.power == 0):
           self.onBrakeFailure()

    def causeBrakeFailure(self):
        self.actualSpeedSecond=17
        self.actualSpeedLast=16
        self.actualSpeed=15
        self.serviceBrake = False
        self.detectBrakeFailure()


    def onBrakeFailure(self):
        self.ui.textBrowser_14.setStyleSheet(u"background-color: rgb(255, 0, 0);") 
    


    def onUpdateBeaconFake(self):
        beaconNum= self.ui.stationNameFake.currentIndex()
        #encoding my beacon
        self.encodedBeacon = int(self.ui.stationUpcoming.checkState()) >> 1
        print(bin(self.encodedBeacon))
        self.encodedBeacon += (int(self.ui.leftDoorsFake.checkState()) >> 1) << 1
        self.encodedBeacon += (int(self.ui.rightDoorsFake.checkState()) >> 1) << 2
        self.encodedBeacon += (int(self.ui.exteriorLightsFake.checkState()) >> 1) << 3
        self.encodedBeacon += (beaconNum & 31) << 4
        print(bin(self.encodedBeacon))
        self.displayUpdate()
        self.decodeBeacon()

    def decodeBeacon(self):
        self.upcomingStation = (self.encodedBeacon & 1)
        self.leftDoorsOpen = (self.encodedBeacon >> 1)&1
        self.rightDoorsOpen = (self.encodedBeacon >> 2)&1
        self.exteriorLightsOn = (self.encodedBeacon >> 3)&1
        self.station = self.stationArray[((self.encodedBeacon >> 4) & 31)]
        self.buildAnnouncement()
        self.onAnnouncement()
        self.displayUpdate()

    def buildAnnouncement(self):
        if(self.upcomingStation):
            self.announcement = str("Arriving at " + self.station + " Station. The doors will open on the ")
            if(self.leftDoorsOpen and self.rightDoorsOpen):
                self.announcement += "left and right.\n"
            elif(self.leftDoorsOpen):
                self.announcement += "left.\n"
            else:
                self.announcement += "right.\n"
        else:
            self.announcement = ""

    def onUpdateKpKi(self):
        self.pid.Ki = float(self.ui.kiInput.toPlainText())
        self.pid.Kp = float(self.ui.kpInput.toPlainText())
        print("Kp Ki values updated" + str(self.pid.Ki) + str(self.pid.Kp))


    def checkSignalPickup(self, tempCmdInt, tempCmdFloat, tempAuthInt, tempAuthFloat, tempCheckSum):
        if(tempCheckSum != tempCmdInt+ tempCmdFloat + tempAuthInt + tempAuthFloat):
            print("Signal Pickup Failure")
            self.ui.textBrowser_15.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        else:
            self.ui.textBrowser_15.setStyleSheet(u"background-color: rgb(255, 255, 255);")


    def decodeTC(self):
        tempCmdInt = self.encodedTC & 255
        tempCmdFloat = (self.encodedTC >> 8) & 15
        tempAuthInt = (self.encodedTC >> 12) & 255
        tempAuthFloat= (self.encodedTC >> 20) & 15
        tempCheckSum = (self.encodedTC >> 24) & 1023
        self.checkSignalPickup(tempCmdInt, tempCmdFloat, tempAuthInt, tempAuthFloat, tempCheckSum)
        if((tempAuthInt == 0 and tempAuthFloat == 0)):
            self.onAuthorityExpiration()

    def onAuthorityExpiration(self):
        print("Authority Expired")
        self.setPointSpeed = 0
        self.commandedSPeed = 0
        self.emergencyBrake = True 

    def pidLoop(self):
        if(self.autoMode):
            self.pid.setpoint = self.commandedSpeed
            self.power = self.pid(self.actualSpeed, dt = 1)
        else:
            self.pid.setpoint = self.setPointSpeed
            self.power = self.pid(self.actualSpeed, dt = 1)
       
        self.displayUpdate()
        print(self.power)

    def onAnnouncement(self):
        self.ui.announcementDisplay.setPlainText(str(self.announcement))

    def onAutoManual(self):
        if(self.ui.automaticMode.isChecked()):
            self.autoMode = True
            print("Auto Mode Entered")
        else:
            self.autoMode = False
            print("Manual Mode Entered")

        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())