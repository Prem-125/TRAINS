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
        TrackControllerUI.resize(579, 425)
        self.centralwidget = QWidget(TrackControllerUI)
        self.centralwidget.setObjectName(u"centralwidget")
        self.Program_2 = QTabWidget(self.centralwidget)
        self.Program_2.setObjectName(u"Program_2")
        self.Program_2.setGeometry(QRect(0, 0, 581, 441))
        self.Program_2.setAutoFillBackground(False)
        self.Program_2.setTabPosition(QTabWidget.North)
        self.Program_2.setTabShape(QTabWidget.Triangular)
        self.Program_2.setElideMode(Qt.ElideNone)
        self.Program_2.setUsesScrollButtons(True)
        self.Program_2.setDocumentMode(False)
        self.Program = QWidget()
        self.Program.setObjectName(u"Program")
        self.line_2 = QFrame(self.Program)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(0, 0, 821, 16))
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.label_2 = QLabel(self.Program)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 20, 231, 21))
        self.label_2.setFrameShape(QFrame.Box)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.ImportLine = QLineEdit(self.Program)
        self.ImportLine.setObjectName(u"ImportLine")
        self.ImportLine.setGeometry(QRect(10, 110, 113, 21))
        self.ImportButton = QPushButton(self.Program)
        self.ImportButton.setObjectName(u"ImportButton")
        self.ImportButton.setGeometry(QRect(130, 110, 111, 21))
        self.SuccessFailLine = QLabel(self.Program)
        self.SuccessFailLine.setObjectName(u"SuccessFailLine")
        self.SuccessFailLine.setGeometry(QRect(10, 130, 111, 21))
        self.SuccessFailLine.setAlignment(Qt.AlignCenter)
        self.label_3 = QLabel(self.Program)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 50, 111, 21))
        self.label_3.setFrameShape(QFrame.Box)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.ProgramLineBox = QComboBox(self.Program)
        self.ProgramLineBox.addItem("")
        self.ProgramLineBox.addItem("")
        self.ProgramLineBox.addItem("")
        self.ProgramLineBox.setObjectName(u"ProgramLineBox")
        self.ProgramLineBox.setGeometry(QRect(129, 50, 111, 22))
        self.label_4 = QLabel(self.Program)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 80, 111, 20))
        self.label_4.setFrameShape(QFrame.Box)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.ProgramControllerBox = QComboBox(self.Program)
        self.ProgramControllerBox.addItem("")
        self.ProgramControllerBox.setObjectName(u"ProgramControllerBox")
        self.ProgramControllerBox.setGeometry(QRect(130, 80, 111, 22))
        self.Program_2.addTab(self.Program, "")
        self.TrackStatus = QWidget()
        self.TrackStatus.setObjectName(u"TrackStatus")
        self.line = QFrame(self.TrackStatus)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(0, 0, 821, 16))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.BlockInput = QComboBox(self.TrackStatus)
        self.BlockInput.addItem("")
        self.BlockInput.setObjectName(u"BlockInput")
        self.BlockInput.setGeometry(QRect(170, 90, 81, 22))
        self.BlockInput.setEditable(False)
        self.BlockInput.setMaxVisibleItems(9)
        self.BlockInput.setModelColumn(0)
        self.label = QLabel(self.TrackStatus)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 90, 131, 21))
        self.label.setFrameShape(QFrame.Box)
        self.label.setAlignment(Qt.AlignCenter)
        self.label_6 = QLabel(self.TrackStatus)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(30, 120, 131, 21))
        self.label_6.setFrameShape(QFrame.Box)
        self.BlockStatus = QLabel(self.TrackStatus)
        self.BlockStatus.setObjectName(u"BlockStatus")
        self.BlockStatus.setGeometry(QRect(170, 120, 81, 21))
        self.BlockStatus.setFrameShape(QFrame.Box)
        self.label_7 = QLabel(self.TrackStatus)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(30, 150, 131, 21))
        self.label_7.setFrameShape(QFrame.Box)
        self.Occupancy = QLabel(self.TrackStatus)
        self.Occupancy.setObjectName(u"Occupancy")
        self.Occupancy.setGeometry(QRect(170, 150, 81, 21))
        self.Occupancy.setFrameShape(QFrame.Box)
        self.label_9 = QLabel(self.TrackStatus)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(30, 180, 131, 21))
        self.label_9.setFrameShape(QFrame.Box)
        self.Authority = QLabel(self.TrackStatus)
        self.Authority.setObjectName(u"Authority")
        self.Authority.setGeometry(QRect(170, 180, 81, 21))
        self.Authority.setFrameShape(QFrame.Box)
        self.label_11 = QLabel(self.TrackStatus)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(30, 210, 131, 21))
        self.label_11.setFrameShape(QFrame.Box)
        self.CommandedSpeed = QLabel(self.TrackStatus)
        self.CommandedSpeed.setObjectName(u"CommandedSpeed")
        self.CommandedSpeed.setGeometry(QRect(170, 210, 81, 21))
        self.CommandedSpeed.setFrameShape(QFrame.Box)
        self.label_13 = QLabel(self.TrackStatus)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(30, 240, 131, 21))
        self.label_13.setFrameShape(QFrame.Box)
        self.CrossingStatus = QLabel(self.TrackStatus)
        self.CrossingStatus.setObjectName(u"CrossingStatus")
        self.CrossingStatus.setGeometry(QRect(170, 240, 81, 21))
        self.CrossingStatus.setFrameShape(QFrame.Box)
        self.label_15 = QLabel(self.TrackStatus)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(30, 270, 131, 21))
        self.label_15.setFrameShape(QFrame.Box)
        self.SwitchStatus = QLabel(self.TrackStatus)
        self.SwitchStatus.setObjectName(u"SwitchStatus")
        self.SwitchStatus.setGeometry(QRect(170, 270, 81, 21))
        self.SwitchStatus.setFrameShape(QFrame.Box)
        self.label_5 = QLabel(self.TrackStatus)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(30, 30, 131, 21))
        self.label_5.setFrameShape(QFrame.Box)
        self.label_5.setAlignment(Qt.AlignCenter)
        self.StatusLineBox = QComboBox(self.TrackStatus)
        self.StatusLineBox.addItem("")
        self.StatusLineBox.addItem("")
        self.StatusLineBox.addItem("")
        self.StatusLineBox.setObjectName(u"StatusLineBox")
        self.StatusLineBox.setGeometry(QRect(170, 30, 81, 21))
        self.label_8 = QLabel(self.TrackStatus)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(30, 60, 131, 21))
        self.label_8.setFrameShape(QFrame.Box)
        self.label_8.setAlignment(Qt.AlignCenter)
        self.StatusControllerBox = QComboBox(self.TrackStatus)
        self.StatusControllerBox.addItem("")
        self.StatusControllerBox.setObjectName(u"StatusControllerBox")
        self.StatusControllerBox.setGeometry(QRect(170, 60, 81, 21))
        self.Program_2.addTab(self.TrackStatus, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.label_10 = QLabel(self.tab)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(30, 30, 131, 21))
        self.label_10.setFrameShape(QFrame.Box)
        self.label_10.setAlignment(Qt.AlignCenter)
        self.label_12 = QLabel(self.tab)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(30, 60, 131, 21))
        self.label_12.setFrameShape(QFrame.Box)
        self.label_12.setAlignment(Qt.AlignCenter)
        self.MainLineBox = QComboBox(self.tab)
        self.MainLineBox.addItem("")
        self.MainLineBox.addItem("")
        self.MainLineBox.addItem("")
        self.MainLineBox.setObjectName(u"MainLineBox")
        self.MainLineBox.setGeometry(QRect(169, 30, 81, 21))
        self.MainControllerBox = QComboBox(self.tab)
        self.MainControllerBox.addItem("")
        self.MainControllerBox.addItem("")
        self.MainControllerBox.addItem("")
        self.MainControllerBox.addItem("")
        self.MainControllerBox.addItem("")
        self.MainControllerBox.addItem("")
        self.MainControllerBox.addItem("")
        self.MainControllerBox.addItem("")
        self.MainControllerBox.setObjectName(u"MainControllerBox")
        self.MainControllerBox.setGeometry(QRect(170, 60, 81, 22))
        self.label_14 = QLabel(self.tab)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(30, 100, 431, 21))
        self.label_14.setFrameShape(QFrame.Box)
        self.label_14.setAlignment(Qt.AlignCenter)
        self.label_16 = QLabel(self.tab)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(30, 130, 131, 21))
        self.label_16.setFrameShape(QFrame.Box)
        self.label_16.setAlignment(Qt.AlignCenter)
        self.label_17 = QLabel(self.tab)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(30, 160, 131, 21))
        self.label_17.setFrameShape(QFrame.Box)
        self.label_17.setAlignment(Qt.AlignCenter)
        self.label_18 = QLabel(self.tab)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(30, 190, 131, 21))
        self.label_18.setFrameShape(QFrame.Box)
        self.label_18.setAlignment(Qt.AlignCenter)
        self.StemBox = QLabel(self.tab)
        self.StemBox.setObjectName(u"StemBox")
        self.StemBox.setGeometry(QRect(170, 130, 81, 21))
        self.StemBox.setFrameShape(QFrame.Box)
        self.StemBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.BranchABox = QLabel(self.tab)
        self.BranchABox.setObjectName(u"BranchABox")
        self.BranchABox.setGeometry(QRect(170, 160, 81, 21))
        self.BranchABox.setFrameShape(QFrame.Box)
        self.BranchABox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.BranchBBox = QLabel(self.tab)
        self.BranchBBox.setObjectName(u"BranchBBox")
        self.BranchBBox.setGeometry(QRect(170, 190, 81, 21))
        self.BranchBBox.setFrameShape(QFrame.Box)
        self.BranchBBox.setAlignment(Qt.AlignCenter)
        self.label_19 = QLabel(self.tab)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(270, 130, 111, 21))
        self.label_19.setFrameShape(QFrame.Box)
        self.label_19.setAlignment(Qt.AlignCenter)
        self.MainBranchCon = QLabel(self.tab)
        self.MainBranchCon.setObjectName(u"MainBranchCon")
        self.MainBranchCon.setGeometry(QRect(390, 130, 71, 21))
        self.MainBranchCon.setFrameShape(QFrame.Box)
        self.MainBranchCon.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.ToggleBranchButton = QPushButton(self.tab)
        self.ToggleBranchButton.setObjectName(u"ToggleBranchButton")
        self.ToggleBranchButton.setGeometry(QRect(270, 160, 191, 51))
        self.Program_2.addTab(self.tab, "")
        TrackControllerUI.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(TrackControllerUI)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 579, 22))
        TrackControllerUI.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(TrackControllerUI)
        self.statusbar.setObjectName(u"statusbar")
        TrackControllerUI.setStatusBar(self.statusbar)

        self.retranslateUi(TrackControllerUI)

        self.Program_2.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(TrackControllerUI)
    # setupUi

    def retranslateUi(self, TrackControllerUI):
        TrackControllerUI.setWindowTitle(QCoreApplication.translate("TrackControllerUI", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate("TrackControllerUI", u"PLC File", None))
        self.ImportLine.setText("")
        self.ImportButton.setText(QCoreApplication.translate("TrackControllerUI", u"Import", None))
        self.SuccessFailLine.setText(QCoreApplication.translate("TrackControllerUI", u"Invalid File", None))
        self.label_3.setText(QCoreApplication.translate("TrackControllerUI", u"Line", None))
        self.ProgramLineBox.setItemText(0, QCoreApplication.translate("TrackControllerUI", u"Choose", None))
        self.ProgramLineBox.setItemText(1, QCoreApplication.translate("TrackControllerUI", u"Green", None))
        self.ProgramLineBox.setItemText(2, QCoreApplication.translate("TrackControllerUI", u"Red", None))

        self.label_4.setText(QCoreApplication.translate("TrackControllerUI", u"Controller", None))
        self.ProgramControllerBox.setItemText(0, QCoreApplication.translate("TrackControllerUI", u"1", None))

        self.Program_2.setTabText(self.Program_2.indexOf(self.Program), QCoreApplication.translate("TrackControllerUI", u"Program", None))
        self.BlockInput.setItemText(0, QCoreApplication.translate("TrackControllerUI", u"Choose", None))

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
        self.label_5.setText(QCoreApplication.translate("TrackControllerUI", u"Line", None))
        self.StatusLineBox.setItemText(0, QCoreApplication.translate("TrackControllerUI", u"Choose", None))
        self.StatusLineBox.setItemText(1, QCoreApplication.translate("TrackControllerUI", u"Green", None))
        self.StatusLineBox.setItemText(2, QCoreApplication.translate("TrackControllerUI", u"Red", None))

        self.label_8.setText(QCoreApplication.translate("TrackControllerUI", u"Controller", None))
        self.StatusControllerBox.setItemText(0, QCoreApplication.translate("TrackControllerUI", u"Choose", None))

        self.Program_2.setTabText(self.Program_2.indexOf(self.TrackStatus), QCoreApplication.translate("TrackControllerUI", u"Controller Status", None))
        self.label_10.setText(QCoreApplication.translate("TrackControllerUI", u"Line", None))
        self.label_12.setText(QCoreApplication.translate("TrackControllerUI", u"Controller", None))
        self.MainLineBox.setItemText(0, QCoreApplication.translate("TrackControllerUI", u"Choose", None))
        self.MainLineBox.setItemText(1, QCoreApplication.translate("TrackControllerUI", u"Green", None))
        self.MainLineBox.setItemText(2, QCoreApplication.translate("TrackControllerUI", u"Red", None))

        self.MainControllerBox.setItemText(0, QCoreApplication.translate("TrackControllerUI", u"Choose", None))
        self.MainControllerBox.setItemText(1, QCoreApplication.translate("TrackControllerUI", u"1", None))
        self.MainControllerBox.setItemText(2, QCoreApplication.translate("TrackControllerUI", u"2", None))
        self.MainControllerBox.setItemText(3, QCoreApplication.translate("TrackControllerUI", u"3", None))
        self.MainControllerBox.setItemText(4, QCoreApplication.translate("TrackControllerUI", u"4", None))
        self.MainControllerBox.setItemText(5, QCoreApplication.translate("TrackControllerUI", u"5", None))
        self.MainControllerBox.setItemText(6, QCoreApplication.translate("TrackControllerUI", u"6", None))
        self.MainControllerBox.setItemText(7, QCoreApplication.translate("TrackControllerUI", u"7", None))

        self.label_14.setText(QCoreApplication.translate("TrackControllerUI", u"Switch Status", None))
        self.label_16.setText(QCoreApplication.translate("TrackControllerUI", u"Switch Stem", None))
        self.label_17.setText(QCoreApplication.translate("TrackControllerUI", u"Branch A", None))
        self.label_18.setText(QCoreApplication.translate("TrackControllerUI", u"Branch B", None))
        self.StemBox.setText("")
        self.BranchABox.setText("")
        self.BranchBBox.setText("")
        self.label_19.setText(QCoreApplication.translate("TrackControllerUI", u"Connecting Branch", None))
        self.MainBranchCon.setText("")
        self.ToggleBranchButton.setText(QCoreApplication.translate("TrackControllerUI", u"Toggle Connecting Branch", None))
        self.Program_2.setTabText(self.Program_2.indexOf(self.tab), QCoreApplication.translate("TrackControllerUI", u"Maintenance", None))
    # retranslateUi

