﻿# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_TrainControllerSW(object):
    def setupUi(self, TrainControllerSW):
        if not TrainControllerSW.objectName():
            TrainControllerSW.setObjectName(u"TrainControllerSW")
        TrainControllerSW.resize(1432, 685)
        self.emergencyBrake = QPushButton(TrainControllerSW)
        self.emergencyBrake.setObjectName(u"emergencyBrake")
        self.emergencyBrake.setGeometry(QRect(460, 550, 411, 111))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.emergencyBrake.setFont(font)
        self.emergencyBrake.setStyleSheet(u"background-color: rgb(170, 0, 0);")
        self.trainStatus = QWidget(TrainControllerSW)
        self.trainStatus.setObjectName(u"trainStatus")
        self.trainStatus.setGeometry(QRect(470, 30, 401, 341))
        self.rightDoors = QCheckBox(self.trainStatus)
        self.rightDoors.setObjectName(u"rightDoors")
        self.rightDoors.setGeometry(QRect(0, 30, 151, 31))
        font1 = QFont()
        font1.setPointSize(12)
        self.rightDoors.setFont(font1)
        self.rightDoors.setLayoutDirection(Qt.RightToLeft)
        self.leftDoors = QCheckBox(self.trainStatus)
        self.leftDoors.setObjectName(u"leftDoors")
        self.leftDoors.setGeometry(QRect(0, 0, 151, 31))
        self.leftDoors.setFont(font1)
        self.leftDoors.setLayoutDirection(Qt.RightToLeft)
        self.interiorLights = QCheckBox(self.trainStatus)
        self.interiorLights.setObjectName(u"interiorLights")
        self.interiorLights.setGeometry(QRect(0, 60, 151, 31))
        self.interiorLights.setFont(font1)
        self.interiorLights.setLayoutDirection(Qt.RightToLeft)
        self.exteriorLights = QCheckBox(self.trainStatus)
        self.exteriorLights.setObjectName(u"exteriorLights")
        self.exteriorLights.setGeometry(QRect(0, 90, 151, 31))
        self.exteriorLights.setFont(font1)
        self.exteriorLights.setLayoutDirection(Qt.RightToLeft)
        self.exteriorLights.setIconSize(QSize(16, 16))
        self.temperature = QSpinBox(self.trainStatus)
        self.temperature.setObjectName(u"temperature")
        self.temperature.setGeometry(QRect(240, 130, 140, 61))
        font2 = QFont()
        font2.setPointSize(12)
        font2.setUnderline(False)
        self.temperature.setFont(font2)
        self.temperature.setMinimum(60)
        self.temperature.setMaximum(80)
        self.temperature.setValue(70)
        self.textBrowser_4 = QTextBrowser(self.trainStatus)
        self.textBrowser_4.setObjectName(u"textBrowser_4")
        self.textBrowser_4.setGeometry(QRect(10, 130, 221, 61))
        self.intercom = QPushButton(self.trainStatus)
        self.intercom.setObjectName(u"intercom")
        self.intercom.setGeometry(QRect(80, 200, 240, 81))
        font3 = QFont()
        font3.setPointSize(12)
        font3.setBold(True)
        self.intercom.setFont(font3)
        self.announcementDisplay = QTextBrowser(self.trainStatus)
        self.announcementDisplay.setObjectName(u"announcementDisplay")
        self.announcementDisplay.setGeometry(QRect(0, 290, 390, 51))
        self.leftDoorsStatus = QTextBrowser(self.trainStatus)
        self.leftDoorsStatus.setObjectName(u"leftDoorsStatus")
        self.leftDoorsStatus.setGeometry(QRect(170, 0, 111, 31))
        self.rightDoorsStatus = QTextBrowser(self.trainStatus)
        self.rightDoorsStatus.setObjectName(u"rightDoorsStatus")
        self.rightDoorsStatus.setGeometry(QRect(170, 30, 111, 31))
        self.speedSettings = QFrame(TrainControllerSW)
        self.speedSettings.setObjectName(u"speedSettings")
        self.speedSettings.setGeometry(QRect(20, 250, 411, 421))
        self.speedSettings.setFrameShape(QFrame.NoFrame)
        self.speedSettings.setFrameShadow(QFrame.Raised)
        self.textBrowser_3 = QTextBrowser(self.speedSettings)
        self.textBrowser_3.setObjectName(u"textBrowser_3")
        self.textBrowser_3.setGeometry(QRect(10, 120, 300, 31))
        self.speedDownButton = QPushButton(self.speedSettings)
        self.speedDownButton.setObjectName(u"speedDownButton")
        self.speedDownButton.setGeometry(QRect(10, 200, 190, 111))
        self.speedDownButton.setFont(font3)
        self.speedDownButton.setAutoRepeat(True)
        self.textBrowser = QTextBrowser(self.speedSettings)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(10, 80, 300, 31))
        self.textBrowser_2 = QTextBrowser(self.speedSettings)
        self.textBrowser_2.setObjectName(u"textBrowser_2")
        self.textBrowser_2.setGeometry(QRect(10, 160, 300, 31))
        self.actualSpeedVal = QLCDNumber(self.speedSettings)
        self.actualSpeedVal.setObjectName(u"actualSpeedVal")
        self.actualSpeedVal.setGeometry(QRect(320, 80, 71, 31))
        self.actualSpeedVal.setAutoFillBackground(True)
        self.actualSpeedVal.setLineWidth(2)
        self.actualSpeedVal.setSmallDecimalPoint(False)
        self.setPointSpeedVal = QLCDNumber(self.speedSettings)
        self.setPointSpeedVal.setObjectName(u"setPointSpeedVal")
        self.setPointSpeedVal.setGeometry(QRect(320, 120, 71, 31))
        self.setPointSpeedVal.setAutoFillBackground(True)
        self.setPointSpeedVal.setLineWidth(2)
        self.setPointSpeedVal.setSmallDecimalPoint(False)
        self.serviceBrake = QPushButton(self.speedSettings)
        self.serviceBrake.setObjectName(u"serviceBrake")
        self.serviceBrake.setGeometry(QRect(10, 320, 390, 100))
        self.serviceBrake.setFont(font3)
        self.speedUpButton = QPushButton(self.speedSettings)
        self.speedUpButton.setObjectName(u"speedUpButton")
        self.speedUpButton.setGeometry(QRect(210, 200, 190, 111))
        self.speedUpButton.setFont(font3)
        self.speedUpButton.setAutoRepeat(True)
        self.commandedSpeedVal = QLCDNumber(self.speedSettings)
        self.commandedSpeedVal.setObjectName(u"commandedSpeedVal")
        self.commandedSpeedVal.setGeometry(QRect(320, 160, 71, 31))
        self.commandedSpeedVal.setAutoFillBackground(True)
        self.commandedSpeedVal.setLineWidth(2)
        self.commandedSpeedVal.setSmallDecimalPoint(False)
        self.textBrowser_8 = QTextBrowser(self.speedSettings)
        self.textBrowser_8.setObjectName(u"textBrowser_8")
        self.textBrowser_8.setGeometry(QRect(220, 40, 171, 31))
        self.textBrowser_9 = QTextBrowser(self.speedSettings)
        self.textBrowser_9.setObjectName(u"textBrowser_9")
        self.textBrowser_9.setGeometry(QRect(10, 40, 180, 31))
        self.textBrowser_9.setInputMethodHints(Qt.ImhMultiLine)
        self.travelParameters = QFrame(TrainControllerSW)
        self.travelParameters.setObjectName(u"travelParameters")
        self.travelParameters.setGeometry(QRect(20, 60, 411, 191))
        self.travelParameters.setFrameShape(QFrame.NoFrame)
        self.travelParameters.setFrameShadow(QFrame.Raised)
        self.textBrowser_5 = QTextBrowser(self.travelParameters)
        self.textBrowser_5.setObjectName(u"textBrowser_5")
        self.textBrowser_5.setGeometry(QRect(10, 50, 250, 31))
        self.textBrowser_6 = QTextBrowser(self.travelParameters)
        self.textBrowser_6.setObjectName(u"textBrowser_6")
        self.textBrowser_6.setGeometry(QRect(10, 10, 250, 31))
        self.textBrowser_7 = QTextBrowser(self.travelParameters)
        self.textBrowser_7.setObjectName(u"textBrowser_7")
        self.textBrowser_7.setGeometry(QRect(10, 90, 381, 31))
        self.power = QLCDNumber(self.travelParameters)
        self.power.setObjectName(u"power")
        self.power.setGeometry(QRect(270, 10, 121, 31))
        self.power.setAutoFillBackground(True)
        self.power.setLineWidth(2)
        self.power.setSmallDecimalPoint(False)
        self.authority = QLCDNumber(self.travelParameters)
        self.authority.setObjectName(u"authority")
        self.authority.setGeometry(QRect(270, 50, 121, 31))
        self.authority.setAutoFillBackground(True)
        self.authority.setLineWidth(2)
        self.authority.setSmallDecimalPoint(False)
        self.upcomingStation = QTextBrowser(self.travelParameters)
        self.upcomingStation.setObjectName(u"upcomingStation")
        self.upcomingStation.setGeometry(QRect(10, 130, 381, 41))
        font4 = QFont()
        font4.setPointSize(14)
        self.upcomingStation.setFont(font4)
        self.operationMode = QFrame(TrainControllerSW)
        self.operationMode.setObjectName(u"operationMode")
        self.operationMode.setGeometry(QRect(0, 10, 331, 31))
        self.operationMode.setFrameShape(QFrame.StyledPanel)
        self.operationMode.setFrameShadow(QFrame.Raised)
        self.manualMode = QRadioButton(self.operationMode)
        self.manualMode.setObjectName(u"manualMode")
        self.manualMode.setGeometry(QRect(180, 0, 131, 31))
        self.manualMode.setFont(font3)
        self.manualMode.setLayoutDirection(Qt.RightToLeft)
        self.manualMode.setChecked(False)
        self.automaticMode = QRadioButton(self.operationMode)
        self.automaticMode.setObjectName(u"automaticMode")
        self.automaticMode.setGeometry(QRect(20, 0, 151, 31))
        self.automaticMode.setFont(font3)
        self.automaticMode.setLayoutDirection(Qt.LeftToRight)
        self.automaticMode.setChecked(True)
        self.reportFailures = QFrame(TrainControllerSW)
        self.reportFailures.setObjectName(u"reportFailures")
        self.reportFailures.setGeometry(QRect(460, 380, 411, 171))
        self.reportFailures.setFrameShape(QFrame.NoFrame)
        self.reportFailures.setFrameShadow(QFrame.Raised)
        self.textBrowser_13 = QTextBrowser(self.reportFailures)
        self.textBrowser_13.setObjectName(u"textBrowser_13")
        self.textBrowser_13.setGeometry(QRect(10, 50, 391, 31))
        self.textBrowser_13.setStyleSheet(u"alternate-background-color: rgb(255, 0, 0);")
        self.textBrowser_14 = QTextBrowser(self.reportFailures)
        self.textBrowser_14.setObjectName(u"textBrowser_14")
        self.textBrowser_14.setGeometry(QRect(10, 10, 391, 31))
        self.textBrowser_14.setStyleSheet(u"alternate-background-color: rgb(255, 0, 0);")
        self.textBrowser_15 = QTextBrowser(self.reportFailures)
        self.textBrowser_15.setObjectName(u"textBrowser_15")
        self.textBrowser_15.setGeometry(QRect(10, 90, 391, 31))
        self.textBrowser_15.setStyleSheet(u"alternate-background-color: rgb(255, 255, 255);")
        self.textBrowser_16 = QTextBrowser(self.reportFailures)
        self.textBrowser_16.setObjectName(u"textBrowser_16")
        self.textBrowser_16.setGeometry(QRect(10, 130, 391, 31))
        self.textBrowser_16.setStyleSheet(u"alternate-background-color: rgb(255, 255, 255);")
        self.testing = QFrame(TrainControllerSW)
        self.testing.setObjectName(u"testing")
        self.testing.setGeometry(QRect(920, 30, 491, 641))
        self.testing.setFrameShape(QFrame.Box)
        self.testing.setFrameShadow(QFrame.Raised)
        self.testing.setLineWidth(1)
        self.testing.setMidLineWidth(1)
        self.causePassenger = QPushButton(self.testing)
        self.causePassenger.setObjectName(u"causePassenger")
        self.causePassenger.setGeometry(QRect(10, 300, 231, 31))
        self.causePassenger.setFont(font3)
        self.inputCommanded = QTextEdit(self.testing)
        self.inputCommanded.setObjectName(u"inputCommanded")
        self.inputCommanded.setGeometry(QRect(160, 60, 104, 21))
        self.inputCommanded.setAutoFillBackground(False)
        self.inputCommanded.setInputMethodHints(Qt.ImhFormattedNumbersOnly)
        self.inputAuthority = QTextEdit(self.testing)
        self.inputAuthority.setObjectName(u"inputAuthority")
        self.inputAuthority.setGeometry(QRect(160, 90, 104, 21))
        self.inputAuthority.setInputMethodHints(Qt.ImhFormattedNumbersOnly)
        self.label = QLabel(self.testing)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 60, 141, 20))
        self.label_2 = QLabel(self.testing)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 90, 101, 16))
        self.updateTCFake = QPushButton(self.testing)
        self.updateTCFake.setObjectName(u"updateTCFake")
        self.updateTCFake.setGeometry(QRect(60, 150, 121, 23))
        self.label_4 = QLabel(self.testing)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 190, 101, 16))
        self.actualSpeed = QTextEdit(self.testing)
        self.actualSpeed.setObjectName(u"actualSpeed")
        self.actualSpeed.setGeometry(QRect(160, 190, 104, 21))
        self.actualSpeed.setInputMethodHints(Qt.ImhFormattedNumbersOnly|Qt.ImhPreferNumbers)
        self.causePickupFailure = QCheckBox(self.testing)
        self.causePickupFailure.setObjectName(u"causePickupFailure")
        self.causePickupFailure.setGeometry(QRect(-10, 120, 131, 20))
        self.causePickupFailure.setLayoutDirection(Qt.RightToLeft)
        self.kiInput = QTextEdit(self.testing)
        self.kiInput.setObjectName(u"kiInput")
        self.kiInput.setGeometry(QRect(340, 360, 104, 21))
        self.label_6 = QLabel(self.testing)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(320, 360, 16, 16))
        self.label_7 = QLabel(self.testing)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(320, 390, 21, 16))
        self.kpInput = QTextEdit(self.testing)
        self.kpInput.setObjectName(u"kpInput")
        self.kpInput.setGeometry(QRect(340, 390, 104, 21))
        self.stationNameFake = QComboBox(self.testing)
        self.stationNameFake.addItem("")
        self.stationNameFake.addItem("")
        self.stationNameFake.addItem("")
        self.stationNameFake.addItem("")
        self.stationNameFake.addItem("")
        self.stationNameFake.addItem("")
        self.stationNameFake.addItem("")
        self.stationNameFake.addItem("")
        self.stationNameFake.addItem("")
        self.stationNameFake.addItem("")
        self.stationNameFake.addItem("")
        self.stationNameFake.addItem("")
        self.stationNameFake.addItem("")
        self.stationNameFake.addItem("")
        self.stationNameFake.addItem("")
        self.stationNameFake.addItem("")
        self.stationNameFake.addItem("")
        self.stationNameFake.addItem("")
        self.stationNameFake.addItem("")
        self.stationNameFake.addItem("")
        self.stationNameFake.setObjectName(u"stationNameFake")
        self.stationNameFake.setGeometry(QRect(310, 50, 151, 22))
        self.label_14 = QLabel(self.testing)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(320, 10, 121, 41))
        self.stationUpcoming = QCheckBox(self.testing)
        self.stationUpcoming.setObjectName(u"stationUpcoming")
        self.stationUpcoming.setGeometry(QRect(310, 80, 111, 17))
        self.leftDoorsFake = QCheckBox(self.testing)
        self.leftDoorsFake.setObjectName(u"leftDoorsFake")
        self.leftDoorsFake.setGeometry(QRect(310, 100, 111, 17))
        self.rightDoorsFake = QCheckBox(self.testing)
        self.rightDoorsFake.setObjectName(u"rightDoorsFake")
        self.rightDoorsFake.setGeometry(QRect(310, 120, 111, 17))
        self.exteriorLightsFake = QCheckBox(self.testing)
        self.exteriorLightsFake.setObjectName(u"exteriorLightsFake")
        self.exteriorLightsFake.setGeometry(QRect(310, 140, 121, 17))
        self.updateBeaconFake = QPushButton(self.testing)
        self.updateBeaconFake.setObjectName(u"updateBeaconFake")
        self.updateBeaconFake.setGeometry(QRect(320, 170, 111, 23))
        self.label_15 = QLabel(self.testing)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(30, 20, 121, 41))
        self.updateActualFake = QPushButton(self.testing)
        self.updateActualFake.setObjectName(u"updateActualFake")
        self.updateActualFake.setGeometry(QRect(60, 230, 121, 23))
        self.causeEngineFailure = QPushButton(self.testing)
        self.causeEngineFailure.setObjectName(u"causeEngineFailure")
        self.causeEngineFailure.setGeometry(QRect(10, 350, 231, 31))
        self.causeEngineFailure.setFont(font3)
        self.causeBrakeFailure = QPushButton(self.testing)
        self.causeBrakeFailure.setObjectName(u"causeBrakeFailure")
        self.causeBrakeFailure.setGeometry(QRect(10, 400, 231, 31))
        self.causeBrakeFailure.setFont(font3)
        self.updatePID = QPushButton(self.testing)
        self.updatePID.setObjectName(u"updatePID")
        self.updatePID.setGeometry(QRect(320, 430, 111, 23))
        self.encodedTC = QTextBrowser(self.testing)
        self.encodedTC.setObjectName(u"encodedTC")
        self.encodedTC.setGeometry(QRect(20, 520, 161, 101))
        self.encodedBeacon = QTextBrowser(self.testing)
        self.encodedBeacon.setObjectName(u"encodedBeacon")
        self.encodedBeacon.setGeometry(QRect(190, 520, 161, 101))
        self.label_16 = QLabel(self.testing)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(190, 500, 101, 16))
        self.label_5 = QLabel(self.testing)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 500, 101, 16))
        self.textBrowser_10 = QTextBrowser(self.testing)
        self.textBrowser_10.setObjectName(u"textBrowser_10")
        self.textBrowser_10.setGeometry(QRect(300, 460, 171, 31))
        self.textBrowser_11 = QTextBrowser(self.testing)
        self.textBrowser_11.setObjectName(u"textBrowser_11")
        self.textBrowser_11.setGeometry(QRect(50, 460, 171, 31))
        self.textBrowser_12 = QTextBrowser(self.testing)
        self.textBrowser_12.setObjectName(u"textBrowser_12")
        self.textBrowser_12.setGeometry(QRect(400, 210, 61, 31))
        self.label_8 = QLabel(self.testing)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(310, 220, 101, 16))
        self.intercomFake = QTextBrowser(self.testing)
        self.intercomFake.setObjectName(u"intercomFake")
        self.intercomFake.setGeometry(QRect(360, 520, 121, 101))
        self.label_17 = QLabel(self.testing)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(360, 500, 101, 16))
        self.textBrowser_17 = QTextBrowser(self.testing)
        self.textBrowser_17.setObjectName(u"textBrowser_17")
        self.textBrowser_17.setGeometry(QRect(400, 250, 61, 31))
        self.label_9 = QLabel(self.testing)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(330, 260, 101, 16))
        self.exteriorLights_2 = QCheckBox(self.testing)
        self.exteriorLights_2.setObjectName(u"exteriorLights_2")
        self.exteriorLights_2.setGeometry(QRect(290, 290, 151, 31))
        font5 = QFont()
        font5.setPointSize(8)
        self.exteriorLights_2.setFont(font5)
        self.exteriorLights_2.setLayoutDirection(Qt.RightToLeft)
        self.exteriorLights_2.setIconSize(QSize(16, 16))
        self.interiorLights_2 = QCheckBox(self.testing)
        self.interiorLights_2.setObjectName(u"interiorLights_2")
        self.interiorLights_2.setGeometry(QRect(290, 320, 151, 31))
        self.interiorLights_2.setFont(font5)
        self.interiorLights_2.setLayoutDirection(Qt.RightToLeft)
        self.label_3 = QLabel(TrainControllerSW)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(950, 10, 161, 16))
        self.frame = QFrame(TrainControllerSW)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 10, 880, 660))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setMidLineWidth(1)
        self.frame.raise_()
        self.emergencyBrake.raise_()
        self.trainStatus.raise_()
        self.speedSettings.raise_()
        self.travelParameters.raise_()
        self.operationMode.raise_()
        self.reportFailures.raise_()
        self.testing.raise_()
        self.label_3.raise_()

        self.retranslateUi(TrainControllerSW)

        QMetaObject.connectSlotsByName(TrainControllerSW)
    # setupUi

    def retranslateUi(self, TrainControllerSW):
        TrainControllerSW.setWindowTitle(QCoreApplication.translate("TrainControllerSW", u"TrainControllerSW", None))
        self.emergencyBrake.setText(QCoreApplication.translate("TrainControllerSW", u"Apply Emergency Brake", None))
        self.rightDoors.setText(QCoreApplication.translate("TrainControllerSW", u"Right Doors Open", None))
        self.leftDoors.setText(QCoreApplication.translate("TrainControllerSW", u"Left Doors Open", None))
        self.interiorLights.setText(QCoreApplication.translate("TrainControllerSW", u"Interior Lights On", None))
        self.exteriorLights.setText(QCoreApplication.translate("TrainControllerSW", u"Exterior Lights On", None))
        self.temperature.setSpecialValueText("")
        self.textBrowser_4.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Temperature (F)</span></p></body></html>", None))
        self.intercom.setText(QCoreApplication.translate("TrainControllerSW", u"Intercom", None))
        self.textBrowser_3.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Setpoint Speed (mph)</span></p></body></html>", None))
        self.speedDownButton.setText(QCoreApplication.translate("TrainControllerSW", u"Decrease Speed", None))
        self.textBrowser.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Actual Speed (mph)</span></p></body></html>", None))
        self.textBrowser_2.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Commanded Speed (mph)</span></p></body></html>", None))
        self.serviceBrake.setText(QCoreApplication.translate("TrainControllerSW", u"Apply Service Brake", None))
        self.speedUpButton.setText(QCoreApplication.translate("TrainControllerSW", u"Increase Speed", None))
        self.textBrowser_8.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">E Brake?</span></p></body></html>", None))
        self.textBrowser_9.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">S Brake?</span></p></body></html>", None))
        self.textBrowser_5.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Authority (feet)</span></p></body></html>", None))
        self.textBrowser_6.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Power (kW)</span></p></body></html>", None))
        self.textBrowser_7.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Next Station:</span></p></body></html>", None))
        self.manualMode.setText(QCoreApplication.translate("TrainControllerSW", u"Manual Mode", None))
        self.automaticMode.setText(QCoreApplication.translate("TrainControllerSW", u"Automatic Mode", None))
        self.textBrowser_13.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Train Engine Failure</span></p></body></html>", None))
        self.textBrowser_14.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Brake Failure</span></p></body></html>", None))
        self.textBrowser_15.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Signal Pickup Failure</span></p></body></html>", None))
        self.textBrowser_16.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Passenger Brake Detected</span></p></body></html>", None))
        self.causePassenger.setText(QCoreApplication.translate("TrainControllerSW", u"deploy passenger brake", None))
        self.label.setText(QCoreApplication.translate("TrainControllerSW", u"Commanded Speed (m/s):", None))
        self.label_2.setText(QCoreApplication.translate("TrainControllerSW", u"Authority (m):", None))
        self.updateTCFake.setText(QCoreApplication.translate("TrainControllerSW", u"Update Track Circuit", None))
        self.label_4.setText(QCoreApplication.translate("TrainControllerSW", u"Actual Speed (m/s):", None))
        self.causePickupFailure.setText(QCoreApplication.translate("TrainControllerSW", u"causePickupFailure", None))
        self.label_6.setText(QCoreApplication.translate("TrainControllerSW", u"Ki:", None))
        self.label_7.setText(QCoreApplication.translate("TrainControllerSW", u"Kp:", None))
        self.stationNameFake.setItemText(0, QCoreApplication.translate("TrainControllerSW", u"Shadyside", None))
        self.stationNameFake.setItemText(1, QCoreApplication.translate("TrainControllerSW", u"Herron Ave", None))
        self.stationNameFake.setItemText(2, QCoreApplication.translate("TrainControllerSW", u"Swissville", None))
        self.stationNameFake.setItemText(3, QCoreApplication.translate("TrainControllerSW", u"Penn Station", None))
        self.stationNameFake.setItemText(4, QCoreApplication.translate("TrainControllerSW", u"Steel Plaza", None))
        self.stationNameFake.setItemText(5, QCoreApplication.translate("TrainControllerSW", u"First Ave", None))
        self.stationNameFake.setItemText(6, QCoreApplication.translate("TrainControllerSW", u"Station Square", None))
        self.stationNameFake.setItemText(7, QCoreApplication.translate("TrainControllerSW", u"South Hills Junction", None))
        self.stationNameFake.setItemText(8, QCoreApplication.translate("TrainControllerSW", u"Pioneer", None))
        self.stationNameFake.setItemText(9, QCoreApplication.translate("TrainControllerSW", u"Edgebrook", None))
        self.stationNameFake.setItemText(10, QCoreApplication.translate("TrainControllerSW", u"Whited", None))
        self.stationNameFake.setItemText(11, QCoreApplication.translate("TrainControllerSW", u"South Bank", None))
        self.stationNameFake.setItemText(12, QCoreApplication.translate("TrainControllerSW", u"Central", None))
        self.stationNameFake.setItemText(13, QCoreApplication.translate("TrainControllerSW", u"Inglewood", None))
        self.stationNameFake.setItemText(14, QCoreApplication.translate("TrainControllerSW", u"Overbrook", None))
        self.stationNameFake.setItemText(15, QCoreApplication.translate("TrainControllerSW", u"Glenbury", None))
        self.stationNameFake.setItemText(16, QCoreApplication.translate("TrainControllerSW", u"Dormont", None))
        self.stationNameFake.setItemText(17, QCoreApplication.translate("TrainControllerSW", u"Mt Lebanon", None))
        self.stationNameFake.setItemText(18, QCoreApplication.translate("TrainControllerSW", u"Poplar", None))
        self.stationNameFake.setItemText(19, QCoreApplication.translate("TrainControllerSW", u"Castle Shannon", None))

        self.label_14.setText(QCoreApplication.translate("TrainControllerSW", u"Beacon Inputs", None))
        self.stationUpcoming.setText(QCoreApplication.translate("TrainControllerSW", u"Station Upcoming", None))
        self.leftDoorsFake.setText(QCoreApplication.translate("TrainControllerSW", u"Left Doors", None))
        self.rightDoorsFake.setText(QCoreApplication.translate("TrainControllerSW", u"Right Doors", None))
        self.exteriorLightsFake.setText(QCoreApplication.translate("TrainControllerSW", u"Exterior Lights on", None))
        self.updateBeaconFake.setText(QCoreApplication.translate("TrainControllerSW", u"Update Beacon", None))
        self.label_15.setText(QCoreApplication.translate("TrainControllerSW", u"Track Circuit", None))
        self.updateActualFake.setText(QCoreApplication.translate("TrainControllerSW", u"Update Actual Speed", None))
        self.causeEngineFailure.setText(QCoreApplication.translate("TrainControllerSW", u"Cause Engine Failure", None))
        self.causeBrakeFailure.setText(QCoreApplication.translate("TrainControllerSW", u"Cause Brake Failure", None))
        self.updatePID.setText(QCoreApplication.translate("TrainControllerSW", u"Update PID", None))
        self.label_16.setText(QCoreApplication.translate("TrainControllerSW", u"Encoded Beacon", None))
        self.label_5.setText(QCoreApplication.translate("TrainControllerSW", u"Encoded Track Circuit", None))
        self.textBrowser_10.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">E Brake?</span></p></body></html>", None))
        self.textBrowser_11.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">S Brake?</span></p></body></html>", None))
        self.textBrowser_12.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">70</p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("TrainControllerSW", u"Temperature (F):", None))
        self.intercomFake.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_17.setText(QCoreApplication.translate("TrainControllerSW", u"Intercom", None))
        self.textBrowser_17.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0</p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("TrainControllerSW", u"Power (W) :", None))
        self.exteriorLights_2.setText(QCoreApplication.translate("TrainControllerSW", u"Exterior Lights On", None))
        self.interiorLights_2.setText(QCoreApplication.translate("TrainControllerSW", u"Interior Lights On", None))
        self.label_3.setText(QCoreApplication.translate("TrainControllerSW", u"TEST UI:", None))
    # retranslateUi

