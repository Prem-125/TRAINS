from TrainControllerSW.src.TrainControllerSW import TrainController
#from TrainControllerSW import TrainController


class TCSWConsole:
    
    def __init__(self):
        self.number_of_trains = 0 
        self.controllers = []
        self.CreateController(3, 2, 1)
        self.CreateController(4,3,3)

        print("initialized")
        print(self.controllers[0].SR.authority)
        print(self.controllers[0].train_ID)
        print(self.number_of_trains)

    

    def CreateController(self, commanded_speed, current_speed, authority):
        temp_controller_pointer = TrainController(commanded_speed, current_speed, authority, len(self.controllers))
        self.controllers.append(temp_controller_pointer)
        
        print("appended")
        self.number_of_trains += 1

    ##console makes a bunch of instances of stephen's train model class, stephen's train model class has an associated instance of the traincontroller class.
    ##stephen's constructor will take in a boolean whether to make it a hardware or software controller