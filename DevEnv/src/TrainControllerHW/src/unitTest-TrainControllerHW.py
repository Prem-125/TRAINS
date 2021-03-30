from UI import Ui_TrainModelInterface
from TrainControllerHW-GUI import MainWindow
import unittest
import sys


class TestTrainController(unittest.TestCase):
    def __init__(self):
    self.app = QApplication(sys.argv)

	self.unit = MainWindow()
	self.unit.show()
	sys.exit(self.app.exec_())

    def LightTest:
        unit.setEncodedB(27) # sets a beacon value that should turn on the Ext Lights
        self.unit.serialWrite()
        self.unit.serialRead()
        self.assertTrue(self.unit.ExtLightsOn)


    def EngineFailTest:
        self.unit.curSpeed = 666 # sets a speed value that should indicate an engine failure 
        self.unit.serialWrite()
        self.unit.serialRead()
        self.assertTrue(self.unit.EBrakePull)
         self.assertTrue(self.unit.power == 0)


    def TCFailTest:
        unit.setEncodedTC(327) # sets a track circut  value with a bad checksum  that should indicate an track circut failure 
        self.unit.serialWrite()
        self.unit.serialRead()
        self.assertTrue(self.unit.EBrakePull)
        self.assertTrue(self.unit.power == 0)



    def AuthTest:
        unit.setEncodedTC(23) # sets a track circut  indicating we have exceeded our authority  
        self.unit.serialWrite()
        self.unit.serialRead()
        self.assertTrue(self.unit.EBrakePull)
        self.assertTrue(self.unit.power == 0)

    def StationTest:
        unit.setEncodedB(27) # sets a beacon value Indicating an upcoming station
        self.unit.serialWrite()
        self.unit.serialRead()
        self.assertTrue(self.unit.sBrakePull)
        self.assertTrue(self.unit.power == 0)
        self.unit.curSpeed=0 # stops the train to test opening of doors 
        self.unit.serialWrite()
        self.unit.serialRead()
        self.assertTrue(self.unit.LDoorOpen and self.unit.RDoorOpen)
        
if __name__ == "__main__":
	tester = TestTrainController()
    tester.LightTest()
    tester.EngineFailTest()
    tester.TCFailTest()
    tester.AuthTest()
    tester.StationTest()