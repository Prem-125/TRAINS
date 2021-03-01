import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from UI import Ui_TrainControllerSW

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_TrainControllerSW()
        self.ui.setupUi(self)

        #commanded speed stuff
        self.setPointSpeed = 700
        self.ui.setPointSpeedVal.display(self.setPointSpeed)
        self.ui.speedUpButton.clicked.connect(self.increaseSetPoint)
        self.ui.speedDownButton.clicked.connect(self.decreaseSetPoint)

        #service brake stuff
        self.ui.serviceBrake.clicked.connect(self.serviceBrakeActivated)

        #encoded Track Circuit stuff
        self.commandedSpeed = 0
        self.authority = 0
        self.encodedTC = 0
        self.ui.updateFake.clicked.connect(self.onUpdateFake)




    def increaseSetPoint(self):
        self.setPointSpeed = self.setPointSpeed + 1
        print(self.setPointSpeed)
        self.displaySetPoint()

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

    def serviceBrakeActivated(self):
        print("Service Brake Activated")
        self.setPointSpeed=0
        self.displayUpdate()
        self.passengerBrakeError()

    def signalPickUpError(self):
        #encoded 64 bit integer
        #thinking 8 bits for speed integer part, 4 bits for speed float, 8 bits for authority, 4 bits for authority float, 13 bits for speed/authority checksum
        #add authority and speed together to get checksum
        ...

    def passengerBrakeError(self):
        self.ui.textBrowser_13.setStyleSheet(u"background-color: rgb(255, 0, 0);")

    def onUpdateFake(self):
        self.commandedSpeed = float(self.ui.inputCommanded.toPlainText())
        self.authority = float(self.ui.inputAuthority.toPlainText())
        self.actualSpeed = float(self.ui.actualSpeed.toPlainText())
        
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

    def decodeTC(self):
        tempCmdInt = self.encodedTC & 255
        tempCmdFloat = (self.encodedTC >> 8) & 15
        tempAuthInt = (self.encodedTC >> 12) & 255
        tempAuthFloat= (self.encodedTC >> 20) & 15
        tempCheckSum = (self.encodedTC >> 24) & 1023

        if(tempCheckSum != tempCmdInt+ tempCmdFloat + tempAuthInt + tempAuthFloat):
            print("Signal Pickup Failure")
            self.ui.textBrowser_15.setStyleSheet(u"background-color: rgb(255, 0, 0);")
            
        print("Temp" + str(tempCmdInt))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())