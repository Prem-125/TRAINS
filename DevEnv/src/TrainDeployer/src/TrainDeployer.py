#from TrainControllerSW.src.TrainControllerSW import TrainController
from TrainModel.src.TrainModelMain import MainWindow as TrainModel
from signals import signals


class TrainDeployer:
    
    def __init__(self):
        self.number_of_trains = 0 
        self.trains = []
        self.trains.append(None)
        signals.TC_signal.connect(self.SendTC)
        signals.Beacon_signal.connect(self.SendBeacon)
        signals.train_creation.connect(self.CreateTrains)
        signals.time_signal.connect(self.PropogateTime)
        #self.CreateTrains(1, 2, 3, True)
        #self.CreateTrains(3, 2, 1, False)

        
        """
        self.CreateController(3, 2, 1)
        self.CreateController(4,3,3)

        print("initialized")
        print(self.controllers[0].SR.authority)
        print(self.controllers[0].train_ID)
        print(self.number_of_trains)
        """
    
    #if soft_or_hard is true, it is software, if false, it is hard
    def SendTC(self,TC, TrainID):
        self.trains[TrainID].set_track_circuit(TC)

    def SendBeacon(self,Beacon, TrainID):
        self.trains[TrainID].set_beacon(TC)

    def PropogateTime(self,time):
        for i in range 1 to self.number_of_trains:
            self.trains[i].set_time(time)


    def CreateTrains(self,line, id):
        if(id == 2):
            self.trains.append(TrainModel(0, 0, 0, False, line, id))
        else:
            self.trains.append(TrainModel(0, 0, 0, True, line, id))
        self.trains[id].show()
        self.number_of_trains = self.number_of_trains + 1

    ##console makes a bunch of instances of stephen's train model class, stephen's train model class has an associated instance of the traincontroller class.
    ##stephen's constructor will take in a boolean whether to make it a hardware or software controller