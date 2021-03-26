from TrainControllerSW import *
import unittest

class TestTrainController(unittest.TestCase):
	def setUp(self):
		self.func = TrainControllerSW()
	def test_power(self):
		self.func.set_commanded_speed(10)
		self.func.set_current_speed(1)
		self.assertTrue(self.func.calcPower() > 0)
		self.assertTrue(self.func.calcPower() <120000)
	def test_s_brake(self):
		self.func.set_s_brake(True)
		self.assertTrue(self.func.s_brake)
		self.func.set_s_brake(False)
		self.assertFalse(self.func.s_brake)
	def test_e_brake(self):
		self.func.set_e_brake(True)
		self.assertTrue(self.func.e_Brake)
		self.func.set_e_brake(False)
		self.assertFalse(self.func.e_brake)
	def test_signal_pickup(self):
		self.func.set_track_circuit(1111001010101010100100100)
		self.assertTrue(self.func.vitalFault)
	def test_beacon(self):
		self.func.set_beacon(111111111111111110000000)
		self.assertTrue(self.func.left_doors)
		self.assertTrue(self.func.right_doors)
		self.assertTrue(self.func.upcoming_station)
	def test_engine_failure(self):
		self.func.set_commanded_speed(666)
		self.assertTrue(self.func.vitalFault)
	def test_brake_failure(self):
		self.func.set_s_brake(True)
		self.func.set_current_speed(444)
		self.func.set_current_speed(555)
		self.assertTrue(self.func.vitalFault)
	def test_vital_fault(self):
		self.func.vitalFault()
		self.assertTrue(self.func.e_brake)

if __name__ == '__main__:'
	unittest.main()


