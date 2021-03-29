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