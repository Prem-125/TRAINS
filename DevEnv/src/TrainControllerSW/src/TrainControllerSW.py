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
        TC = TrainController()



############################################# START NEW CODE
class TrainController:
    def __init__(self, commanded_speed = 0.0, current_speed = 0.0, authority = 0.0):
        print("TrainController")
        self.is_auto = True
        #Vital Info To Speed Regulator
                        #SpeedRegulator.__init__(self)
        self.SR = SpeedRegulator(self)
        self.SR.commanded_speed = commanded_speed
        self.SR.current_speed = current_speed
        self.SR.authority = authority
        self.SR.setpoint_speed = 0.0
        self.SR.service_brake = False
        self.SR.emergency_brake = False
        self.SR.kp = 0
        self.SR.ki = 0


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


class SpeedRegulator(TrainController):

    def __init__(self, TrainController, commanded_speed = 0, current_speed = 0, authority = 0):
        self.commanded_speed = commanded_speed
        self.current_speed = current_speed
        self.authority = authority
        self.setpoint_speed = 0.0
        self.service_brake = False
        self.emergency_brake = False
        self.kp = 0.0
        self.ki = 0.0
        self.power = 0.0
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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

