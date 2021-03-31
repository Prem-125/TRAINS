import sys
import random 
import math 
import time 

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from UI import Ui_MainWindow
from Train import Train
from hello import MainWindow

import unittest 

class TestTrain(unittest.TestCase):
	def setUp(self):
		self.func = MainWindow()
	def test_power(self):
		self.func.set_power(4.2)
		self.assertEqual(self.func.newTrain.power, 4.2)
		self.assertEqual(self.func.newTrain.velocity, 2.1)
	
	def test_left_door(self):
		self.func.open_left_doors()
		self.assertTrue(self.func.newTrain.lDoorsOpen)
		self.func.close_left_doors()
		self.assertFalse(self.func.newTrain.lDoorsOpen)
	
	def test_right_door(self):
		self.func.open_right_doors()
		self.assertTrue(self.func.newTrain.rDoorsOpen)
		self.func.close_right_doors()
		self.assertFalse(self.func.newTrain.rDoorsOpen)

	def test_cabin_lights(self):
		self.func.c_lights_on()
		self.assertTrue(self.func.newTrain.cLightsOn)
		self.func.c_lights_off()
		self.assertFalse(self.func.newTrain.cLightsOn)

	def test_tunnel_lights(self):
		self.func.t_lights_on()
		self.assertTrue(self.func.newTrain.tLightsOn)
		self.func.t_lights_off()
		self.assertFalse(self.func.newTrain.cLightsOn)

	def test_e_brake(self):
		self.func.emergency_brake()
		self.assertTrue(self.func.newTrain.EmergencyBrake)
		self.assertEqual(self.func.newTrain.velocity, 0)
		self.func.emergency_brake()
		self.assertFalse(self.func.newTrain.EmergencyBrake)
		self.assertEqual(self.func.newTrain.velocity, 2.1)

	def test_s_brake(self):
		self.func.s_brake_on()
		self.assertTrue(self.func.newTrain.serviceBrake)
		self.assertEqual(self.func.newTrain.velocity, 0)
		self.func.s_brake_off()
		self.assertFalse(self.func.newTrain.serviceBrake)
		self.assertEqual(self.func.newTrain.velocity, 2.1)

	def test_engine_failure(self):
		self.func.engine1_failure()
		self.assertEqual(self.func.newTrian.engineFailure, 0)
		self.assertEqual(self.func.newTrain.velocity, 2.1)

	def test_c_failure(self)
		self.func.circuit_failure_on()
		self.assertTrue(self.func.newTrain.circuitFailure)
		self.func.circuit_failure_off()
		self.assertFalse(self.func.newTrain.circuitFailure)

	def test_brake_failure(self)
		self.func.brake_failure_on()
		self.assertTrue(self.func.newTrain.brakeFailure)
		self.func.brake_failure_off()
		self.assertFalse(self.func.newTrain.brakeFailure)
		
		

if __name__ == '__main__':
	unittest.main()
