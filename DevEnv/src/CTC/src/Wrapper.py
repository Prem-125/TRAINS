import sys
import time
from CTC.src.TransitSystem import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from CTC.src.UI import Ui_CTCOffice
from signals import signals



#Initialize track layout
BlueLine = Trackline("Blue", "./DevEnv/src/CTC/BlueLineLayout.xls", 0) #./BlueLineLayout.xls

#Declare Schedule
DemoSchedule = Schedule()

#Seconds global variable
gblSeconds = 0

#Define MainWindow class
class MainWindow(QMainWindow): #Subclass of QMainWindow

    #Constructor
    def __init__(self):
        #Call parent constructor
        super(MainWindow, self).__init__()
        self.ui = Ui_CTCOffice()
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
        self.ui.pushButton_13.clicked.connect(self.TrainInterface)
        self.ui.comboBox_10.currentTextChanged.connect(self.BlockInterfaceButtons)
        self.ui.pushButton_21.clicked.connect(self.BlockInterfaceDecide1)
        self.ui.pushButton_22.clicked.connect(self.BlockInterfaceDecide2)
        self.ui.pushButton_23.clicked.connect(self.SwitchInterface)
        self.ui.pushButton_19.clicked.connect(self.ComputeThroughput)
        self.utimer = QTimer()
        self.utimer.timeout.connect(self.timerCallback)
        self.utimer.start(1000)

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

        #Add train to track controller interface
        self.ui.comboBox_14.addItem(str(DemoSchedule.trainList[len(DemoSchedule.trainList)-1].getNumber()))

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

    def BlockClosureInterface(self, blockNumber):
        trackLine = self.ui.comboBox_2.currentText()

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

    #Method to reopen blocks
    def BlockReopenInterface(self, blockNumber):
        trackLine = self.ui.comboBox_4.currentText()

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


    #Method for train interface
    def TrainInterface(self):
        trainNumber = self.ui.comboBox_14.currentText()

        trainDestination = DemoSchedule.trainList[int(trainNumber)-1].getDestination()

        if(trainDestination == "Station B"):
            self.Authority = 10
        else:
            self.Authority = 15

        trainAuthority = BlueLine.stationList[int(trainNumber)].getAssocBlockNum()
        self.ui.label_85.setText("Authority: Block " + str(trainAuthority) )
        self.ui.label_83.setText("Suggested Speed: " + str(50) + "kph")

    #Method for block interface
    def BlockInterfaceButtons(self, inputText):
        blockObj = BlueLine.getBlock(int(inputText))

        #Initialize button functionality
        if(blockObj.getOccupancy() == 0):
            self.ui.pushButton_21.setText("Set Occupied")
        else:
            self.ui.pushButton_21.setText("Set Unoccupied")

        if(blockObj.getStatus() == 1):
            self.ui.pushButton_22.setText("Close Block")
        else:
            self.ui.pushButton_22.setText("Open Block")


    def BlockInterfaceDecide1(self):
        if(self.ui.pushButton_21.text() == "Set Occupied"):
            BlueLine.getBlock(int(self.ui.comboBox_10.currentText())).setOccupancy(1)
            self.ui.pushButton_21.setText("Set Unoccupied")
             #self.ui.label_37.setStyleSheet("background-color: rgb(55, 115, 255);")
        else:
            BlueLine.getBlock(int(self.ui.comboBox_10.currentText())).setOccupancy(0)
            self.ui.pushButton_21.setText("Set Occupied")


    def BlockInterfaceDecide2(self):
        blockNumber = self.ui.comboBox_10.currentText()

        if(self.ui.pushButton_22.text() == "Close Block"):
            BlueLine.CloseBlock(int(blockNumber))
            self.BlockClosureInterface(blockNumber)
            self.ui.pushButton_22.setText("Open Block")
            #self.ui.label_37.setStyleSheet("background-color: rgb(55, 115, 255);")
        else:
            BlueLine.OpenBlock(int(blockNumber))
            self.BlockReopenInterface(blockNumber)
            self.ui.pushButton_22.setText("Close Block")

            #self.ui.label_37.setStyleSheet("background-color: rgb(255, 142, 142);")


    #Method for switch interface
    def SwitchInterface(self):
        BlueLine.ToggleSwitchPosition(5)
        self.ui.label_30.setText("Block 5 to Block " + str(BlueLine.switchList[0].getCurrPosition()))

        if(self.ui.pushButton_23.text() == "Block 5 to Block 6"):
            self.ui.pushButton_23.setText("Block 5 to Block 11")
            self.ui.label_54.setStyleSheet("border: 2px solid black; font-weight: bold; background-color: rgb(238, 246, 255);")
            self.ui.label_54.setText("---")
            self.ui.label_53.setStyleSheet("border: 1px solid black; background-color: rgb(238, 246, 255);")
            self.ui.label_53.setText("")
            self.ui.label_55.setStyleSheet("border: 2px solid black; font-weight: bold; background-color: rgb(238, 246, 255);")
            self.ui.label_55.setText("---")
            self.ui.label_68.setStyleSheet("border: 1px solid black; background-color: rgb(238, 246, 255);")
            self.ui.label_68.setText("")
        else:
            self.ui.pushButton_23.setText("Block 5 to Block 6")
            self.ui.label_53.setStyleSheet("border: 2px solid black; font-weight: bold; background-color: rgb(238, 246, 255);")
            self.ui.label_53.setText("---")
            self.ui.label_54.setStyleSheet("border: 1px solid black; background-color: rgb(238, 246, 255);")
            self.ui.label_54.setText("")
            self.ui.label_68.setStyleSheet("border: 2px solid black; font-weight: bold; background-color: rgb(238, 246, 255);")
            self.ui.label_68.setText("---")
            self.ui.label_55.setStyleSheet("border: 1px solid black; background-color: rgb(238, 246, 255);")
            self.ui.label_55.setText("")

    def ComputeThroughput(self):
        global gblSeconds

        if(self.ui.lineEdit_2.text() == ''):
            BlueLine.stationList[0].setTicketSales = 0
        else:
            BlueLine.stationList[0].setTicketSales = int(self.ui.lineEdit_2.text())

        if(self.ui.lineEdit_3.text() == ''):
            BlueLine.stationList[1].setTicketSales = 0
        else:
            BlueLine.stationList[1].setTicketSales = int(self.ui.lineEdit_3.text())

        LineThroughput = (BlueLine.stationList[0].setTicketSales + BlueLine.stationList[1].setTicketSales) / (gblSeconds/3600)

        self.ui.label_7.setText(str(round(LineThroughput,2)))

    def timerCallback(self):
        global gblSeconds

        print("\n" + str(gblSeconds))
        gblSeconds += 1
        signals.test.emit(gblSeconds)
        if(gblSeconds % 10 == 0):
            self.ComputeThroughput()

        #Convert python time to excel time
        hour = int(gblSeconds / 3600)
        minute = int( (gblSeconds - 3600*hour)/60 )
        seconds = int(gblSeconds - 3600*hour - 60*minute)
        exlTime = str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':' + str(seconds).zfill(2)

        self.ui.label_74.setText("Time: " + exlTime)

        

        for trainObj in DemoSchedule.trainList:
            print("Departure Time: " + str(trainObj.getDepartureTime()))
            if(gblSeconds == trainObj.getDepartureTime()):
                self.ui.tableWidget_2.setItem(trainObj.getNumber(), 3, QTableWidgetItem("Dispatched"))

        self.utimer.start(1000)





        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())