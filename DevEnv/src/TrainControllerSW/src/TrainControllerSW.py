import sys, time
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, QTimer
from TrainControllerSW.src.UI import Ui_TrainControllerSW
from simple_pid import PID




############################################# START NEW CODE
class TrainController:
    def __init__(self, TrainModel, commanded_speed = 0.0, current_speed = 0.0, authority = 0.0, TrainID = 0.0):
        
        #setting important variables
        self.train_ID = TrainID
        self.is_auto = True
        self.upcoming_station = False
        
        self.atDestination = False
        self.station = "Undefined"

        #Auxilliary Variables
        self.leftDoors = False
        self.rightDoors = False
        self.InteriorLights = False

        #sending vital info to SpeedRegulator
        self.SR = SpeedRegulator(self, commanded_speed, current_speed, authority, self.train_ID)
        self.SR.commanded_speed = commanded_speed
        self.SR.current_speed = current_speed
        self.SR.authority = authority
        self.SR.setpoint_speed = 0.0
        self.SR.service_brake = False
        self.SR.emergency_brake = False


        self.TrainModelRef = TrainModel
        
        #UI Stuff
        self.UI = MainWindow(self)
        self.UI.show()


        #other variables
        self.stationArray = ("Shadyside","Herron Ave","Swissville","Penn Station","Steel Plaza","First Ave","Station Square","South Hills Junction", 
                            "Pioneer","Edgebrook","Whited","South Bank","Central","Inglewood","Overbrook","Glenburry","Dormont","Mt Lebanon", "Poplar","Castle Shannon")


        self.DisplayUpdate()

        #all my connections


    #COMMUNICATING WITH CORRESPONDING TRAIN MODEL
    def SendServiceBrakeOn(self):
        self.TrainModelRef.s_brake_on()
    
    def SendServiceBrakeOff(self):
        self.TrainModelRef.s_brake_off()

    def SendEmergencyBrakeOn(self):
        self.TrainModelRef.emergency_brake()

    def toggle_is_auto(self):
        self.is_auto = not(self.is_auto)

    #DisplayUpdate: used to update the UI
    def DisplayUpdate(self):
        self.UI.DisplayUpdate()

    def set_track_circuit(self, TrackInt):
        self.decodeTC(TrackInt)

    def decodeTC(self, TrackInt):
        tempCmdInt = TrackInt & 255
        tempCmdFloat = (TrackInt >> 8) & 15
        tempAuthInt = (TrackInt >> 12) & 255
        tempAuthFloat= (TrackInt >> 20) & 15
        tempCheckSum = (TrackInt >> 24) & 1023
        print("Temp commanded Int" + str(tempCmdInt))
        print("Temp commanded Float" + str(tempCmdFloat))
        if(tempCheckSum != tempCmdInt+ tempCmdFloat + tempAuthInt + tempAuthFloat):
            #print("Signal Pickup Failure")
            self.UI.textBrowser_15.setStyleSheet(u"background-color: rgb(255, 0, 0);")
            self.VitalFault()
        else:
            self.set_commanded_speed(tempCmdFloat/100 + tempCmdInt)
            self.set_authority(tempAuthFloat/100 + tempAuthInt)
        #print("Track Circuit Decoded!")

    def set_beacon(self, BeaconInt):
        self.DecodeBeacon(BeaconInt)
        
    def DecodeBeacon(self, BeaconInt):
        self.upcoming_station = (BeaconInt & 1)
        print(self.upcoming_station)
        self.left_doors_open = (BeaconInt >> 1)&1
        self.right_doors_open = (BeaconInt >> 2)&1
        self.exterior_lights_on = (BeaconInt >> 3)&1
        self.station = self.stationArray[((BeaconInt >> 4) & 31)]
        #self.buildAnnouncement()
        if(self.is_auto):
            self.AuthorityHandler()
            #self.onAnnouncement()
        self.DisplayUpdate()
        #print("Beacon Decoded!")

    def VitalFault(self):
        self.SR.OnEBrakeOn()

    def toggleLeftDoors(self):
        self.leftDoors = not(self.leftDoors)
        
    def toggleRightDoors(self):
        self.rightDoors = not(self.rightDoors)
        print(str(self.rightDoors))
    
    def toggleInteriorLights(self):
        self.interiorLights = not(self.interiorLights)
        print("Interior Lights: " + str(self.interiorLights))

    #SPEED REGULATOR SETTERS
    def set_commanded_speed(self, commanded_speed):
        self.SR.commanded_speed = commanded_speed
    
    def set_current_speed(self, current_speed):
        self.SR.pidLoop()
        self.SR.current_speed = current_speed
        if(self.upcoming_station and self.SR.current_speed == 0):
            
            #Having the car start going again
            self.upcoming_station = False
            if(self.SR.authority != 0):
                self.set_service_brake(False)

            #If you arrive at your destination station, open the corresponding doors until 
            if(self.SR.authority == 0):
                self.atDestination = True
                if(self.leftDoors):
                    print("TODO: Open Left Doors Here")
                    self.leftDoors = True
                    print("Left doors open")
                if(self.rightDoors):
                    self.rightDoors = True
                    print("TODO: Open Right Doors Here")
    
    def set_authority(self, authority):
        if(authority == 0):
            self.AuthorityHandler()
        else:
            self.set_service_brake(False)
        self.SR.authority = authority

    def AuthorityHandler(self):
        if(self.SR.authority == 0 or self.upcoming_station):
            #this is the equivalent of my station handler.
            self.set_service_brake(True)

        else:
            #when authority is false 
            #self.set_service_brake(False)
            ...

    def set_setpoint_speed(self, setpoint_speed):
        self.SR.setpoint_speed = setpoint_speed
    
    def set_service_brake(self, s_brake):
        if(s_brake):
            self.SR.OnSBrakeOn()
        else:
            self.SR.OnSBrakeOff()

    
    def set_emergency_brake(self, e_brake):
        self.SR.emergency_brake = e_brake

    def set_kp_ki(self, kp, ki):
        self.SR.kp = kp
        self.SR.ki = ki

    #SPEED REGULATOR GETTERS
    def get_power(self):
        return self.SR.power

    #SPEED REGULATOR BUTTONS
    


class SpeedRegulator():

    def __init__(self, TrainController, commanded_speed = 0, current_speed = 0, authority = 0, train_ID = 0):
        self.commanded_speed = commanded_speed
        self.current_speed = current_speed
        self.authority = authority
        self.setpoint_speed = 0.0
        self.service_brake = False
        self.emergency_brake = False
        self.kp = 1000.0
        self.ki = 1000.0
        self.power = 0.0
        self.train_ID = train_ID
        self.TrainController = TrainController


        #setting up the PID Loop
        self.pid = PID(self.kp, self.ki, 0)
        self.pid.output_limits = (0, 120000)



    #pidLoop: used to calculate power
    def pidLoop(self):

        #If in Auto Mode, go off the commanded speed
        if(self.TrainController.is_auto and ((not self.service_brake ) and ( not self.emergency_brake))):
            #Closing the doors if we are leaving a destination
            if(self.TrainController.atDestination):
                self.rightDoors = False
                self.leftDoors = False
                self.atDestination = False

            #Doing the power math
            self.pid.setpoint = self.commanded_speed
            self.power = self.pid(self.current_speed, dt = 1)
            
        #If in Manual Mode, go off the setpoint speed
        elif(not(self.setpoint_speed == 0) and not self.service_brake and not self.emergency_brake):
            self.pid.setpoint = self.setpoint_speed
            self.power = self.pid(self.current_speed, dt = 1)

        #If either brake is active, power is 0
        else:
            self.pid.setpoint=0
            self.power = 0

        #Updating the display
        self.TrainController.DisplayUpdate()

        # send power here
        ##print(self.power)
        ##print("Got to end of pidLoop:")
        ##print("Power:" + str(self.power))

    
    def get_power(self):
        print(self.power)
        ...
    
    def OnSBrakeOn(self):
        self.service_brake = True
        self.TrainController.SendServiceBrakeOn()
        self.TrainController.DisplayUpdate()

    def OnSBrakeOff(self):
        self.service_brake = False
        self.TrainController.SendServiceBrakeOff()
        self.TrainController.DisplayUpdate()
        
    def OnEBrakeOn(self):
        self.emergency_brake = True
        self.TrainController.SendEmergencyBrakeOn()
        self.TrainController.DisplayUpdate()
        #DONE: emit service brake
        #print("Emergency Brake: " + str(self.emergency_brake))

    def IncreaseSetpoint(self):
        if(self.setpoint_speed < self.commanded_speed):
            self.setpoint_speed = self.setpoint_speed + 1
        self.TrainController.DisplayUpdate()

    def DecreaseSetpoint(self):
        if(self.setpoint_speed > 0):
            self.setpoint_speed = self.setpoint_speed - 1
        self.TrainController.DisplayUpdate()
        

#MainWindow class - interfaces with TrainController UI
class MainWindow(QMainWindow):
    def __init__(self, TrainController):
        super(MainWindow, self).__init__()
        self.TrainController = TrainController
        self.ui = Ui_TrainControllerSW()
        self.ui.setupUi(self)

        #Button To Function Connections
        self.ui.serviceBrake.pressed.connect(self.TrainController.SR.OnSBrakeOn)
        self.ui.serviceBrake.released.connect(self.TrainController.SR.OnSBrakeOff)
        self.ui.emergencyBrake.pressed.connect(self.TrainController.SR.OnEBrakeOn)
        self.ui.trainNumber.setPlainText(str(self.TrainController.train_ID))
        self.ui.speedDownButton.clicked.connect(self.TrainController.SR.DecreaseSetpoint)
        self.ui.speedUpButton.clicked.connect(self.TrainController.SR.IncreaseSetpoint)
        self.ui.automaticMode.toggled.connect(self.TrainController.toggle_is_auto)
        self.ui.updatePID.clicked.connect(self.send_kp_ki)
        self.ui.leftDoors.stateChanged.connect(self.TrainController.toggleLeftDoors)
        self.ui.rightDoors.stateChanged.connect(self.TrainController.toggleRightDoors)
        self.ui.interiorLights.stateChanged.connect(self.TrainController.toggleInteriorLights)
        

        #self.pidTimer = QTimer()
        #self.pidTimer.timeout.connect(self.TrainController.SR.pidLoop)
        #self.pidTimer.start(1000)



        
    def DisplayUpdate(self):
        #Displaying Speeds
        self.ui.setPointSpeedVal.display(self.TrainController.SR.setpoint_speed * 2.23694)
        self.ui.commandedSpeedVal.display(self.TrainController.SR.commanded_speed * 2.23694)
        self.ui.authority.display(self.TrainController.SR.authority)
        self.ui.actualSpeedVal.display(self.TrainController.SR.current_speed * 2.23694)
        self.ui.power.display(self.TrainController.SR.power / 1000)
  

        if(self.TrainController.SR.service_brake):
            self.ui.textBrowser_9.setPlainText("S Brake Active")
            #self.ui.textBrowser_11.setPlainText("S Brake Active")
        else:
            self.ui.textBrowser_9.setPlainText("S Brake Inactive")
            #self.ui.textBrowser_11.setPlainText("S Brake Inactive")

        if(self.TrainController.SR.emergency_brake):
            self.ui.textBrowser_8.setPlainText("E Brake Active")
            #self.ui.textBrowser_10.setPlainText("E Brake Active")
        else:
            self.ui.textBrowser_8.setPlainText("E Brake Inactive")
            #self.ui.textBrowser_10.setPlainText("E Brake Inactive")

        #keeping door info up to date
        if(self.TrainController.is_auto):
            self.ui.leftDoors.setEnabled(False)
            self.ui.rightDoors.setEnabled(False)
        else:
            self.ui.leftDoors.setEnabled(True)
            self.ui.rightDoors.setEnabled(True)

    def send_kp_ki(self):
        self.TrainController.SR.pid.Ki = float(self.ui.kiInput.toPlainText())
        self.TrainController.SR.pid.Kp = float(self.ui.kpInput.toPlainText())
        self.TrainController.set_kp_ki(float(self.ui.kpInput.toPlainText()), float(self.ui.kiInput.toPlainText()))
        #print("Sent Kp: " + str(float(self.ui.kpInput.toPlainText())) + "Sent Ki: " + str(float(self.ui.kiInput.toPlainText())))
    #stephen cals TC.get power and TC.set track circuit and TC.set current speed and TC.set beacon

    #need set beacon, set track circuit functions for stephen to call and for us to decode
            #in here, make sure 0 authority = service brake and thus no power
    #add auto mode functionality
    #add things for KP and Ki


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

