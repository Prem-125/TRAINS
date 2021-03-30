import sys, time
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
        self.onAutoManual()

        #commanded speed stuff
        self.setPointSpeed = 0
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
        self.actualSpeed = float(0)
        self.actualSpeedLast = float(0)
        self.actualSpeedSecond = float(0)
        self.commandedSpeed = float(0)
        self.authority = float(0)
        self.encodedTC = 0
        self.ui.updateTCFake.clicked.connect(self.onUpdateTCFake)
        self.power = float(0)

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
        
        self.station = " "
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

        self.ui.temperature.valueChanged.connect(self.onTemperatureChange)
        self.temperature = 70

        #auto mode loop
        self.alreadyWaiting=False

        #manual mode loop
        self.openedl = False
        self.openedr = False

        #lights sending to test ui
        
        self.ui.interiorLights_2.setEnabled(False)
        self.ui.exteriorLights_2.setEnabled(False)
        self.ui.interiorLights.stateChanged.connect(self.onIntLightsChanged)
        self.ui.exteriorLights.stateChanged.connect(self.onExtLightsChanged)





    #increase: used to increase setpoint speed
    def increaseSetPoint(self):
        if(self.setPointSpeed+1 <= self.commandedSpeed):
            self.setPointSpeed = self.setPointSpeed + 1
            print(self.setPointSpeed)
        self.displayUpdate()

    #decreaseSetPoint: used to decrease setpoint speed
    def decreaseSetPoint(self):
        if(self.setPointSpeed>0):
            self.setPointSpeed = self.setPointSpeed - 1
        print(self.setPointSpeed)
        self.displayUpdate()

    #displayUpdate: used to update all display features
    def displayUpdate(self):
        self.ui.setPointSpeedVal.display(self.setPointSpeed)
        self.ui.commandedSpeedVal.display(self.commandedSpeed)
        self.ui.authority.display(self.authority)
        self.ui.actualSpeedVal.display(self.actualSpeed)
        self.ui.encodedTC.setPlainText(str(bin(self.encodedTC)))
        
        if(self.serviceBrake):
            self.ui.textBrowser_9.setPlainText("S Brake Active")
            self.ui.textBrowser_11.setPlainText("S Brake Active")
        else:
            self.ui.textBrowser_9.setPlainText("S Brake Inactive")
            self.ui.textBrowser_11.setPlainText("S Brake Inactive")

        if(self.emergencyBrake):
            self.ui.textBrowser_8.setPlainText("E Brake Active")
            self.ui.textBrowser_10.setPlainText("E Brake Active")
        else:
            self.ui.textBrowser_8.setPlainText("E Brake Inactive")
            self.ui.textBrowser_10.setPlainText("E Brake Inactive")


        #to be removed once fake inputs are stripped
        if(self.autoMode == True):
            self.ui.leftDoors.setChecked(self.leftDoorsOpen)
            self.ui.rightDoors.setChecked(self.rightDoorsOpen)
        
        #when you are in not auto mode
        if(self.autoMode == False):
            self.leftDoors = self.ui.leftDoors.isChecked()
            self.rightDoors = self.ui.rightDoors.isChecked()
            self.openDoorsManual()
        if(self.autoMode):
            self.ui.exteriorLights.setChecked(self.exteriorLightsOn)
        self.ui.upcomingStation.setPlainText(str(self.station))
        self.ui.encodedBeacon.setPlainText(str(bin(self.encodedBeacon)))
        self.ui.power.display(self.power/1000)
        self.ui.textBrowser_17.setPlainText(str(int(self.power)))
        if(self.upcomingStation):
            self.ui.upcomingStation.setStyleSheet(u"background-color: rgb(124,252,0);")
            #going through our arrival procedures
            if(self.alreadyWaiting == False):
                self.onArrival()
        else:
            self.ui.upcomingStation.setStyleSheet(u"background-color: rgb(255,255,255);")
        
    #onEmergencyBrake: used to enable emergency brake
    def onEmergencyBrake(self):
        print("Emergency Brake Activated")
        self.setpointSpeed = 0
        self.power=0
        self.emergencyBrake = True
        self.displayUpdate()

    #onEmergencyBrakeOff: used to disable emergency brake upon release
    def onEmergencyBrakeOff(self):
        print("Emergency Brake Released")
        self.emergencyBrake = False
        self.displayUpdate()


    #serviceBrakeActivated: used when service Brake activated
    def serviceBrakeActivated(self):
        self.serviceBrake = True
        print("Service Brake Activated")
        self.setPointSpeed=0
        self.power=0
        self.displayUpdate()

    #serviceBrakeDeactivated: used when service brake released
    def serviceBrakeDeactivated(self):
        self.serviceBrake = False
        print("Service Brake Released")
        self.displayUpdate()

    #onPassengerBrakeActivated: act upon passenger brake
    def onPassengerBrakeActivated(self):
        print("Passenger Brake Activated!")
        self.ui.textBrowser_16.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.emergencyBrake = True
        self.setPointSpeed=0
        self.commandedSpeed=0


    #onUpdateTCFake: used to act upon TC Values
    def onUpdateTCFake(self):
        self.commandedSpeed = (2.237 * float(self.ui.inputCommanded.toPlainText()))
        self.authority = float (float(self.ui.inputAuthority.toPlainText()) * 3.28084 )
        
        print("Fake Commanded" + str(self.commandedSpeed))
        print("Fake Authority" + str(self.authority))
       
        if(self.authority <= 0):
            self.onAuthorityExpiration()

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

    #onUpdateActualFake: used for updating current speed
    def onUpdateActualFake(self):
        self.actualSpeedSecond = self.actualSpeedLast
        self.actualSpeedLast = self.actualSpeed
        self.actualSpeed = (2.237 * float(self.ui.actualSpeed.toPlainText()))

        #checking to see if there is train engine failure
        self.detectEngineFailure()
        self.detectBrakeFailure()
        self.displayUpdate()

    #onBrakeFailure: used to detect engine failures
    def detectEngineFailure(self):
        #defined by Train Model
        #stephen send a value as our current velocity symbolizing problem with engine
        if(self.actualSpeed==666):
            self.onEngineFailure()
    
    #causeEngineFailure: used to cause engine failures
    def causeEngineFailure(self):
        self.actualSpeed=666
        self.detectEngineFailure()

    #onEngineFailure: used to act upon engine failures
    def onEngineFailure(self):
        self.ui.textBrowser_13.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.emergencyBrake = true

    #detectBrakeFailure: used to detect brake failures
    def detectBrakeFailure(self):
        # a brake failure is actually when the brakes are stuck on, so if we're slowing down, no brakes are applied and power is not 0 
        #print("Brake Failure Detection Occuring")
        #print("Service Brake: " + str(self.serviceBrake))
        if(not self.serviceBrake and (self.actualSpeedSecond > self.actualSpeedLast and self.actualSpeedLast > self.actualSpeed) and not self.power == 0):
           self.onBrakeFailure()

    #causeBrakeFailure: used to simulate brake failures
    def causeBrakeFailure(self):
        self.actualSpeedSecond=17
        self.actualSpeedLast=16
        self.actualSpeed=15
        self.serviceBrake = False
        self.detectBrakeFailure()


    #onBrakeFailure: used to act on brake failures
    def onBrakeFailure(self):
        self.ui.textBrowser_14.setStyleSheet(u"background-color: rgb(255, 0, 0);") 
        self.emergencyBrake = True
    

    #onUpdateBeaconFake: Used to update beacon values
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

    #decodeBeacon: Used to decode beacon
    def decodeBeacon(self):
        self.upcomingStation = (self.encodedBeacon & 1)
        self.leftDoorsOpen = (self.encodedBeacon >> 1)&1
        self.rightDoorsOpen = (self.encodedBeacon >> 2)&1
        self.exteriorLightsOn = (self.encodedBeacon >> 3)&1
        self.station = self.stationArray[((self.encodedBeacon >> 4) & 31)]
        self.buildAnnouncement()
        if(self.autoMode):
            self.onAnnouncement()
        self.displayUpdate()

    #buildAnnouncement: Used to build announcement
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

    #onUpdateKpKi: Used to update Kp/Ki Values
    def onUpdateKpKi(self):
        self.pid.Ki = float(self.ui.kiInput.toPlainText())
        self.pid.Kp = float(self.ui.kpInput.toPlainText())
        print("Kp Ki values updated" + str(self.pid.Ki) + str(self.pid.Kp))

    #checkSignalPickup: Used to detect and act on signal pickup failures
    def checkSignalPickup(self, tempCmdInt, tempCmdFloat, tempAuthInt, tempAuthFloat, tempCheckSum):
        if(tempCheckSum != tempCmdInt+ tempCmdFloat + tempAuthInt + tempAuthFloat):
            print("Signal Pickup Failure")
            self.ui.textBrowser_15.setStyleSheet(u"background-color: rgb(255, 0, 0);")
            self.emergencyBrake = True
        else:
            self.ui.textBrowser_15.setStyleSheet(u"background-color: rgb(255, 255, 255);")

    #decodeTC: Used to decode track circuit
    def decodeTC(self):
        tempCmdInt = self.encodedTC & 255
        tempCmdFloat = (self.encodedTC >> 8) & 15
        tempAuthInt = (self.encodedTC >> 12) & 255
        tempAuthFloat= (self.encodedTC >> 20) & 15
        tempCheckSum = (self.encodedTC >> 24) & 1023
        self.checkSignalPickup(tempCmdInt, tempCmdFloat, tempAuthInt, tempAuthFloat, tempCheckSum)
        #if((tempAuthInt == 0 and tempAuthFloat == 0)):
            #self.onAuthorityExpiration()

    #onAuthorityExpiration: Used as emergency procedure if authority has expired
    def onAuthorityExpiration(self):
        print("Authority Expired")
        self.setPointSpeed = 0
        self.commandedSpeed = 0
        self.emergencyBrake = True
        self.ui.textBrowser_5.setStyleSheet(u"background-color: rgb(255,0,0);")   

    #pidLoop: used to calculate power
    def pidLoop(self):
        #print("INPID")
        print("auto mode = " + str(self.autoMode))
        print("self.upComingStation = " + str(self.upcomingStation))
        print("service brake" + str(self.serviceBrake))
        print("emergency brake" + str(self.emergencyBrake))
        if(self.autoMode and not self.upcomingStation and ((not self.serviceBrake ) and ( not self.emergencyBrake))):
            print("PID Auto")
            self.pid.setpoint = self.commandedSpeed
            self.power = self.pid(self.actualSpeed, dt = 1)
        elif(not(self.setPointSpeed == 0) and not self.serviceBrake and not self.emergencyBrake and not self.ui.leftDoors.isChecked() and not self.ui.rightDoors.isChecked()):
            print("PID Manual")
            self.pid.setpoint = self.setPointSpeed
            self.power = self.pid(self.actualSpeed, dt = 1)
        else:
            self.pid.setpoint=0
            self.power= 0
            print("inPIDOff")
        self.displayUpdate()
        # print(self.power)

    #onAnnouncement: Used to display announcement
    def onAnnouncement(self):
        self.ui.announcementDisplay.setPlainText(str(self.announcement))
        self.ui.intercomFake.setPlainText(str(self.announcement))

    #onAutoManual: Used to differentiate between operation modes
    def onAutoManual(self):
        if(self.ui.automaticMode.isChecked()):
            self.autoMode = True
            print("Auto Mode Entered")

            #making the door checkboxes not usable
            self.ui.leftDoors.setEnabled(False)
            self.ui.rightDoors.setEnabled(False)

        else:
            self.autoMode = False
            print("Manual Mode Entered")

            #making the door checkboxes usable
            self.ui.leftDoors.setEnabled(True)
            self.ui.rightDoors.setEnabled(True)

    def onArrival(self):
        #if we are in autoMode, and we have upComingStation = true, stop the train
        if(self.autoMode == True):
            self.alreadyWaiting = True
            self.previousCommanded = self.commandedSpeed
            self.serviceBrake = True
            self.commandedSpeed = 0
            self.power = 0
            
            self.waitTimer = QTimer()
            self.waitTimer.timeout.connect(self.checkVel)
            self.waitTimer.start(1000)

        else:
            ...
            #Letting use open the doors on their own
            
    #openDoorsManual: used in Manual Mode to open/close doors
    def openDoorsManual(self):
        if(self.autoMode == False):
            if(self.actualSpeed == 0):
                if(self.leftDoors):
                    self.ui.leftDoorsStatus.setPlainText("Open")  
                    self.ui.leftDoorsStatus.setStyleSheet(u"background-color: rgb(124,252,0);")   
                      
                if(self.rightDoors):
                    self.ui.rightDoorsStatus.setPlainText("Open")
                    self.ui.rightDoorsStatus.setStyleSheet(u"background-color: rgb(124,252,0);")
                    self.openedr=True 
            if(not self.leftDoors):
                self.ui.leftDoorsStatus.setPlainText("Closed")  
                self.ui.leftDoorsStatus.setStyleSheet(u"background-color: rgb(255,255,255);")    
            if(not self.rightDoors):
                self.ui.rightDoorsStatus.setPlainText("Closed")
                self.ui.rightDoorsStatus.setStyleSheet(u"background-color: rgb(255,255,255);")
            

    #checkVel: Used in Auto mode to see if doors can be opened
    def checkVel(self):
        if(self.actualSpeed==0):
            self.waitTimer.stop()
            self.upcomingStation=False
            self.ui.stationUpcoming.setChecked(False)
            self.openDoors()
            

    #openDoors: Used in Auto mode to open doors
    def openDoors(self):
            #opening the doors
        if(self.leftDoorsOpen):
            self.ui.leftDoorsStatus.setPlainText("Open")  
            self.ui.leftDoorsStatus.setStyleSheet(u"background-color: rgb(124,252,0);")     
        if(self.rightDoorsOpen):
            self.ui.rightDoorsStatus.setPlainText("Open")
            self.ui.rightDoorsStatus.setStyleSheet(u"background-color: rgb(124,252,0);")  
            
        self.waitForDisembark()

    #waitForDisembark: Used in Auto mode to close doors
    def waitForDisembark(self):
            #waiting for passengers to disembark
            self.waitTimer2 = QTimer()
            self.waitTimer2.timeout.connect(self.closeDoors)
            self.waitTimer2.start(4000)
            #where you would send out a signal to close doors

    #closeDoors: Used in Auto mode to close doors and keep going
    def closeDoors(self):
        self.waitTimer2.stop()
        print("Done with disembarking.")
        self.ui.stationUpcoming.setChecked(False)
        self.upcomingStation = False
        self.ui.rightDoorsStatus.setPlainText("Closed")
        self.ui.leftDoorsStatus.setPlainText("Closed")
        self.ui.leftDoorsStatus.setStyleSheet(u"background-color: rgb(255,255,255);")
        self.ui.rightDoorsStatus.setStyleSheet(u"background-color: rgb(255,255,255);")
        self.leftDoorsOpen = False
        self.rightDoorsOpen = False
        self.commandedSpeed = self.previousCommanded
        self.alreadyWaiting = False
        self.serviceBrake = False
        print("upcomingStation flag is" + str(self.upcomingStation))


    def onTemperatureChange(self):
        self.temperature = int(self.ui.temperature.value())
        print("Temp is " + str(self.temperature))
        self.ui.textBrowser_12.setPlainText(str(self.temperature))
        self.displayUpdate()

    def onExtLightsChanged(self):
        self.ui.exteriorLights_2.setChecked(self.ui.exteriorLights.checkState())
        self.displayUpdate()

    def onIntLightsChanged(self):
        self.ui.interiorLights_2.setChecked(self.ui.interiorLights.checkState())
        self.displayUpdate()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())