import unittest
import main.py

class TestControllerValues(unittest.TestCase):

    def test_authority(self):
        self.ui.CTCBlockInput.text = "1"
        self.ui.AuthorityInput.text = "1"
        self.assertEqual(authority[0], 1)
    
    def test_sugspeed_in(self):
        self.ui.CTCBlockInput.text = "1"
        self.ui.SugSpeedInput.text = "10"
        self.assertEqual(suggestedSpeed[0], 10)
    
    def test_commanded_authority_zero(self):
        self.authority[1] = 0
        self.calcCommandedSpeed()
        self.assertEqual(self.commandedSpeed[1], 0)

    def test_com_speed(self):
        self.suggestedSpeed = [0,0,20,40,0,0,0,0,25,0,0,0,0,0,0]
        self.CalcCommandedSpeed()
        for x in range(15):
            self.assertEqual(self.commandedSpeed[x], int(float(self.suggestedSpeed[x]) * 0.621371))

    def test_occupancy_string(self):
        self.occupancy = [False,True,False,True,False,True,False,True,False,True,False,True,False,True,False]
        self.getTrackOccString()
        self.assertEqual(self.trackOccString, "010101010101010")

    def test_switch(self):
        self.occupancy = [False,False,False,False,True,True,False,False,False,False,False,False,False,False,False]
        self.ControlSwitch()
        self.assertFalse(self.switchState)

if __name__ == '__main__':
    unittest.main()