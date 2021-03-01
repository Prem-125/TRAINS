# -*- coding: utf-8 -*-

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
        TrainControllerSW.resize(1250, 685)
        self.emergencyBrake = QPushButton(TrainControllerSW)
        self.emergencyBrake.setObjectName(u"emergencyBrake")
        self.emergencyBrake.setGeometry(QRect(460, 560, 411, 111))
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
        self.trainStatus.setGeometry(QRect(470, 30, 381, 341))
        self.rightDoors = QCheckBox(self.trainStatus)
        self.rightDoors.setObjectName(u"rightDoors")
        self.rightDoors.setGeometry(QRect(0, 30, 151, 31))
        font1 = QFont()
        font1.setPointSize(12)
        self.rightDoors.setFont(font1)
        self.rightDoors.setLayoutDirection(Qt.RightToLeft)
        self.checkBox_2 = QCheckBox(self.trainStatus)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(0, 0, 151, 31))
        self.checkBox_2.setFont(font1)
        self.checkBox_2.setLayoutDirection(Qt.RightToLeft)
        self.interiorLights = QCheckBox(self.trainStatus)
        self.interiorLights.setObjectName(u"interiorLights")
        self.interiorLights.setGeometry(QRect(0, 60, 151, 31))
        self.interiorLights.setFont(font1)
        self.interiorLights.setLayoutDirection(Qt.RightToLeft)
        self.checkBox_4 = QCheckBox(self.trainStatus)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setGeometry(QRect(0, 90, 151, 31))
        self.checkBox_4.setFont(font1)
        self.checkBox_4.setLayoutDirection(Qt.RightToLeft)
        self.checkBox_4.setIconSize(QSize(16, 16))
        self.temperature = QSpinBox(self.trainStatus)
        self.temperature.setObjectName(u"temperature")
        self.temperature.setGeometry(QRect(240, 130, 131, 61))
        font2 = QFont()
        font2.setPointSize(12)
        font2.setUnderline(False)
        self.temperature.setFont(font2)
        self.temperature.setValue(70)
        self.textBrowser_4 = QTextBrowser(self.trainStatus)
        self.textBrowser_4.setObjectName(u"textBrowser_4")
        self.textBrowser_4.setGeometry(QRect(10, 130, 221, 61))
        self.intercom = QPushButton(self.trainStatus)
        self.intercom.setObjectName(u"intercom")
        self.intercom.setGeometry(QRect(80, 220, 231, 91))
        font3 = QFont()
        font3.setPointSize(12)
        font3.setBold(True)
        self.intercom.setFont(font3)
        self.speedSettings = QFrame(TrainControllerSW)
        self.speedSettings.setObjectName(u"speedSettings")
        self.speedSettings.setGeometry(QRect(20, 310, 311, 361))
        self.speedSettings.setFrameShape(QFrame.StyledPanel)
        self.speedSettings.setFrameShadow(QFrame.Raised)
        self.textBrowser_3 = QTextBrowser(self.speedSettings)
        self.textBrowser_3.setObjectName(u"textBrowser_3")
        self.textBrowser_3.setGeometry(QRect(10, 50, 211, 31))
        self.speedDownButton = QPushButton(self.speedSettings)
        self.speedDownButton.setObjectName(u"speedDownButton")
        self.speedDownButton.setGeometry(QRect(10, 130, 141, 111))
        self.speedDownButton.setFont(font3)
        self.speedDownButton.setAutoRepeat(True)
        self.textBrowser = QTextBrowser(self.speedSettings)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(10, 10, 211, 31))
        self.textBrowser_2 = QTextBrowser(self.speedSettings)
        self.textBrowser_2.setObjectName(u"textBrowser_2")
        self.textBrowser_2.setGeometry(QRect(10, 90, 211, 31))
        self.actualSpeedVal = QLCDNumber(self.speedSettings)
        self.actualSpeedVal.setObjectName(u"actualSpeedVal")
        self.actualSpeedVal.setGeometry(QRect(230, 10, 71, 31))
        self.actualSpeedVal.setAutoFillBackground(True)
        self.actualSpeedVal.setLineWidth(2)
        self.actualSpeedVal.setSmallDecimalPoint(False)
        self.setPointSpeedVal = QLCDNumber(self.speedSettings)
        self.setPointSpeedVal.setObjectName(u"setPointSpeedVal")
        self.setPointSpeedVal.setGeometry(QRect(230, 50, 71, 31))
        self.setPointSpeedVal.setAutoFillBackground(True)
        self.setPointSpeedVal.setLineWidth(2)
        self.setPointSpeedVal.setSmallDecimalPoint(False)
        self.serviceBrake = QPushButton(self.speedSettings)
        self.serviceBrake.setObjectName(u"serviceBrake")
        self.serviceBrake.setGeometry(QRect(10, 250, 291, 111))
        self.serviceBrake.setFont(font3)
        self.speedUpButton = QPushButton(self.speedSettings)
        self.speedUpButton.setObjectName(u"speedUpButton")
        self.speedUpButton.setGeometry(QRect(160, 130, 141, 111))
        self.speedUpButton.setFont(font3)
        self.speedUpButton.setAutoRepeat(True)
        self.commandedSpeedVal = QLCDNumber(self.speedSettings)
        self.commandedSpeedVal.setObjectName(u"commandedSpeedVal")
        self.commandedSpeedVal.setGeometry(QRect(230, 90, 71, 31))
        self.commandedSpeedVal.setAutoFillBackground(True)
        self.commandedSpeedVal.setLineWidth(2)
        self.commandedSpeedVal.setSmallDecimalPoint(False)
        self.travelParameters = QFrame(TrainControllerSW)
        self.travelParameters.setObjectName(u"travelParameters")
        self.travelParameters.setGeometry(QRect(20, 60, 271, 241))
        self.travelParameters.setFrameShape(QFrame.StyledPanel)
        self.travelParameters.setFrameShadow(QFrame.Raised)
        self.textBrowser_5 = QTextBrowser(self.travelParameters)
        self.textBrowser_5.setObjectName(u"textBrowser_5")
        self.textBrowser_5.setGeometry(QRect(10, 50, 171, 31))
        self.textBrowser_6 = QTextBrowser(self.travelParameters)
        self.textBrowser_6.setObjectName(u"textBrowser_6")
        self.textBrowser_6.setGeometry(QRect(10, 10, 171, 31))
        self.textBrowser_7 = QTextBrowser(self.travelParameters)
        self.textBrowser_7.setObjectName(u"textBrowser_7")
        self.textBrowser_7.setGeometry(QRect(10, 90, 171, 31))
        self.power = QLCDNumber(self.travelParameters)
        self.power.setObjectName(u"power")
        self.power.setGeometry(QRect(190, 10, 71, 31))
        self.power.setAutoFillBackground(True)
        self.power.setLineWidth(2)
        self.power.setSmallDecimalPoint(False)
        self.authority = QLCDNumber(self.travelParameters)
        self.authority.setObjectName(u"authority")
        self.authority.setGeometry(QRect(190, 50, 71, 31))
        self.authority.setAutoFillBackground(True)
        self.authority.setLineWidth(2)
        self.authority.setSmallDecimalPoint(False)
        self.nextStation = QLCDNumber(self.travelParameters)
        self.nextStation.setObjectName(u"nextStation")
        self.nextStation.setGeometry(QRect(190, 92, 71, 31))
        self.nextStation.setAutoFillBackground(True)
        self.nextStation.setLineWidth(2)
        self.nextStation.setSmallDecimalPoint(False)
        self.textBrowser_8 = QTextBrowser(self.travelParameters)
        self.textBrowser_8.setObjectName(u"textBrowser_8")
        self.textBrowser_8.setGeometry(QRect(10, 130, 171, 31))
        self.distanceToNext = QLCDNumber(self.travelParameters)
        self.distanceToNext.setObjectName(u"distanceToNext")
        self.distanceToNext.setGeometry(QRect(190, 130, 71, 31))
        self.distanceToNext.setAutoFillBackground(True)
        self.distanceToNext.setLineWidth(2)
        self.distanceToNext.setSmallDecimalPoint(False)
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
        self.failureEvents = QFrame(TrainControllerSW)
        self.failureEvents.setObjectName(u"failureEvents")
        self.failureEvents.setGeometry(QRect(460, 380, 411, 171))
        self.failureEvents.setFrameShape(QFrame.StyledPanel)
        self.failureEvents.setFrameShadow(QFrame.Raised)
        self.textBrowser_13 = QTextBrowser(self.failureEvents)
        self.textBrowser_13.setObjectName(u"textBrowser_13")
        self.textBrowser_13.setGeometry(QRect(10, 50, 391, 31))
        self.textBrowser_13.setStyleSheet(u"alternate-background-color: rgb(255, 0, 0);")
        self.textBrowser_14 = QTextBrowser(self.failureEvents)
        self.textBrowser_14.setObjectName(u"textBrowser_14")
        self.textBrowser_14.setGeometry(QRect(10, 10, 391, 31))
        self.textBrowser_14.setStyleSheet(u"alternate-background-color: rgb(255, 0, 0);")
        self.textBrowser_15 = QTextBrowser(self.failureEvents)
        self.textBrowser_15.setObjectName(u"textBrowser_15")
        self.textBrowser_15.setGeometry(QRect(10, 90, 391, 31))
        self.textBrowser_15.setStyleSheet(u"alternate-background-color: rgb(255, 255, 255);")
        self.textBrowser_16 = QTextBrowser(self.failureEvents)
        self.textBrowser_16.setObjectName(u"textBrowser_16")
        self.textBrowser_16.setGeometry(QRect(10, 130, 391, 31))
        self.textBrowser_16.setStyleSheet(u"alternate-background-color: rgb(255, 255, 255);")
        self.frame = QFrame(TrainControllerSW)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(950, 30, 231, 391))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.causePassenger = QPushButton(self.frame)
        self.causePassenger.setObjectName(u"causePassenger")
        self.causePassenger.setGeometry(QRect(0, 80, 231, 31))
        self.causePassenger.setFont(font3)
        self.causeEngine = QPushButton(self.frame)
        self.causeEngine.setObjectName(u"causeEngine")
        self.causeEngine.setGeometry(QRect(0, 40, 231, 31))
        self.causeEngine.setFont(font3)
        self.causeBrake = QPushButton(self.frame)
        self.causeBrake.setObjectName(u"causeBrake")
        self.causeBrake.setGeometry(QRect(0, 0, 231, 31))
        self.causeBrake.setFont(font3)
        self.inputCommanded = QTextEdit(self.frame)
        self.inputCommanded.setObjectName(u"inputCommanded")
        self.inputCommanded.setGeometry(QRect(120, 160, 104, 21))
        self.inputAuthority = QTextEdit(self.frame)
        self.inputAuthority.setObjectName(u"inputAuthority")
        self.inputAuthority.setGeometry(QRect(120, 190, 104, 21))
        self.inputBeacon = QTextEdit(self.frame)
        self.inputBeacon.setObjectName(u"inputBeacon")
        self.inputBeacon.setGeometry(QRect(120, 220, 104, 21))
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 160, 101, 16))
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 190, 101, 16))
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(0, 220, 101, 16))
        self.updateFake = QPushButton(self.frame)
        self.updateFake.setObjectName(u"updateFake")
        self.updateFake.setGeometry(QRect(70, 360, 75, 23))
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(0, 250, 101, 16))
        self.actualSpeed = QTextEdit(self.frame)
        self.actualSpeed.setObjectName(u"actualSpeed")
        self.actualSpeed.setGeometry(QRect(120, 250, 104, 21))
        self.causePickupFailure = QCheckBox(self.frame)
        self.causePickupFailure.setObjectName(u"causePickupFailure")
        self.causePickupFailure.setGeometry(QRect(0, 280, 111, 20))
        self.causePickupFailure.setLayoutDirection(Qt.RightToLeft)
        self.encodedTC = QTextBrowser(TrainControllerSW)
        self.encodedTC.setObjectName(u"encodedTC")
        self.encodedTC.setGeometry(QRect(940, 430, 256, 192))
        self.label_5 = QLabel(TrainControllerSW)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(1000, 590, 101, 16))

        self.retranslateUi(TrainControllerSW)

        QMetaObject.connectSlotsByName(TrainControllerSW)
    # setupUi

    def retranslateUi(self, TrainControllerSW):
        TrainControllerSW.setWindowTitle(QCoreApplication.translate("TrainControllerSW", u"TrainControllerSW", None))
        self.emergencyBrake.setText(QCoreApplication.translate("TrainControllerSW", u"Apply Emergency Brake", None))
        self.rightDoors.setText(QCoreApplication.translate("TrainControllerSW", u"Right Doors Open", None))
        self.checkBox_2.setText(QCoreApplication.translate("TrainControllerSW", u"Left Doors Open", None))
        self.interiorLights.setText(QCoreApplication.translate("TrainControllerSW", u"Interior Lights On", None))
        self.checkBox_4.setText(QCoreApplication.translate("TrainControllerSW", u"Exterior Lights On", None))
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
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Setpoint Speed</span></p></body></html>", None))
        self.speedDownButton.setText(QCoreApplication.translate("TrainControllerSW", u"Decrease Speed", None))
        self.textBrowser.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Actual Speed</span></p></body></html>", None))
        self.textBrowser_2.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Commanded Speed</span></p></body></html>", None))
        self.serviceBrake.setText(QCoreApplication.translate("TrainControllerSW", u"Apply Service Brake", None))
        self.speedUpButton.setText(QCoreApplication.translate("TrainControllerSW", u"Increase Speed", None))
        self.textBrowser_5.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Authority</span></p></body></html>", None))
        self.textBrowser_6.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Power</span></p></body></html>", None))
        self.textBrowser_7.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Next Station</span></p></body></html>", None))
        self.textBrowser_8.setHtml(QCoreApplication.translate("TrainControllerSW", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Distance To Next</span></p></body></html>", None))
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
        self.causeEngine.setText(QCoreApplication.translate("TrainControllerSW", u"cause engine failure", None))
        self.causeBrake.setText(QCoreApplication.translate("TrainControllerSW", u"cause brake failure", None))
        self.label.setText(QCoreApplication.translate("TrainControllerSW", u"Commanded Speed:", None))
        self.label_2.setText(QCoreApplication.translate("TrainControllerSW", u"Authority", None))
        self.label_3.setText(QCoreApplication.translate("TrainControllerSW", u"Encoded Beacon", None))
        self.updateFake.setText(QCoreApplication.translate("TrainControllerSW", u"Update", None))
        self.label_4.setText(QCoreApplication.translate("TrainControllerSW", u"Actual Speed:", None))
        self.causePickupFailure.setText(QCoreApplication.translate("TrainControllerSW", u"causePickupFailure", None))
        self.label_5.setText(QCoreApplication.translate("TrainControllerSW", u"Encoded Track Circuit", None))
    # retranslateUi

