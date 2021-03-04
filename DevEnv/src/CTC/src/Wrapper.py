import sys
import time
import TransitSystem
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from UI import Ui_MainWindow


#Initialize track layout
BlueLine = TransitSystem.Trackline("Blue", "BlueLineLayout.xls", 0)

#Declare Schedule
DemoSchedule = TransitSystem.Schedule()

#Define MainWindow class
class MainWindow(QMainWindow): #Subclass of QMainWindow

    #Constructor
    def __init__(self):
        #Call parent constructor
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Define user interactivity
        self.ui.pushButton.clicked.connect(self.setStackIndex0)
        self.ui.pushButton_2.clicked.connect(self.setStackIndex1)
        self.ui.pushButton_3.clicked.connect(self.setStackIndex2)
        self.ui.pushButton_6.clicked.connect(self.setStackIndex3)
        self.ui.pushButton_5.clicked.connect(self.ManualDispatch)
        self.ui.pushButton_4.clicked.connect(self.AutoDispatch)
        self.ui.pushButton_7.clicked.connect(self.BlockClosure)
        self.ui.pushButton_8.clicked.connect(self.BlockReopen)
        self.ui.pushButton_9.clicked.connect(self.SwitchFlip)
        self.ui.pushButton_10.clicked.connect(self.BlockInfo)

    #Methods to navigate central stacked widget
    def setStackIndex0(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def setStackIndex1(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def setStackIndex2(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def setStackIndex3(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    #Method to initiate manual dispatch
    def ManualDispatch(self):
        #Get station destination
        trainDestination = self.ui.comboBox.currentText()

        #Get arrival time
        recievedArrivalTime = self.ui.lineEdit.text()

        #Ensure that user specified a time
        if (recievedArrivalTime == ''):
            #ERROR WINDOW
            return

        #Convert excel time to python time
        #Parse arrival time
        parsedArrivalTime = recievedArrivalTime.split(':')
        hour = parsedArrivalTime[0]
        minute = parsedArrivalTime[1]
        second = parsedArrivalTime[2]
        trainArrivalTime = 3600*int(hour) + 60*int(minute) + int(second)

        #Add train to schedule
        DemoSchedule.addTrain(trainDestination, trainArrivalTime, BlueLine)

        #Populate transit schedule table
        numRows = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(numRows)
        self.ui.tableWidget.setItem(numRows, 0, QTableWidgetItem(recievedArrivalTime))
        self.ui.tableWidget.setItem(numRows, 1, QTableWidgetItem(trainDestination))
        self.ui.tableWidget.setItem(numRows, 2, QTableWidgetItem(BlueLine.getColor()))
        self.ui.tableWidget.setItem(numRows, 3, QTableWidgetItem(str(DemoSchedule.trainList[numRows].getNumber())))

        #Populate train status table
        numRows = self.ui.tableWidget_2.rowCount()
        self.ui.tableWidget_2.insertRow(numRows)
        self.ui.tableWidget_2.setItem(numRows, 0, QTableWidgetItem(str(DemoSchedule.trainList[numRows].getNumber())))
        self.ui.tableWidget_2.setItem(numRows, 1, QTableWidgetItem(trainDestination))
        self.ui.tableWidget_2.setItem(numRows, 2, QTableWidgetItem(BlueLine.getColor()))
        self.ui.tableWidget_2.setItem(numRows, 3, QTableWidgetItem("Yard"))
        self.ui.tableWidget_2.setItem(numRows, 4, QTableWidgetItem(recievedArrivalTime))

    #Method to initiate automatic dispatch
    def AutoDispatch(self):
        #Get schedule file from user
        #fileDialog will be of type tuple
        fileDialog = QFileDialog.getOpenFileName()

        #Access first fileDialog element to isolate schedule file path
        filePath = fileDialog[0]

        #Parse file name from file path
        parsedFilePath = filePath.split('/')
        fileName = parsedFilePath.pop()

        #Update last loaded schedule label
        self.ui.label_10.setText(fileName)

        DemoSchedule.AutoSchedule(fileName, 0)

        #Clear table contents
        self.ui.tableWidget.setRowCount(0)

        for trainObj in DemoSchedule.trainList:
            #Convert python time to excel time
            hour = int(trainObj.getArrivalTime() / 3600)
            minute = int( (trainObj.getArrivalTime() - 3600*hour)/60 )
            seconds = int(trainObj.getArrivalTime() - 3600*hour - 60*minute)
            exlTime = str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':' + str(seconds).zfill(2)

            #Populate transit schedule table
            numRows = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(numRows)
            self.ui.tableWidget.setItem(numRows, 0, QTableWidgetItem(exlTime))
            self.ui.tableWidget.setItem(numRows, 1, QTableWidgetItem(trainObj.getDestination()))
            self.ui.tableWidget.setItem(numRows, 2, QTableWidgetItem(BlueLine.getColor()))
            self.ui.tableWidget.setItem(numRows, 3, QTableWidgetItem(str(trainObj.getNumber())))

            #Populate train status table
            numRows = self.ui.tableWidget_2.rowCount()
            self.ui.tableWidget_2.insertRow(numRows)
            self.ui.tableWidget_2.setItem(numRows, 0, QTableWidgetItem(str(trainObj.getNumber())))
            self.ui.tableWidget_2.setItem(numRows, 1, QTableWidgetItem(trainObj.getDestination()))
            self.ui.tableWidget_2.setItem(numRows, 2, QTableWidgetItem(BlueLine.getColor()))
            self.ui.tableWidget_2.setItem(numRows, 3, QTableWidgetItem("Yard"))
            self.ui.tableWidget_2.setItem(numRows, 4, QTableWidgetItem(exlTime))


    #Method to update currently closed blocks
    def BlockClosure(self):
        trackLine = self.ui.comboBox_2.currentText()
        blockNumber = self.ui.comboBox_3.currentText()

        BlueLine.CloseBlock(int(blockNumber))

        numRows = self.ui.tableWidget_3.rowCount()
        self.ui.tableWidget_3.insertRow(numRows)
        self.ui.tableWidget_3.setItem(numRows, 0, QTableWidgetItem(trackLine))
        self.ui.tableWidget_3.setItem(numRows, 1, QTableWidgetItem(blockNumber))
        self.ui.tableWidget_3.sortItems(1)

        for i in range(0, self.ui.comboBox_3.count()):
            if (self.ui.comboBox_3.itemText(i) == blockNumber):
                self.ui.comboBox_3.removeItem(i)
                break

        self.ui.comboBox_5.addItem(blockNumber)

    #Method to reopen blocks
    def BlockReopen(self):
        trackLine = self.ui.comboBox_4.currentText()
        blockNumber = self.ui.comboBox_5.currentText()

        BlueLine.OpenBlock(int(blockNumber))

        for i in range(0, self.ui.tableWidget_3.rowCount()):
            #print("\n\nCell contents: " + self.ui.tableWidget_3.item(i,1).text())
            if(self.ui.tableWidget_3.item(i, 1).text() == blockNumber):
                self.ui.tableWidget_3.removeRow(i)
                break

        for j in range(0, self.ui.comboBox_5.count()):
            if (self.ui.comboBox_5.itemText(j) == blockNumber):
                self.ui.comboBox_5.removeItem(j)
                break

        self.ui.comboBox_3.addItem(blockNumber)

    #Method to flip switch
    def SwitchFlip(self):
        print("Block 5 Status: " + str(BlueLine.blockList[4].getStatus()))
        print("Block 6 Status: " + str(BlueLine.blockList[5].getStatus()))
        print("Block 11 Status: " + str(BlueLine.blockList[10].getStatus()))

        if(BlueLine.blockList[4].getStatus() == 0 or ((BlueLine.blockList[5].getStatus() == 0 and BlueLine.blockList[10].getStatus() == 0))):
            BlueLine.ToggleSwitchPosition(5)
            print(str(BlueLine.switchList[0].getCurrPosition()))
            self.ui.label_30.setText("Block 5 to Block " + str(BlueLine.switchList[0].getCurrPosition()))
        #else:
            #ERROR WINDOW

        if(BlueLine.switchList[0].getCurrPosition() == 6):
            self.ui.label_68.setStyleSheet("border: 2px solid black; font-weight: bold; background-color: rgb(238, 246, 255);")
            self.ui.label_68.setText("---")
            self.ui.label_55.setStyleSheet("border: 1px solid black; background-color: rgb(238, 246, 255);")
            self.ui.label_55.setText("")
        else:
            self.ui.label_55.setStyleSheet("border: 2px solid black; font-weight: bold; background-color: rgb(238, 246, 255);")
            self.ui.label_55.setText("---")
            self.ui.label_68.setStyleSheet("border: 1px solid black; background-color: rgb(238, 246, 255);")
            self.ui.label_68.setText("")

        return


    #Method for block info
    def BlockInfo(self):
        trackLine = self.ui.comboBox_6.currentText()
        blockNumber = self.ui.comboBox_7.currentText()

        blockObj = BlueLine.blockList[int(blockNumber)-1]

        self.ui.label_21.setText("Section: " + blockObj.getSection())
        self.ui.label_22.setText("Block Length: " + str(blockObj.getLength()*3.28) + " ft")
        self.ui.label_23.setText("Block Grade: " + str(blockObj.getGrade()) + " %")
        self.ui.label_24.setText("Speed Limit: " + str(blockObj.getSpeedLimit()*.621) + " mph")
        self.ui.label_25.setText("Cumulative Elevation: " + str(blockObj.getCumElevation()*3.28) + " ft")
        self.ui.label_26.setText("Occupancy: " + str(blockObj.getOccupancy()) )
        self.ui.label_27.setText("Status: " + str(blockObj.getStatus()) )

        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())