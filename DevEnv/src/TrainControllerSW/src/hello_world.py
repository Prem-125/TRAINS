import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from UI import Ui_TrainControllerSW
from simple_pid import PID

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_TrainControllerSW()
        self.ui.setupUi(self)


        #automatic mode stuff
        self.autoMode = True

        #commanded speed stuff
        self.setPointSpeed = 125
        self.ui.setPointSpeedVal.display(self.setPointSpeed)
        self.ui.speedUpButton.clicked.connect(self.increaseSetPoint)
        self.ui.speedDownButton.clicked.connect(self.decreaseSetPoint)

        #service brake stuff
        self.ui.serviceBrake.clicked.connect(self.serviceBrakeActivated)

        #encoded Track Circuit stuff
        self.actualSpeed = 0
        self.commandedSpeed = 0
        self.authority = 0
        self.encodedTC = 0
        self.ui.updateTCFake.clicked.connect(self.onUpdateTCFake)
        self.power = 0

        #passenger brake fake stuff
        self.ui.causePassenger.clicked.connect(self.passengerBrakeActivated)

        #actual speed fake stuff
        self.ui.updateActualFake.clicked.connect(self.onUpdateActualFake)

        #beacon stuff
        self.ui.updateBeaconFake.clicked.connect(self.onUpdateBeaconFake)
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
        self.pid = PID(kp, ki, 0)




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
        if(self.upcomingStation):
            self.ui.upcomingStation.setStyleSheet(u"background-color: rgb(124,252,0);")
        else:
            self.ui.upcomingStation.setStyleSheet(u"background-color: rgb(255,255,255);")
        

    def serviceBrakeActivated(self):
        print("Service Brake Activated")
        self.setPointSpeed=0
        self.displayUpdate()

    def passengerBrakeActivated(self):
        print("Passenger Brake Activated!")
        self.ui.textBrowser_16.setStyleSheet(u"background-color: rgb(255, 0, 0);")

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
        self.actualSpeed = float(self.ui.actualSpeed.toPlainText())
        self.displayUpdate()



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

    def onUpdateKpKi(self):
        pid.Ki = toPlainText(self.ui.kiInput)
        pid.Kp = toPlainText(self.ui.kpInput)

    
    def checkFailures(self):
        ...

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

    def pidLoop(self):

        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())