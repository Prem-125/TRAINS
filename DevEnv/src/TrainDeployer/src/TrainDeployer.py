#from TrainControllerSW.src.TrainControllerSW import TrainController
from TrainModel.src.TrainModelMain import MainWindow as TrainModel
from signals import signals


class TrainDeployer:
    
    def __init__(self):
        self.number_of_trains = 0 
        self.trains = []
        self.trains.append(None)
        
        #self.CreateTrains("Red", 1)
        #self.CreateTrains(3, 2, 1, True)

        
        signals.TC_signal.connect(self.SendTC)
        signals.Beacon_signal.connect(self.SendBeacon)
        signals.train_creation.connect(self.CreateTrains)
        signals.time_signal.connect(self.PropogateTime)
        #here is the signals i need connor to pass me when i send him whoch train is now on a new block
        signals.new_block.connect(self.sendBlockInfo)
        signals.num_passengers_changed.connect(self.change_passengers)
        # self.CreateTrains(1, 2, 3, True)
        # self.CreateTrains(3, 2, 1, False)
        print("fick")

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




 

    def sendBlockInfo(self, blockNum, blockLen, blockSlope, trainID):
       # print("Deployer Block Num is :" + str(blockNum))
      #  print("Deployer Block Len is :" + str(blockLen))
      #  print("Deployer Block Id is :" + str(trainID))
       # print("Deployer Block Slope is :" + str(blockSlope))

        self.trains[trainID].set_block_info(blockNum, blockLen, blockSlope)

    def change_passengers(self, delta, trainID):
        self.trains[trainID].change_passengers(delta)




    """
    def CreateController(self, commanded_speed, current_speed, authority):
        temp_controller_pointer = TrainController(commanded_speed, current_speed, authority, len(self.controllers))
        self.controllers.append(temp_controller_pointer)
        
        print("appended")
        self.number_of_trains += 1
    """

    def SendTC(self,TC, TrainID):
        self.trains[TrainID].set_track_circuit(TC)

    def SendBeacon(self,Beacon, TrainID):
        self.trains[TrainID].set_beacon(Beacon)

    def PropogateTime(self,time):
        for i in range(1 , self.number_of_trains):
            self.trains[i].set_time(time)


    def CreateTrains(self,line, id):
        if(id == 1):
            #self.trains.insert(id, TrainModel(0, 0, 0, False, line, id)
            self.trains.insert(id,TrainModel(0, 0, 0, False, line, id))
        else:
            #self.trains.insert(id, TrainModel(0, 0, 0, True, line, id )
            #self.trains[id] = TrainModel(0, 0, 0, True, line, id)
            self.trains.insert(id,TrainModel(15, 0, 0, True, line, id))
        print(len(self.trains))
        self.trains[id].show()
        self.number_of_trains = self.number_of_trains + 1


    ##console makes a bunch of instances of stephen's train model class, stephen's train model class has an associated instance of the traincontroller class.
    ##stephen's constructor will take in a boolean whether to make it a hardware or software controller