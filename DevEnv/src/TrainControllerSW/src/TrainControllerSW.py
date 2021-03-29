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

        #sending vital info to SpeedRegulator
        self.SR = SpeedRegulator(self, commanded_speed, current_speed, authority, self.train_ID)
        self.SR.commanded_speed = commanded_speed
        self.SR.current_speed = current_speed
        self.SR.authority = authority
        self.SR.setpoint_speed = 0.0
        self.SR.service_brake = False
        self.SR.emergency_brake = False
        self.SR.kp = 0
        self.SR.ki = 0
        self.TrainModelRef = TrainModel

        #UI Stuff
        self.UI = MainWindow(self)
        self.UI.show()

        #all my connections


    #communicating with train model
    def sendServiceBrake(self):
        self.TrainModelRef.s_brake_on()
    
    #SPEED REGULATOR SETTERS
    def set_commanded_speed(self, commanded_speed):
        self.SR.commanded_speed = commanded_speed
    
    def set_current_speed(self, current_speed):
        self.SR.current_speed = current_speed
    
    def set_authority(self, authority):
        self.SR.authority = authority

    def set_setpoint_speed(self, setpoint_speed):
        self.SR.setpoint_speed = setpoint_speed
    
    def set_service_brake(self, s_brake):
        self.SR.service_brake = s_brake
    
    def set_emergency_brake(self, e_brake):
        self.SR.emergency_brake = e_brake

    def set_kp_ki(self, kp, ki):
        self.SR.kp = kp
        self.SR.ki = ki

    #SPEED REGULATOR GETTERS
    def get_power(self):
        return self.SR.power


class SpeedRegulator():

    def __init__(self, TrainController, commanded_speed = 0, current_speed = 0, authority = 0, train_ID = 0):
        self.commanded_speed = commanded_speed
        self.current_speed = current_speed
        self.authority = authority
        self.setpoint_speed = 0.0
        self.service_brake = False
        self.emergency_brake = False
        self.kp = 0.0
        self.ki = 0.0
        self.power = 0.0
        self.train_ID = train_ID
        self.TrainController = TrainController
        print("SpeedRegulator")

        #setting up the PID Loop
        self.pid = PID(self.kp, self.ki, 0)
        self.pid.output_limits = (0, 120000)
        self.pidTimer = QTimer()
        self.pidTimer.timeout.connect(self.pidLoop(TrainController))
        self.pidTimer.start(1000)
        print("Created the timer")


    #pidLoop: used to calculate power
    def pidLoop(self, TrainController):
        print("In PID")
        if(TrainController.is_auto and ((not self.service_brake ) and ( not self.emergency_brake))):
            self.pid.setpoint = self.commanded_speed
            self.power = self.pid(self.current_speed, dt = 1)
        elif(not(self.setpoint_speed == 0) and not self.service_brake and not self.emergency_brake):
            self.pid.setpoint = self.setpoint_speed
            self.power = self.pid(self.current_speed, dt = 1)
        else:
            self.pid.setpoint=0
            self.power= 0
        # send power here
        print(self.power)
        print("Got to end of pidLoop:")

    def get_power(self):
        print(self.power)

    def OnSBrakeOn(self):
        self.service_brake = True
        #DONE: emit service brake
        self.TrainController.sendServiceBrake()
        print("Train ID: " + str(self.train_ID) + "Service Brake: " + str(self.service_brake))
    
    def OnSBrakeOff(self):
        self.service_brake = False
        #TODO: emit service brake
        print("Service Brake: " + str(self.service_brake))
        
        
    def OnEBrakeOn(self):
        self.emergency_brake = True
        #TODO: emit service brake
        print("Emergency Brake: " + str(self.emergency_brake))

    
    



class MainWindow(QMainWindow):
    def __init__(self, TrainController):
        super(MainWindow, self).__init__()
        self.ui = Ui_TrainControllerSW()
        self.ui.setupUi(self)
        self.ui.serviceBrake.pressed.connect(TrainController.SR.OnSBrakeOn)
        self.ui.serviceBrake.released.connect(TrainController.SR.OnSBrakeOff)
        self.ui.emergencyBrake.pressed.connect(TrainController.SR.OnEBrakeOn)
        self.ui.trainNumber.setPlainText(str(TrainController.train_ID))
        #self.ui.emergencyBrake.pressed.connect(TrainController.SR.IncreaseSetpoint)
        #self.ui.D.pressed.connect(TrainController.SR.DecreaseSetpoint)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

