﻿# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'trackUIdesign.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1125, 773)
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(-10, 0, 1131, 841))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.LineBox = QGroupBox(self.tab)
        self.LineBox.setObjectName(u"LineBox")
        self.LineBox.setGeometry(QRect(10, 10, 1101, 161))
        self.trackSelector = QLineEdit(self.LineBox)
        self.trackSelector.setObjectName(u"trackSelector")
        self.trackSelector.setGeometry(QRect(10, 60, 191, 22))
        self.label_17 = QLabel(self.LineBox)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(10, 30, 201, 31))
        self.getTrackBTN = QPushButton(self.LineBox)
        self.getTrackBTN.setObjectName(u"getTrackBTN")
        self.getTrackBTN.setGeometry(QRect(10, 90, 191, 28))
        self.trackSelectorValid = QLabel(self.LineBox)
        self.trackSelectorValid.setObjectName(u"trackSelectorValid")
        self.trackSelectorValid.setGeometry(QRect(210, 60, 201, 31))
        self.trackBox = QGroupBox(self.tab)
        self.trackBox.setObjectName(u"trackBox")
        self.trackBox.setGeometry(QRect(10, 180, 371, 561))
        self.label_13 = QLabel(self.trackBox)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(10, 20, 261, 341))
        self.selTrackSW = QLabel(self.trackBox)
        self.selTrackSW.setObjectName(u"selTrackSW")
        self.selTrackSW.setGeometry(QRect(290, 50, 55, 31))
        self.selTrackCross = QLabel(self.trackBox)
        self.selTrackCross.setObjectName(u"selTrackCross")
        self.selTrackCross.setGeometry(QRect(290, 80, 55, 31))
        self.selTrackSpeed = QLCDNumber(self.trackBox)
        self.selTrackSpeed.setObjectName(u"selTrackSpeed")
        self.selTrackSpeed.setGeometry(QRect(250, 110, 71, 31))
        self.label_14 = QLabel(self.trackBox)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(330, 120, 61, 21))
        self.selTrackHeater = QLabel(self.trackBox)
        self.selTrackHeater.setObjectName(u"selTrackHeater")
        self.selTrackHeater.setGeometry(QRect(290, 190, 55, 31))
        self.selTrackBranch = QLabel(self.trackBox)
        self.selTrackBranch.setObjectName(u"selTrackBranch")
        self.selTrackBranch.setGeometry(QRect(290, 220, 55, 31))
        self.trackStatusBox = QGroupBox(self.trackBox)
        self.trackStatusBox.setObjectName(u"trackStatusBox")
        self.trackStatusBox.setGeometry(QRect(10, 360, 351, 141))
        self.label_15 = QLabel(self.trackStatusBox)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(10, 20, 131, 211))
        self.selTrackRailStat = QLabel(self.trackStatusBox)
        self.selTrackRailStat.setObjectName(u"selTrackRailStat")
        self.selTrackRailStat.setGeometry(QRect(280, 30, 55, 31))
        self.selTrackCircStat = QLabel(self.trackStatusBox)
        self.selTrackCircStat.setObjectName(u"selTrackCircStat")
        self.selTrackCircStat.setGeometry(QRect(280, 70, 55, 31))
        self.selTrackPowerStat = QLabel(self.trackStatusBox)
        self.selTrackPowerStat.setObjectName(u"selTrackPowerStat")
        self.selTrackPowerStat.setGeometry(QRect(280, 100, 55, 31))
        self.trackSignalBox = QGroupBox(self.trackBox)
        self.trackSignalBox.setObjectName(u"trackSignalBox")
        self.trackSignalBox.setGeometry(QRect(10, 500, 351, 51))
        self.sigGo = QRadioButton(self.trackSignalBox)
        self.sigGo.setObjectName(u"sigGo")
        self.sigGo.setGeometry(QRect(10, 20, 95, 20))
        self.sigGo.setCheckable(True)
        self.sigSlow = QRadioButton(self.trackSignalBox)
        self.sigSlow.setObjectName(u"sigSlow")
        self.sigSlow.setGeometry(QRect(120, 20, 95, 20))
        self.sigStop = QRadioButton(self.trackSignalBox)
        self.sigStop.setObjectName(u"sigStop")
        self.sigStop.setGeometry(QRect(240, 20, 95, 20))
        self.selTrackSection = QLabel(self.trackBox)
        self.selTrackSection.setObjectName(u"selTrackSection")
        self.selTrackSection.setGeometry(QRect(290, 20, 55, 31))
        self.selTrackGrade = QLabel(self.trackBox)
        self.selTrackGrade.setObjectName(u"selTrackGrade")
        self.selTrackGrade.setGeometry(QRect(290, 150, 55, 31))
        self.selTrackStation = QLabel(self.trackBox)
        self.selTrackStation.setObjectName(u"selTrackStation")
        self.selTrackStation.setGeometry(QRect(234, 250, 111, 31))
        self.selTrackUnderground = QLabel(self.trackBox)
        self.selTrackUnderground.setObjectName(u"selTrackUnderground")
        self.selTrackUnderground.setGeometry(QRect(290, 320, 91, 31))
        self.selTrackStationSide = QLabel(self.trackBox)
        self.selTrackStationSide.setObjectName(u"selTrackStationSide")
        self.selTrackStationSide.setGeometry(QRect(260, 290, 91, 31))
        self.failBox = QGroupBox(self.tab)
        self.failBox.setObjectName(u"failBox")
        self.failBox.setGeometry(QRect(410, 180, 261, 261))
        self.breakRailBTN = QPushButton(self.failBox)
        self.breakRailBTN.setObjectName(u"breakRailBTN")
        self.breakRailBTN.setGeometry(QRect(20, 30, 221, 61))
        self.breakCircuitBTN = QPushButton(self.failBox)
        self.breakCircuitBTN.setObjectName(u"breakCircuitBTN")
        self.breakCircuitBTN.setGeometry(QRect(20, 110, 221, 61))
        self.breakPowerBTN = QPushButton(self.failBox)
        self.breakPowerBTN.setObjectName(u"breakPowerBTN")
        self.breakPowerBTN.setGeometry(QRect(20, 190, 221, 61))
        self.waysideBox = QGroupBox(self.tab)
        self.waysideBox.setObjectName(u"waysideBox")
        self.waysideBox.setGeometry(QRect(700, 180, 411, 161))
        self.wayCommandedSpeed = QLCDNumber(self.waysideBox)
        self.wayCommandedSpeed.setObjectName(u"wayCommandedSpeed")
        self.wayCommandedSpeed.setGeometry(QRect(290, 10, 71, 31))
        self.label = QLabel(self.waysideBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 261, 131))
        self.wayAuthority = QLCDNumber(self.waysideBox)
        self.wayAuthority.setObjectName(u"wayAuthority")
        self.wayAuthority.setGeometry(QRect(290, 50, 71, 31))
        self.waySwitch = QLabel(self.waysideBox)
        self.waySwitch.setObjectName(u"waySwitch")
        self.waySwitch.setGeometry(QRect(294, 80, 91, 31))
        self.waySignal = QLabel(self.waysideBox)
        self.waySignal.setObjectName(u"waySignal")
        self.waySignal.setGeometry(QRect(330, 120, 55, 31))
        self.label_11 = QLabel(self.waysideBox)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(370, 20, 61, 21))
        self.label_12 = QLabel(self.waysideBox)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(370, 60, 61, 21))
        self.waySwitchBTN = QPushButton(self.waysideBox)
        self.waySwitchBTN.setObjectName(u"waySwitchBTN")
        self.waySwitchBTN.setGeometry(QRect(180, 80, 93, 28))
        self.outputBox = QGroupBox(self.tab)
        self.outputBox.setObjectName(u"outputBox")
        self.outputBox.setGeometry(QRect(700, 350, 411, 391))
        self.label_2 = QLabel(self.outputBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 10, 81, 41))
        self.label_3 = QLabel(self.outputBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 50, 261, 131))
        self.label_4 = QLabel(self.outputBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 190, 81, 41))
        self.label_5 = QLabel(self.outputBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 230, 261, 51))
        self.label_6 = QLabel(self.outputBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 300, 111, 41))
        self.label_7 = QLabel(self.outputBox)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 350, 261, 31))
        self.trainSpeedLimitO = QLCDNumber(self.outputBox)
        self.trainSpeedLimitO.setObjectName(u"trainSpeedLimitO")
        self.trainSpeedLimitO.setGeometry(QRect(290, 50, 71, 31))
        self.trainAuthorityO = QLCDNumber(self.outputBox)
        self.trainAuthorityO.setObjectName(u"trainAuthorityO")
        self.trainAuthorityO.setGeometry(QRect(290, 80, 71, 31))
        self.trainBeaconO = QLabel(self.outputBox)
        self.trainBeaconO.setObjectName(u"trainBeaconO")
        self.trainBeaconO.setGeometry(QRect(200, 110, 171, 31))
        self.label_8 = QLabel(self.outputBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(370, 60, 61, 21))
        self.label_9 = QLabel(self.outputBox)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(370, 90, 61, 21))
        self.ctcTicketO = QLCDNumber(self.outputBox)
        self.ctcTicketO.setObjectName(u"ctcTicketO")
        self.ctcTicketO.setGeometry(QRect(290, 250, 71, 31))
        self.ctcTrackUpO = QLabel(self.outputBox)
        self.ctcTrackUpO.setObjectName(u"ctcTrackUpO")
        self.ctcTrackUpO.setGeometry(QRect(280, 220, 101, 31))
        self.wayOccupiedO = QLabel(self.outputBox)
        self.wayOccupiedO.setObjectName(u"wayOccupiedO")
        self.wayOccupiedO.setGeometry(QRect(300, 340, 81, 31))
        self.train_people_boarding = QLCDNumber(self.outputBox)
        self.train_people_boarding.setObjectName(u"train_people_boarding")
        self.train_people_boarding.setGeometry(QRect(290, 140, 71, 31))
        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(410, 460, 261, 281))
        self.ctcTrackUpO_2 = QLabel(self.groupBox)
        self.ctcTrackUpO_2.setObjectName(u"ctcTrackUpO_2")
        self.ctcTrackUpO_2.setGeometry(QRect(20, 30, 261, 31))
        self.ambTemp = QLCDNumber(self.groupBox)
        self.ambTemp.setObjectName(u"ambTemp")
        self.ambTemp.setGeometry(QRect(80, 70, 91, 41))
        self.tempSelector = QLineEdit(self.groupBox)
        self.tempSelector.setObjectName(u"tempSelector")
        self.tempSelector.setGeometry(QRect(40, 140, 191, 22))
        self.ctcTrackUpO_3 = QLabel(self.groupBox)
        self.ctcTrackUpO_3.setObjectName(u"ctcTrackUpO_3")
        self.ctcTrackUpO_3.setGeometry(QRect(50, 110, 261, 31))
        self.tempSelectorValid = QLabel(self.groupBox)
        self.tempSelectorValid.setObjectName(u"tempSelectorValid")
        self.tempSelectorValid.setGeometry(QRect(110, 160, 81, 31))
        self.heaterToggleBTN = QPushButton(self.groupBox)
        self.heaterToggleBTN.setObjectName(u"heaterToggleBTN")
        self.heaterToggleBTN.setGeometry(QRect(20, 200, 101, 51))
        self.setTempBTN = QPushButton(self.groupBox)
        self.setTempBTN.setObjectName(u"setTempBTN")
        self.setTempBTN.setGeometry(QRect(140, 200, 101, 51))
        self.selTrackRailStat_2 = QLabel(self.groupBox)
        self.selTrackRailStat_2.setObjectName(u"selTrackRailStat_2")
        self.selTrackRailStat_2.setGeometry(QRect(180, 80, 55, 31))
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.label_18 = QLabel(self.tab_2)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(10, 10, 211, 61))
        self.lineEdit = QLineEdit(self.tab_2)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(20, 60, 113, 22))
        self.upTrackGreen = QRadioButton(self.tab_2)
        self.upTrackGreen.setObjectName(u"upTrackGreen")
        self.upTrackGreen.setGeometry(QRect(20, 130, 95, 20))
        self.upTrackGreen.setChecked(True)
        self.getTrackFileBTN = QPushButton(self.tab_2)
        self.getTrackFileBTN.setObjectName(u"getTrackFileBTN")
        self.getTrackFileBTN.setGeometry(QRect(20, 90, 111, 28))
        self.trackFileValid = QLabel(self.tab_2)
        self.trackFileValid.setObjectName(u"trackFileValid")
        self.trackFileValid.setGeometry(QRect(140, 60, 201, 31))
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.LineBox.setTitle(QCoreApplication.translate("Dialog", u"Green Line", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">Input Track Block Number</span></p></body></html>", None))
        self.getTrackBTN.setText(QCoreApplication.translate("Dialog", u"Get Track", None))
        self.trackSelectorValid.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">Valid</span></p></body></html>", None))
        self.trackBox.setTitle(QCoreApplication.translate("Dialog", u"Selected Track Status", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:11pt;\">\u2022 Track Section:</span></p><p><span style=\" font-size:11pt;\">\u2022 Track Switch:</span></p><p><span style=\" font-size:11pt;\">\u2022 Railway Crossing:</span></p><p><span style=\" font-size:11pt;\">\u2022 Rail Speed Limit:</span></p><p><span style=\" font-size:11pt;\">\u2022 Grade:</span></p><p><span style=\" font-size:11pt;\">\u2022 Track Heater Status:</span></p><p><span style=\" font-size:11pt;\">\u2022 Branch:</span></p><p><span style=\" font-size:11pt;\">\u2022 Station:</span></p><p><span style=\" font-size:11pt;\">\u2022 Station Side:</span></p><p><span style=\" font-size:11pt;\">\u2022 Underground:</span><br/></p><p><br/></p></body></html>", None))
        self.selTrackSW.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">&quot;No&quot;</span></p></body></html>", None))
        self.selTrackCross.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">&quot;No&quot;</span></p></body></html>", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">mph</span></p></body></html>", None))
        self.selTrackHeater.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">&quot;Off&quot;</span></p></body></html>", None))
        self.selTrackBranch.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">&quot;No&quot;</span></p></body></html>", None))
        self.trackStatusBox.setTitle(QCoreApplication.translate("Dialog", u"Track Status", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:11pt;\">\u2022 Rail Status:</span></p><p><span style=\" font-size:11pt;\">\u2022 Circuit Status:</span></p><p><span style=\" font-size:11pt;\">\u2022 Power Status:</span></p><p><br/></p><p><br/></p></body></html>", None))
        self.selTrackRailStat.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">&quot;OK&quot;</span></p></body></html>", None))
        self.selTrackCircStat.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">&quot;OK&quot;</span></p></body></html>", None))
        self.selTrackPowerStat.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">&quot;OK&quot;</span></p></body></html>", None))
        self.trackSignalBox.setTitle(QCoreApplication.translate("Dialog", u"Signals", None))
        self.sigGo.setText(QCoreApplication.translate("Dialog", u"Go", None))
        self.sigSlow.setText(QCoreApplication.translate("Dialog", u"Slow", None))
        self.sigStop.setText(QCoreApplication.translate("Dialog", u"Stop", None))
        self.selTrackSection.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">&quot;A&quot;</span></p></body></html>", None))
        self.selTrackGrade.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">&quot;0%&quot;</span></p></body></html>", None))
        self.selTrackStation.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">&quot;Station 1&quot;</span></p></body></html>", None))
        self.selTrackUnderground.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">&quot;No&quot;</span></p></body></html>", None))
        self.selTrackStationSide.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">&quot;Left/Right&quot;</span></p></body></html>", None))
        self.failBox.setTitle(QCoreApplication.translate("Dialog", u"Cause a Failure", None))
        self.breakRailBTN.setText(QCoreApplication.translate("Dialog", u"Toggle Break Rail", None))
        self.breakCircuitBTN.setText(QCoreApplication.translate("Dialog", u"Toggle Break Track Circuit", None))
        self.breakPowerBTN.setText(QCoreApplication.translate("Dialog", u"Toggle Break Power Line", None))
        self.waysideBox.setTitle(QCoreApplication.translate("Dialog", u"Wayside Status", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:11pt;\">\u2022 Commanded Speed:</span></p><p><span style=\" font-size:11pt;\">\u2022 Authroity:</span></p><p><span style=\" font-size:11pt;\">\u2022 Switch Position:</span></p><p><span style=\" font-size:11pt;\">\u2022 Signal:</span></p><p><br/></p></body></html>", None))
        self.waySwitch.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">North</span></p></body></html>", None))
        self.waySignal.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">Go</span></p></body></html>", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">mph</span></p></body></html>", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">ft</span></p></body></html>", None))
        self.waySwitchBTN.setText(QCoreApplication.translate("Dialog", u"Swap Switch", None))
        self.outputBox.setTitle(QCoreApplication.translate("Dialog", u"Outputs", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; text-decoration: underline;\">To Train:</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">\u2022 Speed Limit:</span></p><p><span style=\" font-size:10pt;\">\u2022 Authroity:</span></p><p><span style=\" font-size:10pt;\">\u2022 Beacon:</span></p><p><span style=\" font-size:10pt;\">\u2022 People Boarding:</span></p><p><span style=\" font-size:10pt;\"><br/></span></p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; text-decoration: underline;\">To CTC:</span></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">\u2022 Track Update Status:</span></p><p><span style=\" font-size:10pt;\">\u2022 Ticket Count:</span></p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; text-decoration: underline;\">To Wayside:</span></p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">\u2022 Occupied:</span></p><p><br/></p></body></html>", None))
        self.trainBeaconO.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">&quot;Station&quot;</span></p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">mph</span></p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">ft</span></p></body></html>", None))
        self.ctcTrackUpO.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">&quot;Updated&quot;</span></p></body></html>", None))
        self.wayOccupiedO.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">&quot;Open&quot;</span></p></body></html>", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Temperature Status and Controls", None))
        self.ctcTrackUpO_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; text-decoration: underline;\">Current Ambient Temperature:</span></p></body></html>", None))
        self.ctcTrackUpO_3.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; text-decoration: underline;\">Input Ambient Temp</span></p></body></html>", None))
        self.tempSelectorValid.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">Valid</span></p></body></html>", None))
        self.heaterToggleBTN.setText(QCoreApplication.translate("Dialog", u"Toggle Heater", None))
        self.setTempBTN.setText(QCoreApplication.translate("Dialog", u"Set Temp", None))
        self.selTrackRailStat_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-family:'Roboto,arial,sans-serif'; font-size:12pt; color:#4d5156; background-color:#ffffff;\">\u00b0F</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Green Line", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">Type Rail Document Name</span></p></body></html>", None))
        self.lineEdit.setText("")
        self.upTrackGreen.setText(QCoreApplication.translate("Dialog", u"Green Line", None))
        self.getTrackFileBTN.setText(QCoreApplication.translate("Dialog", u"Load", None))
        self.trackFileValid.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt;\">.</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"Track Editor", None))
    # retranslateUi

