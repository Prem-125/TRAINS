import sys, time
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, QTimer
from TrainControllerSW.src.UI import Ui_TrainControllerSW
from simple_pid import PID
from TrainControllerSW.src.PIDBackup import PID as backupPID





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
        self.ad_length = 0
        self.current_ad=0

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


        self.advertisements = ("Advertisement: Tired of the arts? Consider Pitt COE!", "Advertisement: Another rainy day in Pittsburgh? Vitamin D supplements 30 percent off at Market.")
        self.DisplayUpdate()


    ###################### TRAIN MODEL INTERFACES ######################

    #TRAIN MODEL: SENDING TO
    def SendServiceBrakeOn(self):
        self.TrainModel.s_brake_on()
    
    def SendServiceBrakeOff(self):
        self.TrainModel.s_brake_off()

    def SendEmergencyBrakeOn(self):
        self.TrainModel.emergency_brake()

    #TRAIN MODEL : RECEIVING FROM
    def set_track_circuit(self, TrackInt):
        self.DecodeTC(TrackInt)

    def set_beacon(self, BeaconInt):
        self.DecodeBeacon(BeaconInt)

    def set_passenger_brake(self):
        self.passenger_brake_detected = True
        self.UI.ui.textBrowser_16.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.VitalFault()

    def set_current_speed(self, current_speed):
        self.SR.pidLoop()
        self.SR.backupPIDLoop()
        
        self.SR.previous_previous_speed = self.SR.previous_speed
        self.SR.previous_speed = self.SR.current_speed
        self.SR.current_speed = current_speed

        self.SR.DetectBrakeFailure()
        self.SR.DetectEngineFailure()
        
        #If we reach a station and our current speed is 0, open doors and all that jazz
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
                        self.toggle_left_doors()

                #Opening Right Doors in auto mode
                if(self.right_doors_at_dest and self.is_auto):
                    if(self.right_doors):
                         pass
                    else:
                        self.toggle_right_doors()
        else:
            self.SendAdvertisement()
    
    def set_commanded_speed(self, commanded_speed):
        self.SR.commanded_speed = commanded_speed
    
    #TRAIN MODEL : CALLABLE
    def get_power(self):
        return self.SR.get_power()
    

    ###################### CLASS FUNCTIONS ###################### 

    #toggle_is_auto: toggles between manual and auto mode
    def toggle_is_auto(self):
        self.is_auto = not(self.is_auto)

    #DisplayUpdate: used to update the UI
    def DisplayUpdate(self):
        self.UI.DisplayUpdate()

    #DecodeTC: used to decode track circuit received from train model
    def DecodeTC(self, TrackInt):
        print("Decoding TC")
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
            self.SR.VitalFault()
        else:
            self.set_commanded_speed(tempCmdFloat/100 + tempCmdInt)
            self.set_authority(tempAuthFloat/100 + tempAuthInt)
        #print("Track Circuit Decoded!")
       
    #DecodeBeacon: used to decode beacon from train model
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

    #BuildAnnouncement: used to build announcement upon receiving a beacon
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

    #SendAnnouncement: used to send announcement to train model and UI  
    def SendAnnouncement(self):
        self.UI.Announce(self.announcement)

    def SendAdvertisement(self):
        if(self.ad_length<100):
            self.ad_length += 1
            self.UI.Announce(self.advertisements[0])    
        elif(self.ad_length<200):
            self.ad_length += 1
            self.UI.Announce(self.advertisements[1])
        else:
            self.UI.Announce(self.advertisements[0])
            self.ad_length=0
        #print("In send advertisement")

    #Door/Lights Toggles
    def toggle_left_doors(self):
        self.left_doors = not(self.left_doors)
        if(self.left_doors):
            self.TrainModel.open_left_doors()
        else:
            self.TrainModel.close_left_doors()
           
    def toggle_right_doors(self):
        self.right_doors = not(self.right_doors)
        if(self.right_doors):
            self.TrainModel.open_right_doors()
        else:
            self.TrainModel.close_right_doors()
    
    #toggle_interior_lights: function for toggling interior lights based of checkmarks
    def toggle_interior_lights(self):
        self.interior_lights = not(self.interior_lights)
        print("Interior Lights: " + str(self.interior_lights))
        if(self.interior_lights):
            self.TrainModel.c_lights_on()
        else:
            self.TrainModel.c_lights_off()

    #toggle_exterior_lights: function for toggling exterior lights based of checkmarks
    def toggle_exterior_lights(self):
        self.exterior_lights = not(self.exterior_lights)
        print("Exterior Lights: " + str(self.exterior_lights))
        if(self.exterior_lights):
            self.TrainModel.t_lights_on()
        else:
            self.TrainModel.t_lights_off()

    #toggle_exterior_lights: function for keeping checks in UI in sync with beacon
    def HandleExteriorLights(self):
        if(self.exterior_lights):
            if(self.UI.ui.exteriorLights.isChecked() == False):
                self.UI.ui.exteriorLights.setChecked(True)
            self.DisplayUpdate()
        else:
            if(self.UI.ui.exteriorLights.isChecked() == True):
                self.UI.ui.exteriorLights.setChecked(False)
            self.DisplayUpdate()



    ###################### SPEED REGULATOR INTERFACES ######################

    def set_authority(self, authority):
        if(authority == 0):
            self.AuthorityHandler()
        else:
            self.AuthorityHandler()
            self.set_service_brake(False)
        self.SR.authority = authority

    def AuthorityHandler(self):
        

        if(self.SR.authority==0 and self.upcoming_station):
            self.set_service_brake(True)
            self.sendAnnouncement()
            print("both true in authoity handler")

        elif(self.SR.authority == 0 or self.upcoming_station):
            #this is the equivalent of my station handler.
            self.set_service_brake(True)
            print("one true in authority handler")

        else:
            self.SendAdvertisement()
            print("sending in authority handler")
                
                
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


    ###################### POWER STUFF ######################

    #pidLoop: used to calculate power
    def pidLoop(self):

        #print("Main called. Main power is: " + str(self.power))

        #If in Auto Mode, go off the commanded speed
        if(self.TrainController.is_auto and ((not self.service_brake ) and (not self.emergency_brake))):

            #Closing the doors if we are leaving a destination
            if(self.TrainController.atDestination):
                if(self.TrainController.right_doors):
                    self.TrainController.toggle_right_doors
                if(self.TrainController.left_doors):
                    self.TrainController.toggle_left_doors
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
    
    #backupPID: used to make PID Loop safety-critical
    def backupPIDLoop(self):

        #print("Backup called. Backup power is: " + str(self.power_backup))
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
    
    #get_power: makes sure PID loops are in tune, returns power
    def get_power(self):
        if(self.power == 0):
            return self.power
        elif(not(self.power == 0 or self.power_backup == 0)):
            if(self.power / self.power_backup > 2):
                print("TOO MUCH POWER DIFFERENCE")
                return 0
                self.Vital
            else:
                return self.power
        else:
            return self.power
            ...
    
    ###################### ON CLICK/CALL ACTIONS ACTIONS ######################
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

    def IncreaseSetpoint(self):
        if(self.setpoint_speed+1 <= self.commanded_speed):
            self.setpoint_speed = self.setpoint_speed + 1
        self.TrainController.DisplayUpdate()

    def DecreaseSetpoint(self):
        if(self.setpoint_speed > 0):
            self.setpoint_speed = self.setpoint_speed - 1
        self.TrainController.DisplayUpdate()

    ###################### FAILURE DETECTION ######################
    def DetectEngineFailure(self):
        if(self.current_speed == 666):
            self.engine_failure = True
            self.UI.textBrowser_13.setStyleSheet(u"background-color: rgb(255, 0, 0);")
            self.VitalFault()
            self.TrainController.TrainModel.engine_failure_on()

    def DetectBrakeFailure(self):
        if(self.service_brake and (self.current_speed >= self.previous_speed) and not(self.current_speed == 0)):
            self.brake_failure = True
            self.TrainController.UI.ui.textBrowser_14.setStyleSheet(u"background-color: rgb(255, 0, 0);")
            self.VitalFault()
            self.TrainController.TrainModel.brake_failure_on()
    
    def VitalFault(self):
        self.TrainController.any_failure = True
        print("********************************************************* VITAL FAULT DETECTED *********************************************************")
        self.OnEBrakeOn()

        
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
        self.ui.leftDoors.stateChanged.connect(self.TrainController.toggle_left_doors)
        self.ui.rightDoors.stateChanged.connect(self.TrainController.toggle_right_doors)
        self.ui.interiorLights.stateChanged.connect(self.TrainController.toggle_interior_lights)
        self.ui.exteriorLights.stateChanged.connect(self.TrainController.toggle_exterior_lights)
        

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
        self.ui.announcementDisplay.setPlainText(announceString)
    
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

