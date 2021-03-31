#from TrainControllerSW.src.TrainControllerSW import TrainController
from TrainModel.src.TrainModelMain import MainWindow as TrainModel
#from TrainControllerSW import TrainController


class TrainDeployer:
    
    def __init__(self):
        self.number_of_trains = 0 
        self.trains = []
        #self.CreateTrains(1, 2, 3, True)
        self.CreateTrains(3, 2, 1, True)
        
        """
        self.CreateController(3, 2, 1)
        self.CreateController(4,3,3)

        print("initialized")
        print(self.controllers[0].SR.authority)
        print(self.controllers[0].train_ID)
        print(self.number_of_trains)
        """
    
    #if soft_or_hard is true, it is software, if false, it is hard
    def CreateTrains(self, commanded_speed, current_speed, authority, soft_or_hard):
        self.trains.append(TrainModel(commanded_speed, current_speed, authority, soft_or_hard, len(self.trains)))
        self.trains[len(self.trains)-1].show()
        self.number_of_trains = self.number_of_trains + 1


    """
    def CreateController(self, commanded_speed, current_speed, authority):
        temp_controller_pointer = TrainController(commanded_speed, current_speed, authority, len(self.controllers))
        self.controllers.append(temp_controller_pointer)
        
        print("appended")
        self.number_of_trains += 1
    """

    ##console makes a bunch of instances of stephen's train model class, stephen's train model class has an associated instance of the traincontroller class.
    ##stephen's constructor will take in a boolean whether to make it a hardware or software controller