import sys, time
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, QTimer
from TrainControllerSW.src.UI import Ui_TrainControllerSW
from simple_pid import PID
from TrainControllerSW.src.PIDBackup import PID as backupPID




############################################# START NEW CODE
class TrainController:
    def __init__(self, TrainModel, commanded_speed = 0.0, current_speed = 0.0, authority = 0.0, TrainID = 0.0):
        
        self.TrainModel = TrainModel

        #setting important variables
        self.train_ID = TrainID
        self.is_auto = True
        self.upcoming_station = False
        
        #Station Variables
        self.atDestination = False
        self.station = ""
        self.left_doors_at_dest = False
        self.right_doors_at_dest = False

        #Failures
        self.any_failure = False
        self.engine_failure = False
        self.brake_failure = False
        self.signal_pickup_failure = False
        self.passenger_brake_detected = False

        #Auxilliary Variables
        self.left_doors = False
        self.right_doors = False
        self.interior_lights = False
        self.exterior_lights = False
        self.announcement = ""

        #sending vital info to SpeedRegulator
        self.SR = SpeedRegulator(self, commanded_speed, current_speed, authority, self.train_ID)
        self.SR.commanded_speed = commanded_speed
        self.SR.current_speed = current_speed
        self.SR.authority = authority
        self.SR.setpoint_speed = 0.0
        self.SR.service_brake = False
        self.SR.emergency_brake = False

        #UI Stuff
        self.UI = MainWindow(self)
        self.UI.show()

        #other variables
        self.stationArray = ("Shadyside","Herron Ave","Swissville","Penn Station","Steel Plaza","First Ave","Station Square","South Hills Junction", 
                            "Pioneer","Edgebrook","Whited","South Bank","Central","Inglewood","Overbrook","Glenburry","Dormont","Mt Lebanon", "Poplar","Castle Shannon")


        self.DisplayUpdate()


    #COMMUNICATING WITH CORRESPONDING TRAIN MODEL
    def SendServiceBrakeOn(self):
        self.TrainModel.s_brake_on()
    
    def SendServiceBrakeOff(self):
        self.TrainModel.s_brake_off()

    def SendEmergencyBrakeOn(self):
        self.TrainModel.emergency_brake()

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
            self.signal_pickup_failure = True
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
        self.right_doors_at_dest = (BeaconInt >> 1)&1
        self.right_doors_at_dest = (BeaconInt >> 2)&1
        self.exterior_lights = (BeaconInt >> 3)&1
        self.station = self.stationArray[((BeaconInt >> 4) & 31)]
        self.BuildAnnouncement()
        self.HandleExteriorLights()

        if(self.is_auto):
            self.AuthorityHandler()
        self.DisplayUpdate()
        #print("Beacon Decoded!")

    def BuildAnnouncement(self):
        if(self.upcoming_station):
            self.announcement = str("Arriving at " + self.station + " Station.")
        if(self.left_doors_at_dest and self.right_doors_at_dest):
                self.announcement += " The doors will open on the left and right.\n"
        elif(self.left_doors_at_dest):
            self.announcement += " The doors will open on the left.\n"
        elif(self.right_doors_at_dest):
                self.announcement += " The doors will open on the right.\n"
        else:
            self.announcement += ""
        
    def DetectBrakeFailure(self):
        if(self.SR.service_brake and (self.SR.current_speed >= self.SR.previous_speed)):
            self.brake_failure = True
            self.UI.textBrowser_14.setStyleSheet(u"background-color: rgb(255, 0, 0);")
            self.VitalFault()

    def set_passenger_brake(self):
        self.passenger_brake_detected = True
        self.UI.textBrowser_16.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.VitalFault()

    def VitalFault(self):
        self.any_failure = True
        print("********************************************************* VITAL FAULT DETECTED *********************************************************")
        self.set_emergency_brake(True)

    def toggleLeftDoors(self):
        self.left_doors = not(self.left_doors)
        if(self.left_doors):
            self.TrainModel.open_left_doors()
        else:
            self.TrainModel.close_left_doors()
           
    def toggleRightDoors(self):
        self.right_doors = not(self.right_doors)
        if(self.right_doors):
            self.TrainModel.open_right_doors()
        else:
            self.TrainModel.close_right_doors()
    
    def toggleInteriorLights(self):
        self.interior_lights = not(self.interior_lights)
        print("Interior Lights: " + str(self.interior_lights))
        if(self.interior_lights):
            self.TrainModel.c_lights_on()
        else:
            self.TrainModel.c_lights_off()

    def HandleExteriorLights(self):
        if(self.exterior_lights):
            if(self.ui.exteriorLights.isChecked() == False):
                self.ui.exteriorLights.setChecked(True)
            print("Should turn exterior lights on")
            #self.TrainModel.t_lights_on()
            self.DisplayUpdate()
        else:
            if(self.ui.exteriorLights.isChecked() == True):
                self.ui.exteriorLights.setChecked(False)
            print("Shoudl turn exterior Lights off")
            #self.TrainModel.t_lights_off()
            self.DisplayUpdate()

    def toggleExteriorLights(self):
        self.exterior_lights = not(self.exterior_lights)
        print("Exterior Lights: " + str(self.exterior_lights))
        if(self.exterior_lights):
            self.TrainModel.t_lights_on()
        else:
            self.TrainModel.t_lights_off()

    def set_commanded_speed(self, commanded_speed):
        self.SR.commanded_speed = commanded_speed
        if(self.SR.setpoint_speed > self.SR.commanded_speed):
            self.SR.setpoint_speed = self.SR.commanded_speed
    
    def set_current_speed(self, current_speed):
        #main loop stuff
        self.SR.pidLoop()
        self.SR.backupPIDLoop()
        
        self.SR.previous_previous_speed = self.SR.previous_speed
        self.SR.previous_speed = self.SR.current_speed
        self.SR.current_speed = current_speed

        self.DetectBrakeFailure()
        
        #If we are approaching a station
        if(self.upcoming_station and self.SR.current_speed == 0):
            
            #Having the car start going again
            self.upcoming_station = False
            if(self.SR.authority != 0):
                self.set_service_brake(False)

            #If you arrive at your destination station, open the corresponding doors 
            if(self.SR.authority == 0):
                self.atDestination = True

                #Opening Left Doors in auto mode
                if(self.left_doors_at_dest and self.is_auto):
                    if(self.left_doors):
                         pass
                    else:
                        self.toggleLeftDoors()

                #Opening Right Doors in auto mode
                if(self.right_doors_at_dest and self.is_auto):
                    if(self.right_doors):
                         pass
                    else:
                        self.toggleRightDoors()

    def set_authority(self, authority):
        if(authority == 0):
            self.AuthorityHandler()
        else:
            self.set_service_brake(False)
        self.SR.authority = authority

    def AuthorityHandler(self):

        if(self.SR.authority==0 and self.upcoming_station):
            self.set_Service_brake(True)
            self.UI.Announce(self.announcement)

        elif(self.SR.authority == 0 or self.upcoming_station):
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
        return self.SR.get_power()

    #SPEED REGULATOR BUTTONS
    


class SpeedRegulator():

    def __init__(self, TrainController, commanded_speed = 0, current_speed = 0, authority = 0, train_ID = 0):
        self.commanded_speed = commanded_speed
        self.previous_previous_speed = 0.0
        self.previous_speed = 0.0 
        self.current_speed = current_speed
        self.authority = authority
        self.setpoint_speed = 0.0
        self.service_brake = False
        self.emergency_brake = False
        self.train_ID = train_ID
        self.TrainController = TrainController


        #variables for main PID loop
        self.kp = 1000.0
        self.ki = 1000.0
        self.power = 0.0
        self.previous_power = 0.0
        self.pid = PID(self.kp, self.ki, 0)
        self.pid.output_limits = (0, 120000)

        #variables for backup PID loop;
        self.power_backup = 0
        self.previous_power_backup = 0.0
        self.backupPID = PID(self.kp, self.ki, 0)
        self.backupPID.output_limits = (0, 120000)
        ##self.backupPID = backupPID.PID(self.kp, self.ki, 1)

        






    #pidLoop: used to calculate power
    def pidLoop(self):

        print("Main called. Main power is: " + str(self.power))

        #If in Auto Mode, go off the commanded speed
        if(self.TrainController.is_auto and ((not self.service_brake ) and (not self.emergency_brake))):

            #Closing the doors if we are leaving a destination
            if(self.TrainController.atDestination):
                if(self.TrainController.right_doors):
                    self.TrainController.toggleRightDoors
                if(self.TrainController.left_doors):
                    self.TrainController.toggleLeftDoors
                self.atDestination = False

            #updating setpoint
            self.pid.setpoint = self.commanded_speed
            self.previous_power = self.power
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

        #pidLoop: used to calculate power
    
    #backupPID: used to backup our process
    def backupPIDLoop(self):

        print("Backup called. Backup power is: " + str(self.power_backup))
        #If in Auto Mode, go off the commanded speed
        if(self.TrainController.is_auto and ((not self.service_brake ) and (not self.emergency_brake))):
            #updating setpoint
            self.backupPID.setpoint = self.commanded_speed
            
            #updating power variables
            self.previous_power_backup = self.power_backup
            self.power_backup = self.pid(self.current_speed, dt = 1)
            #Doing the power math
            ##self.backupPID.SetPoint = self.commanded_speed
            ##3self.power_backup = max(min( int(self.backupPID.output), 120000 ),0)
            
        #If in Manual Mode, go off the setpoint speed
        elif(not(self.setpoint_speed == 0) and not self.service_brake and not self.emergency_brake):
            self.pid.setpoint = self.setpoint_speed
            self.power_backup = self.pid(self.current_speed, dt = 1)
            ##self.power_backup = self.backupPID.output

        #If either brake is active, power is 0
        else:
            self.pid.setpoint=0
            self.power_backup = 0

        #Updating the display
        self.TrainController.DisplayUpdate()

        # send power here
        ##print(self.power)
        ##print("Got to end of pidLoop:")
        ##print("Power:" + str(self.power))
    
    def get_power(self):
        if(self.power == 0):
            return self.power
        elif(not(self.power == 0 or self.power_backup == 0)):
            if(self.power / self.power_backup > 2):
                print("TOO MUCH POWER DIFFERENCE")
                return 0
            else:
                return self.power
        else:
            return self.power
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
        if(self.setpoint_speed+1 <= self.commanded_speed):
            self.setpoint_speed = self.setpoint_speed + 1
        self.TrainController.DisplayUpdate()

    def DecreaseSetpoint(self):
        if(self.setpoint_speed > 0):
            self.setpoint_speed = self.setpoint_speed - 1
        self.TrainController.DisplayUpdate()

    def DetectEngineFailure(self):
        if(self.current_speed == 666):
            self.engine_failure = True
            self.UI.textBrowser_13.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        

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
        self.ui.trainNumber.setAcceptRichText(True)
        self.Text1 = "<p style=\"font-size:20px\">"
        self.Text2 = "</p>"
        self.ui.trainNumber.setText(self.Text1 + "<b>" + "Train ID: " + str(self.TrainController.train_ID) + "</b>" + self.Text2)
        self.ui.speedDownButton.clicked.connect(self.TrainController.SR.DecreaseSetpoint)
        self.ui.speedUpButton.clicked.connect(self.TrainController.SR.IncreaseSetpoint)
        self.ui.automaticMode.toggled.connect(self.TrainController.toggle_is_auto)
        self.ui.updatePID.clicked.connect(self.send_kp_ki)
        self.ui.leftDoors.stateChanged.connect(self.TrainController.toggleLeftDoors)
        self.ui.rightDoors.stateChanged.connect(self.TrainController.toggleRightDoors)
        self.ui.interiorLights.stateChanged.connect(self.TrainController.toggleInteriorLights)
        self.ui.exteriorLights.stateChanged.connect(self.TrainController.toggleExteriorLights)
        

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
        self.ui.upcomingStation.setPlainText(self.TrainController.station)
  

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

    def Announce(self, announceString):
        self.announcementDisplay.setPlainText(announceString)
    
    def send_kp_ki(self):
        self.TrainController.SR.pid.Ki = float(self.ui.kiInput.toPlainText())
        self.TrainController.SR.pid.Kp = float(self.ui.kpInput.toPlainText())
        self.TrainController.set_kp_ki(float(self.ui.kpInput.toPlainText()), float(self.ui.kiInput.toPlainText()))
        #print("Sent Kp: " + str(float(self.ui.kpInput.toPlainText())) + "Sent Ki: " + str(float(self.ui.kiInput.toPlainText())))




if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

