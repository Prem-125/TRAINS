﻿# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TrackControllerSW.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_TrackControllerUI(object):
    def setupUi(self, TrackControllerUI):
        if not TrackControllerUI.objectName():
            TrackControllerUI.setObjectName(u"TrackControllerUI")
        TrackControllerUI.setWindowModality(Qt.NonModal)
        TrackControllerUI.resize(486, 320)
        self.centralwidget = QWidget(TrackControllerUI)
        self.centralwidget.setObjectName(u"centralwidget")
        self.Program_2 = QTabWidget(self.centralwidget)
        self.Program_2.setObjectName(u"Program_2")
        self.Program_2.setGeometry(QRect(0, 0, 641, 441))
        self.Program_2.setAutoFillBackground(False)
        self.Program_2.setTabPosition(QTabWidget.North)
        self.Program_2.setTabShape(QTabWidget.Triangular)
        self.Program_2.setElideMode(Qt.ElideNone)
        self.Program_2.setUsesScrollButtons(True)
        self.Program_2.setDocumentMode(False)
        self.TrackStatus = QWidget()
        self.TrackStatus.setObjectName(u"TrackStatus")
        self.line = QFrame(self.TrackStatus)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(0, 0, 821, 16))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.BlockInput = QComboBox(self.TrackStatus)
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.addItem("")
        self.BlockInput.setObjectName(u"BlockInput")
        self.BlockInput.setGeometry(QRect(130, 20, 71, 22))
        self.BlockInput.setEditable(False)
        self.BlockInput.setMaxVisibleItems(9)
        self.BlockInput.setModelColumn(0)
        self.label = QLabel(self.TrackStatus)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 101, 21))
        self.label.setFrameShape(QFrame.Box)
        self.label_6 = QLabel(self.TrackStatus)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 50, 101, 21))
        self.label_6.setFrameShape(QFrame.Box)
        self.BlockStatus = QLabel(self.TrackStatus)
        self.BlockStatus.setObjectName(u"BlockStatus")
        self.BlockStatus.setGeometry(QRect(130, 50, 71, 21))
        self.BlockStatus.setFrameShape(QFrame.Box)
        self.label_7 = QLabel(self.TrackStatus)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 80, 101, 21))
        self.label_7.setFrameShape(QFrame.Box)
        self.Occupancy = QLabel(self.TrackStatus)
        self.Occupancy.setObjectName(u"Occupancy")
        self.Occupancy.setGeometry(QRect(130, 80, 71, 21))
        self.Occupancy.setFrameShape(QFrame.Box)
        self.label_9 = QLabel(self.TrackStatus)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(10, 110, 101, 21))
        self.label_9.setFrameShape(QFrame.Box)
        self.Authority = QLabel(self.TrackStatus)
        self.Authority.setObjectName(u"Authority")
        self.Authority.setGeometry(QRect(130, 110, 71, 21))
        self.Authority.setFrameShape(QFrame.Box)
        self.label_11 = QLabel(self.TrackStatus)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(10, 140, 101, 21))
        self.label_11.setFrameShape(QFrame.Box)
        self.CommandedSpeed = QLabel(self.TrackStatus)
        self.CommandedSpeed.setObjectName(u"CommandedSpeed")
        self.CommandedSpeed.setGeometry(QRect(130, 140, 71, 21))
        self.CommandedSpeed.setFrameShape(QFrame.Box)
        self.label_13 = QLabel(self.TrackStatus)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(10, 170, 101, 21))
        self.label_13.setFrameShape(QFrame.Box)
        self.CrossingStatus = QLabel(self.TrackStatus)
        self.CrossingStatus.setObjectName(u"CrossingStatus")
        self.CrossingStatus.setGeometry(QRect(130, 170, 71, 21))
        self.CrossingStatus.setFrameShape(QFrame.Box)
        self.label_15 = QLabel(self.TrackStatus)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(10, 200, 101, 21))
        self.label_15.setFrameShape(QFrame.Box)
        self.SwitchStatus = QLabel(self.TrackStatus)
        self.SwitchStatus.setObjectName(u"SwitchStatus")
        self.SwitchStatus.setGeometry(QRect(130, 200, 71, 21))
        self.SwitchStatus.setFrameShape(QFrame.Box)
        self.Program_2.addTab(self.TrackStatus, "")
        self.Program = QWidget()
        self.Program.setObjectName(u"Program")
        self.line_2 = QFrame(self.Program)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(0, 0, 821, 16))
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.label_2 = QLabel(self.Program)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 20, 51, 21))
        self.label_2.setFrameShape(QFrame.Box)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.ImportLine = QLineEdit(self.Program)
        self.ImportLine.setObjectName(u"ImportLine")
        self.ImportLine.setGeometry(QRect(10, 50, 113, 21))
        self.ImportButton = QPushButton(self.Program)
        self.ImportButton.setObjectName(u"ImportButton")
        self.ImportButton.setGeometry(QRect(130, 50, 111, 21))
        self.SuccessFailLine = QLabel(self.Program)
        self.SuccessFailLine.setObjectName(u"SuccessFailLine")
        self.SuccessFailLine.setGeometry(QRect(10, 80, 81, 16))
        self.Program_2.addTab(self.Program, "")
        TrackControllerUI.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(TrackControllerUI)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 486, 22))
        TrackControllerUI.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(TrackControllerUI)
        self.statusbar.setObjectName(u"statusbar")
        TrackControllerUI.setStatusBar(self.statusbar)

        self.retranslateUi(TrackControllerUI)

        self.Program_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(TrackControllerUI)
    # setupUi

    def retranslateUi(self, TrackControllerUI):
        TrackControllerUI.setWindowTitle(QCoreApplication.translate("TrackControllerUI", u"MainWindow", None))
        self.BlockInput.setItemText(0, QCoreApplication.translate("TrackControllerUI", u"Choose", None))
        self.BlockInput.setItemText(1, QCoreApplication.translate("TrackControllerUI", u"33", None))
        self.BlockInput.setItemText(2, QCoreApplication.translate("TrackControllerUI", u"34", None))
        self.BlockInput.setItemText(3, QCoreApplication.translate("TrackControllerUI", u"35", None))
        self.BlockInput.setItemText(4, QCoreApplication.translate("TrackControllerUI", u"36", None))
        self.BlockInput.setItemText(5, QCoreApplication.translate("TrackControllerUI", u"37", None))
        self.BlockInput.setItemText(6, QCoreApplication.translate("TrackControllerUI", u"38", None))
        self.BlockInput.setItemText(7, QCoreApplication.translate("TrackControllerUI", u"39", None))
        self.BlockInput.setItemText(8, QCoreApplication.translate("TrackControllerUI", u"40", None))
        self.BlockInput.setItemText(9, QCoreApplication.translate("TrackControllerUI", u"41", None))
        self.BlockInput.setItemText(10, QCoreApplication.translate("TrackControllerUI", u"42", None))
        self.BlockInput.setItemText(11, QCoreApplication.translate("TrackControllerUI", u"43", None))
        self.BlockInput.setItemText(12, QCoreApplication.translate("TrackControllerUI", u"44", None))
        self.BlockInput.setItemText(13, QCoreApplication.translate("TrackControllerUI", u"45", None))
        self.BlockInput.setItemText(14, QCoreApplication.translate("TrackControllerUI", u"46", None))
        self.BlockInput.setItemText(15, QCoreApplication.translate("TrackControllerUI", u"47", None))
        self.BlockInput.setItemText(16, QCoreApplication.translate("TrackControllerUI", u"48", None))
        self.BlockInput.setItemText(17, QCoreApplication.translate("TrackControllerUI", u"49", None))
        self.BlockInput.setItemText(18, QCoreApplication.translate("TrackControllerUI", u"50", None))
        self.BlockInput.setItemText(19, QCoreApplication.translate("TrackControllerUI", u"51", None))
        self.BlockInput.setItemText(20, QCoreApplication.translate("TrackControllerUI", u"52", None))
        self.BlockInput.setItemText(21, QCoreApplication.translate("TrackControllerUI", u"53", None))
        self.BlockInput.setItemText(22, QCoreApplication.translate("TrackControllerUI", u"54", None))
        self.BlockInput.setItemText(23, QCoreApplication.translate("TrackControllerUI", u"55", None))
        self.BlockInput.setItemText(24, QCoreApplication.translate("TrackControllerUI", u"56", None))
        self.BlockInput.setItemText(25, QCoreApplication.translate("TrackControllerUI", u"57", None))
        self.BlockInput.setItemText(26, QCoreApplication.translate("TrackControllerUI", u"58", None))
        self.BlockInput.setItemText(27, QCoreApplication.translate("TrackControllerUI", u"59", None))
        self.BlockInput.setItemText(28, QCoreApplication.translate("TrackControllerUI", u"60", None))
        self.BlockInput.setItemText(29, QCoreApplication.translate("TrackControllerUI", u"61", None))
        self.BlockInput.setItemText(30, QCoreApplication.translate("TrackControllerUI", u"62", None))
        self.BlockInput.setItemText(31, QCoreApplication.translate("TrackControllerUI", u"63", None))
        self.BlockInput.setItemText(32, QCoreApplication.translate("TrackControllerUI", u"64", None))
        self.BlockInput.setItemText(33, QCoreApplication.translate("TrackControllerUI", u"65", None))
        self.BlockInput.setItemText(34, QCoreApplication.translate("TrackControllerUI", u"66", None))
        self.BlockInput.setItemText(35, QCoreApplication.translate("TrackControllerUI", u"67", None))
        self.BlockInput.setItemText(36, QCoreApplication.translate("TrackControllerUI", u"68", None))
        self.BlockInput.setItemText(37, QCoreApplication.translate("TrackControllerUI", u"69", None))
        self.BlockInput.setItemText(38, QCoreApplication.translate("TrackControllerUI", u"70", None))
        self.BlockInput.setItemText(39, QCoreApplication.translate("TrackControllerUI", u"71", None))
        self.BlockInput.setItemText(40, QCoreApplication.translate("TrackControllerUI", u"72", None))
        self.BlockInput.setItemText(41, QCoreApplication.translate("TrackControllerUI", u"73", None))

        self.label.setText(QCoreApplication.translate("TrackControllerUI", u"Block Number", None))
        self.label_6.setText(QCoreApplication.translate("TrackControllerUI", u"Block Status", None))
        self.BlockStatus.setText("")
        self.label_7.setText(QCoreApplication.translate("TrackControllerUI", u"Occupancy", None))
        self.Occupancy.setText("")
        self.label_9.setText(QCoreApplication.translate("TrackControllerUI", u"Authority", None))
        self.Authority.setText("")
        self.label_11.setText(QCoreApplication.translate("TrackControllerUI", u"Commanded Speed", None))
        self.CommandedSpeed.setText("")
        self.label_13.setText(QCoreApplication.translate("TrackControllerUI", u"Crossing Signal", None))
        self.CrossingStatus.setText("")
        self.label_15.setText(QCoreApplication.translate("TrackControllerUI", u"Switch Status", None))
        self.SwitchStatus.setText("")
        self.Program_2.setTabText(self.Program_2.indexOf(self.TrackStatus), QCoreApplication.translate("TrackControllerUI", u"Track Status", None))
        self.label_2.setText(QCoreApplication.translate("TrackControllerUI", u"PLC File", None))
        self.ImportButton.setText(QCoreApplication.translate("TrackControllerUI", u"Import", None))
        self.SuccessFailLine.setText("")
        self.Program_2.setTabText(self.Program_2.indexOf(self.Program), QCoreApplication.translate("TrackControllerUI", u"Program", None))
    # retranslateUi

