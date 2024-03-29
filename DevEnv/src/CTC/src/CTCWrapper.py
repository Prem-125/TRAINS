import sys
import time
from signals import signals
from CTC.src.UI import *
from CTC.src.CTCBackEnd import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

#Load in track layout
GreenLine = TrackLine("./TrackLayout.xls", 2)

RedLine = TrackLine("./TrackLayout.xls", 1)

#Declare a schedule object
CTCSchedule = Schedule()

"""
for blockObj in GreenLine.block_list:
    print("\nBlock " + str(blockObj.number) + " MinTraversalTime = " + str(blockObj.min_traveral_time) )
    
for switchObj in GreenLine.switch_list:
    print("\nSwitch: Root = " + str(switchObj.root) + " Branch1 = " + str(switchObj.branch_1) + " Branch2 = " + str(switchObj.branch_2))

for stationObj in GreenLine.station_list:
    print("\nStation: Root = " + str(stationObj.block_num) + " Name = " + str(stationObj.name) )

for blockObj in RedLine.block_list:
    print("\nBlock " + str(blockObj.number))
    
for switchObj in RedLine.switch_list:
    print("\nSwitch: Root = " + str(switchObj.root) + " Branch1 = " + str(switchObj.branch_1) + " Branch2 = " + str(switchObj.branch_2))

for stationObj in RedLine.station_list:
    print("\nStation: Root = " + str(stationObj.block_num) + " Name = " + str(stationObj.name) )
"""

#Define MainWindow class
class MainWindow(QMainWindow): #Subclass of QMainWindow

    #Constructor
    def __init__(self):
        #Call parent constructor
        super(MainWindow, self).__init__()
        self.ui = Ui_CTCOffice()
        self.ui.setupUi(self)

        #Define user navigation buttons over main stacked widget
        self.ui.StackControlButton1.clicked.connect(self.SetStack1Index0)
        self.ui.StackControlButton2.clicked.connect(self.SetStack1Index1)
        self.ui.StackControlButton3.clicked.connect(self.SetStack1Index2)

        #Define functionality of radio buttons and combo boxes in manual scheduler
        self.ui.StationRadioButton.clicked.connect(self.SetManDispStations)
        self.ui.BlockRadioButton.clicked.connect(self.SetManDispBlocks)
        self.ui.TrackComboBox1.currentTextChanged.connect(self.UpdateManDispDisplay)
        self.ui.AddDestButton.clicked.connect(self.UpdateDestList)

        #Define connection for manual dispatch button
        self.ui.ManDispButton.clicked.connect(self.GUIManualDispatch)
        #Define connection for automatic dispatch button
        self.ui.ImportSchedButton.clicked.connect(self.GUIAutoDispatch)

        #Define high-level functionality of Automatic and Manual group boxes
        self.ui.AutoGroupBox.clicked.connect(self.ExitAutoMode)
        self.ui.ManGroupBox.clicked.connect(self.EnterManMode)

        #Declare destination list for manual dispatch procedures
        self.dest_list = []

        #Define user navigation buttons in stacked widget of track map page
        self.ui.GreenLineButton1.clicked.connect(self.SetGreenMap)
        self.ui.RedLineButton1.clicked.connect(self.SetRedMap)
        self.ui.SectionComboBox1.currentTextChanged.connect(self.SetSectionBlocks)

        #Define track maintenance features
        self.ui.TrackComboBox2.currentTextChanged.connect(self.CloseTabTrackSections)
        self.ui.SectionComboBox2.currentTextChanged.connect(self.CloseTabTrackBlocks)
        self.ui.TrackComboBox3.currentTextChanged.connect(self.ReopenTabTrackSections)
        self.ui.SectionComboBox3.currentTextChanged.connect(self.ReopenTabTrackBlocks)
        
        self.ui.CloseBlockButton.clicked.connect(self.GUICloseBlock)
        self.ui.ReopenBlockButton.clicked.connect(self.GUIReopenBlock)

        #Define block status informational display
        self.ui.TrackComboBox4.currentTextChanged.connect(self.StatusTrackSections)
        self.ui.SectionComboBox4.currentTextChanged.connect(self.StatusTrackBlocks)
        #self.ui.BlockComboBox3.currentTextChanged.connect(self.UpdateBlockInfo)

        #Define switch status informational display
        self.ui.TrackComboBox5.currentTextChanged.connect(self.StatusSwitchNums)

        #Connect signal to obtain block closures from wayside controller
        signals.CTC_failure.connect(self.WaysideCloseBlock)

        #Define functionality of toggle switch when in maintenance mode
        self.ui.ToggleSwitchButton.clicked.connect(self.UpdateSwitchPos)

        #Initialize simulation speed to real time
        self.timer_interval = 1000
        #Define functionality for simulation speed slider
        self.ui.SimSpeedSlider.valueChanged.connect(self.GUISetSimSpeed)

        #Define button interaction to pause timer
        self.ui.PlayPauseButton.clicked.connect(self.PlayPauseSim)

        #Set global clock
        self.utimer = QTimer()
        self.utimer.timeout.connect(self.timerUpdate)
        self.utimer.start(self.timer_interval)

        #Initialize simulation timers
        self.gbl_seconds = 0

    #End constructor

    #Methods to navigate central stacked widget
    def SetStack1Index0(self):
        self.ui.StackedWidget1.setCurrentIndex(0)

    def SetStack1Index1(self):
        self.ui.StackedWidget1.setCurrentIndex(1)

    def SetStack1Index2(self):
        self.ui.StackedWidget1.setCurrentIndex(2)

    #Method to leave automatic mode
    def ExitAutoMode(self):
        #Display warning message box
        AutoExitMsg = QMessageBox()
        AutoExitMsg.setWindowTitle("Exiting Automatic Mode")
        AutoExitMsg.setText("WARNING: Are you sure you would like to disable automatic mode?\nOnce disabled, automatic mode cannot be reenabled.")
        AutoExitMsg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
        AutoExitMsg.setIcon(QMessageBox.Warning)

        AutoExitMsg.buttonClicked.connect(self.PopUpSelection)

        MsgWin = AutoExitMsg.exec()
    #End method

    #Method to respond to user selection in pop-up window for leaving automatic mode
    def PopUpSelection(self, response):
        if(response.text() == "Cancel"):
            self.ui.AutoGroupBox.setChecked(True)
            return
        else:
            self.ui.AutoGroupBox.setDisabled(True)
            self.ui.ManGroupBox.setChecked(True)
        #End if-else block
    #End method

    #Method to responsd to attempted modification of manual dispatch group checkbox
    def EnterManMode(self):
        if(self.ui.AutoGroupBox.isChecked() == True):
            #Display warning message box
            AutoExitMsg = QMessageBox()
            AutoExitMsg.setWindowTitle("Exiting Automatic Mode")
            AutoExitMsg.setText("WARNING: Are you sure you would like to disable automatic mode and enter manual mode?\nOnce disabled, automatic mode cannot be reenabled.")
            AutoExitMsg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
            AutoExitMsg.setIcon(QMessageBox.Warning)

            AutoExitMsg.buttonClicked.connect(self.PopUpSelection)

            MsgWin = AutoExitMsg.exec()
        else:
            #Display warning message box
            ManExitMsg = QMessageBox()
            ManExitMsg.setWindowTitle("Operational Mode Immutable")
            ManExitMsg.setText("ERROR: Once entered, manual mode cannot be disabled.")
            ManExitMsg.setIcon(QMessageBox.Critical)

            MsgWin = ManExitMsg.exec()

            self.ui.ManGroupBox.setChecked(True)
        #End if-else block
    #End method

    #Method to fill destination combo box with stations in manual scheduler
    def SetManDispStations(self):
        #Determine which track line is currently being viewed
        if(str(self.ui.TrackComboBox1.currentText()) == "Green"): #Green line is being viewed
            #Create list of Green line stations
            green_line_stations = ["Glenbury", "Dormont", "Mt Lebanon", "Poplar", "Castle Shannon", 
                                    "Overbrook", "Inglewood", "Central", "Whited", "Edgebrook", "Pioneer", "South Bank"]
            
            #Clear contents of destination combo box
            self.ui.DestComboBox1.clear()

            #Populate destination combo box
            for station_name in green_line_stations:
                self.ui.DestComboBox1.addItem(station_name)

        elif(str(self.ui.TrackComboBox1.currentText()) == "Red"): #Red line is being viewed
            #Create list of Red line stations
            red_line_stations = ["Shadyside", "Swissville", "Penn Station", "Steel Plaza",
                                 "First Ave", "Station Sqaure", "South Hills Junc."]

            #Clear contents of destination combo box
            self.ui.DestComboBox1.clear()

            #Populate destination combo box
            for station_name in red_line_stations:
                self.ui.DestComboBox1.addItem(station_name)

        #End if-elif block
    #End method

    #Method to fill destination combo box with blocks in manual scheduler
    def SetManDispBlocks(self):
        #Determine which track line is currently being viewed
        if(str(self.ui.TrackComboBox1.currentText()) == "Green"): #Green line is being viewed
            #Create list of Green line blocks
            green_line_blocks = list(range(1,151))

            #Clear contents of destination combo box
            self.ui.DestComboBox1.clear()

            #Populate destination combo box
            for block_num in green_line_blocks:
                self.ui.DestComboBox1.addItem(str(block_num))

        elif(str(self.ui.TrackComboBox1.currentText()) == "Red"): #Red line is being viewed
            #Create list of Green line blocks
            red_line_blocks = list(range(1,77))

            #Clear contents of destination combo box
            self.ui.DestComboBox1.clear()

            #Populate destination combo box
            for block_num in red_line_blocks:
                self.ui.DestComboBox1.addItem(str(block_num))
        
        #End if-elif block
    #End method

    #Method to update destination combo boxes in respose to changes in track line
    def UpdateManDispDisplay(self):
        #Determine which radio button is selected
        if(self.ui.StationRadioButton.isChecked()):
            self.SetManDispStations() 
        elif(self.ui.BlockRadioButton.isChecked()):
            self.SetManDispBlocks()
        #End if-else
    #End method

    #Method to update destination list in manual dispather
    def UpdateDestList(self):
        #Obtain train destination
        train_destination = str(self.ui.DestComboBox1.currentText())

        #Append to desination list
        self.dest_list.append(train_destination)

        #Update block closure list in maintenance mode of GUI
        numRows = self.ui.DestTable.rowCount()
        self.ui.DestTable.insertRow(numRows)
        self.ui.DestTable.setItem(numRows, 0, QTableWidgetItem(train_destination))
    #End method

    #Method to initiate manual dispatch and update scheduler accordingly
    def GUIManualDispatch(self):
        #Obtain track line on which train is to be dispatched
        track_line_name = str(self.ui.TrackComboBox1.currentText())

        #Clear destination table
        self.ui.DestTable.setRowCount(0)

        #Declare processed list to be returned to calling environment
        proc_block_list = []

        print("\n\nFULL DEST LIST")
        for dest_name in self.dest_list:
            print(dest_name)

        #Obtain train destinations from list
        if(track_line_name == "Green" and self.ui.StationRadioButton.isChecked()):
            #Create list of all track stations in the order they appear beginning at the yard
            dest_order = ["Glenbury", "Dormont", "Mt Lebanon", "Poplar", "Castle Shannon", "Mt Lebanon", "Dormont", "Glenbury", "Overbrook", "Inglewood", "Central",
                            "Whited", "Edgebrook", "Pioneer", "Whited", "South Bank", "Central", "Inglewood", "Overbrook"]

            #Declare list of passed stations as the ordered list is traversed
            prev_stations = []

            #Ensure destination list abides by track layout
            for destination_name in self.dest_list:
                print("Trying to find " + destination_name + " in dest_list")
                print("Length of destination ordered list: " + str(len(dest_order)))
                for dest_order_elem in dest_order:
                    print(dest_order_elem)

                if(destination_name in dest_order):
                    #Check if this is the second visitation of this station
                    if(destination_name in prev_stations):
                        if(destination_name == "Dormont"):
                            proc_block_list.append(105)
                        elif(destination_name == "Glenbury"):
                            proc_block_list.append(114)
                        elif(destination_name == "Overbrook"):
                            proc_block_list.append(57)
                        elif(destination_name == "Inglewood"):
                            proc_block_list.append(38)
                        elif(destination_name == "Central"):
                            proc_block_list.append(49)
                        elif(destination_name == "Mt Lebanon"):
                            proc_block_list.append(77)
                        elif(destination_name == "Whited"):
                            proc_block_list.append(22)
                        #End if-elif block
                    else:
                        if(destination_name == "Overbrook"):
                            proc_block_list.append(123)
                        elif(destination_name == "Inglewood"):
                            proc_block_list.append(132)
                        elif(destination_name == "Central"):
                            proc_block_list.append(141)
                        else:
                            for StationObj in GreenLine.station_list:
                                if(StationObj.name == destination_name.upper()):
                                    proc_block_list.append(StationObj.block_num)
                                    break
                                #End if
                            #End for loop
                        #End if-elif block
                    #End if-else block

                    #Determine position of station in ordered list
                    dest_pos = dest_order.index(destination_name) + 1

                    #Do not exceed bounds of list
                    if(dest_pos == len(dest_order)):
                        break

                    #Collect passed stations
                    prev_stations = prev_stations + dest_order[:dest_pos]

                    #Remove all list elements up to and including this station
                    del dest_order[:dest_pos]

                else:
                    #Create error message box
                    ClosureInfoMsg = QMessageBox()
                    ClosureInfoMsg.setWindowTitle("Dispatch Failed")
                    ClosureInfoMsg.setText("INFO: The specified destination list does not reflect the track layout")
                    ClosureInfoMsg.setIcon(QMessageBox.Critical)

                    MsgWin = ClosureInfoMsg.exec()

                    #Clear destination list
                    self.dest_list.clear()

                    return
                #End if-else block
            #End for loop
            
        elif(track_line_name == "Red" and self.ui.StationRadioButton.isChecked()):
            #Create list of all track stations in the order they appear beginning at the yard
            dest_order = ["Shadyside", "Herron Ave", "Swissville", "Penn Station", "Steel Plaza", "First Ave", "Station Square", "South Hills Junction",
                            "Station Square", "First Ave", "Steel Plaza", "Penn Station", "Swissville", "Herron Ave", "Shadyside"]

            #Declare list of passed stations as the ordered list is traversed
            prev_stations = []

            #Ensure destination list abides by track layout
            for destination_name in self.dest_list:
                print("Trying to find " + destination_name + " in dest_list")
                print("Length of destination ordered list: " + str(len(dest_order)))
                for dest_order_elem in dest_order:
                    print(dest_order_elem)
                if(destination_name in dest_order):
                    for StationObj in RedLine.station_list:
                        if(StationObj.name == destination_name.upper()):
                            proc_block_list.append(StationObj.block_num)
                            break
                        #End if
                    #End for loop

                    #Determine position of station in ordered list
                    dest_pos = dest_order.index(destination_name) + 1

                    #Do not exceed bounds of list
                    if(dest_pos == len(dest_order)):
                        break

                    #Collect passed stations
                    prev_stations = prev_stations + dest_order[:dest_pos]

                    #Remove all list elements up to and including this station
                    del dest_order[:dest_pos]

                else:
                    #Create error message box
                    ClosureInfoMsg = QMessageBox()
                    ClosureInfoMsg.setWindowTitle("Dispatch Failed")
                    ClosureInfoMsg.setText("INFO: The specified destination list does not reflect the track layout")
                    ClosureInfoMsg.setIcon(QMessageBox.Critical)

                    MsgWin = ClosureInfoMsg.exec()

                    #Clear destination list
                    self.dest_list.clear()

                    return
                #End if-else block
            #End for loop
        #End if-else block
            
        print("\nLength of processed list: " + str( len(proc_block_list) ) + "\n")

        #Obtain train arrival time
        input_time = str(self.ui.TimeLineEdit1.text())

        #Convert input time to seconds
        parsed_input_time = input_time.split(":")
        train_arrival_time = int(parsed_input_time[0])*3600 + int(parsed_input_time[1])*60 + int(parsed_input_time[2])

        print("\nBLOCK LIST")
        for dest_block in proc_block_list:
            print(str(dest_block))

        #Call back-end function for manual dispatch
        if(track_line_name == "Green"):
            dest_arrival_times = CTCSchedule.ManualSchedule(proc_block_list, train_arrival_time, GreenLine, self.gbl_seconds)
        if(track_line_name == "Red"):
            dest_arrival_times = CTCSchedule.ManualSchedule(proc_block_list, train_arrival_time, RedLine, self.gbl_seconds)

        print("\nLength of destination arrival times list is " + str(len(dest_arrival_times)))

        #If train could not be scheduled, display pop-up window and return to calling environment
        if(len(dest_arrival_times) == 0):
            #Create error message box
            ManDispFailMsg = QMessageBox()
            ManDispFailMsg.setWindowTitle("Dispatch Failed")
            ManDispFailMsg.setText("ERROR: The dispatch request could not be fullfilled\nThe specified arrival time cannot be achieved for the provided destinations.")
            ManDispFailMsg.setIcon(QMessageBox.Critical)

            MsgWin = ManDispFailMsg.exec()

            #Clear destination list
            self.dest_list.clear()

            return
        #End if

        #Obtain newly created train object as a temporary varialbe
        trainObj = CTCSchedule.train_list[-1]

        #Add train to scheduling table
        if(self.ui.StationRadioButton.isChecked()):
            for destination_name in self.dest_list:
                numRows = self.ui.SchedTable.rowCount()
                self.ui.SchedTable.insertRow(numRows)

                self.ui.SchedTable.setItem(numRows, 0, QTableWidgetItem(str(trainObj.number)))
                self.ui.SchedTable.setItem(numRows, 1, QTableWidgetItem(trainObj.HostTrackLine.color))
                self.ui.SchedTable.setItem(numRows, 2, QTableWidgetItem("Block " + str(trainObj.route_queue[0])))
                self.ui.SchedTable.setItem(numRows, 3, QTableWidgetItem(destination_name))

                #Convert seconds to display time
                backend_time = dest_arrival_times[self.dest_list.index(destination_name)]
                arrival_hours = int(backend_time/3600)
                arrival_minutes = int( (backend_time%3600)/60 )
                arrival_seconds = int( (backend_time%60) )
                display_time = str(arrival_hours).zfill(2) + ":" + str(arrival_minutes).zfill(2) + ":" + str(arrival_seconds).zfill(2)
                self.ui.SchedTable.setItem( numRows, 4, QTableWidgetItem(display_time) )
            #End for

        else:
            for block_destination in self.dest_list:
                numRows = self.ui.SchedTable.rowCount()
                self.ui.SchedTable.insertRow(numRows)

                self.ui.SchedTable.setItem(numRows, 0, QTableWidgetItem(str(trainObj.number)))
                self.ui.SchedTable.setItem(numRows, 1, QTableWidgetItem(trainObj.HostTrackLine.color))
                self.ui.SchedTable.setItem(numRows, 2, QTableWidgetItem("Block " + str(trainObj.route_queue[0])))
                self.ui.SchedTable.setItem(numRows, 3, QTableWidgetItem("Block " + str(block_destination)))
                
                #Convert seconds to display time
                backend_time = dest_arrival_times[self.dest_list.index(destination_name)]
                arrival_hours = int(backend_time/3600)
                arrival_minutes = int( (backend_time%3600)/60 )
                arrival_seconds = int( (backend_time%60) )
                display_time = str(arrival_hours).zfill(2) + ":" + str(arrival_minutes).zfill(2) + ":" + str(arrival_seconds).zfill(2)
                self.ui.SchedTable.setItem( numRows, 4, QTableWidgetItem(display_time) )
            #End for
        #End if-else block

        #Inform user of successful dispatch
        ManDispFailMsg = QMessageBox()
        ManDispFailMsg.setWindowTitle("Dispatch Fulfilled")
        ManDispFailMsg.setText("Dispatch request was successful.\nThe schedule has been updated accordingly.")
        ManDispFailMsg.setIcon(QMessageBox.Information)

        MsgWin = ManDispFailMsg.exec()

        #Clear destination list
        self.dest_list.clear()

        print("Train Number " + str(CTCSchedule.train_list[-1].number) )
        print("Train Destination: Block " + str(CTCSchedule.train_list[-1].destination_list[0]))
        print("Track Line: " + CTCSchedule.train_list[-1].HostTrackLine.color)
        print("Departure Time: " + str(CTCSchedule.train_list[-1].departure_time))
    #End method
    
    #Method to initiate automatic dispatch and update scheduler accordingly
    def GUIAutoDispatch(self):
        #Get schedule file from user
        #fileDialog will be of type tuple
        file_dialog = QFileDialog.getOpenFileName()

        #Access first fileDialog element to isolate schedule file path
        filepath = file_dialog[0]

        #Parse file name from file path
        parsed_filepath = filepath.split('/')
        file_name = parsed_filepath.pop()

        #Update last loaded schedule label
        self.ui.FileNameLabel.setText(file_name)

        #Call back-end function for automatic dispatch
        CTCSchedule.AutoSchedule(file_name, 1, GreenLine)

        print("Number of trains is " + str(len(CTCSchedule.train_list)))

        for trainObj in CTCSchedule.train_list:
            print("Number of final destinations is " + str(len(trainObj.destination_list)))
            #Loop through destinations of each train

            #Reset loop iterator
            iterator = 0

            print("\n\nTRAIN ARRIVAL TIMES IN GUI FUNCTION")

            for destination_block in trainObj.destination_list:

                print(str(trainObj.arrival_times[iterator]))

                numRows = self.ui.SchedTable.rowCount()
                self.ui.SchedTable.insertRow(numRows)

                self.ui.SchedTable.setItem(numRows, 0, QTableWidgetItem(str(trainObj.number)))
                self.ui.SchedTable.setItem(numRows, 1, QTableWidgetItem(trainObj.HostTrackLine.color))
                self.ui.SchedTable.setItem(numRows, 2, QTableWidgetItem("Block " + str(trainObj.route_queue[0])))

                if(iterator == 2):
                    self.ui.SchedTable.setItem(numRows, 3, QTableWidgetItem("LUIGI'S MANSION"))
                elif(iterator < 2):
                    self.ui.SchedTable.setItem(numRows, 3, QTableWidgetItem(trainObj.HostTrackLine.station_list[iterator].name))
                elif(iterator > 2):
                    self.ui.SchedTable.setItem(numRows, 3, QTableWidgetItem(trainObj.HostTrackLine.station_list[iterator-1].name))

                #Convert seconds to display time
                backend_time = trainObj.arrival_times[iterator]
                arrival_hours = int(backend_time/3600)
                arrival_minutes = int( (backend_time%3600)/60 )
                arrival_seconds = int( (backend_time%60) )
                display_time = str(arrival_hours).zfill(2) + ":" + str(arrival_minutes).zfill(2) + ":" + str(arrival_seconds).zfill(2)
                self.ui.SchedTable.setItem( numRows, 4, QTableWidgetItem(display_time) )

                #Increment iterator
                iterator += 1
            #End destination loop
        #End train loop

        #Inform user of successful dispatch
        AutoDispMsg = QMessageBox()
        AutoDispMsg.setWindowTitle("Dispatch Fulfilled")
        AutoDispMsg.setText("The imported schedule was succesfully processed.\nThe schedule has been updated accordingly.")
        AutoDispMsg.setIcon(QMessageBox.Information)

        MsgWin = AutoDispMsg.exec()
    #End method


    #Methods to modify map information
    def SetGreenMap(self):
        self.ui.StackedWidget2.setCurrentIndex(0)
        
        #Create list of Green track sections
        green_track_sections = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
                                "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

        #Clear contents of section combo box
        self.ui.SectionComboBox1.clear()

        #Populate section combo box
        for letter in green_track_sections:
            self.ui.SectionComboBox1.addItem(letter)
        
    def SetRedMap(self):
        self.ui.StackedWidget2.setCurrentIndex(1)

        #Create list of Red track sections
        red_track_sections = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                              "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"]
                            
        #Clear contents of section combo box
        self.ui.SectionComboBox1.clear()

        #Populate section combo box
        for letter in red_track_sections:
            self.ui.SectionComboBox1.addItem(letter)

    def SetSectionBlocks(self):
        #Check if the Green line or Red line is being view
        if(self.ui.StackedWidget2.currentIndex() == 0): #Green line is open
            #Print member blocks of selected track section
            if(self.ui.SectionComboBox1.currentText() == "A"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section A: 1-3")
            elif(self.ui.SectionComboBox1.currentText() == "B"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section B: 4-6")
            elif(self.ui.SectionComboBox1.currentText() == "C"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section C: 7-12")
            elif(self.ui.SectionComboBox1.currentText() == "D"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section D: 13-16")
            elif(self.ui.SectionComboBox1.currentText() == "E"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section E: 17-20")
            elif(self.ui.SectionComboBox1.currentText() == "F"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section F: 21-28")
            elif(self.ui.SectionComboBox1.currentText() == "G"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section G: 29-32")
            elif(self.ui.SectionComboBox1.currentText() == "H"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section H: 33-35")
            elif(self.ui.SectionComboBox1.currentText() == "I"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section I: 36-57")
            elif(self.ui.SectionComboBox1.currentText() == "J"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section J: 58-62")
            elif(self.ui.SectionComboBox1.currentText() == "K"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section K: 63-68")
            elif(self.ui.SectionComboBox1.currentText() == "L"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section L: 69-73")
            elif(self.ui.SectionComboBox1.currentText() == "M"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section M: 74-76")
            elif(self.ui.SectionComboBox1.currentText() == "N"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section N: 77-85")
            elif(self.ui.SectionComboBox1.currentText() == "O"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section O: 86-88")
            elif(self.ui.SectionComboBox1.currentText() == "P"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section P: 89-97")
            elif(self.ui.SectionComboBox1.currentText() == "Q"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section Q: 98-100")
            elif(self.ui.SectionComboBox1.currentText() == "R"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section R: 101")
            elif(self.ui.SectionComboBox1.currentText() == "S"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section S: 102-104")
            elif(self.ui.SectionComboBox1.currentText() == "T"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section T: 105-109")
            elif(self.ui.SectionComboBox1.currentText() == "U"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section U: 110-116")
            elif(self.ui.SectionComboBox1.currentText() == "V"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section V: 117-121")
            elif(self.ui.SectionComboBox1.currentText() == "W"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section W: 122-143")
            elif(self.ui.SectionComboBox1.currentText() == "X"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section X: 144-146")
            elif(self.ui.SectionComboBox1.currentText() == "Y"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section Y: 147-149")
            elif(self.ui.SectionComboBox1.currentText() == "Z"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section Z: 150")
            #End track section if-elif block
        
        elif(self.ui.StackedWidget2.currentIndex() == 1): #Red line is open
            #Print member blocks of selected track section
            if(self.ui.SectionComboBox1.currentText() == "A"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section A: 1-3")
            elif(self.ui.SectionComboBox1.currentText() == "B"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section B: 4-6")
            elif(self.ui.SectionComboBox1.currentText() == "C"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section C: 7-9")
            elif(self.ui.SectionComboBox1.currentText() == "D"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section D: 10-12")
            elif(self.ui.SectionComboBox1.currentText() == "E"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section E: 13-15")
            elif(self.ui.SectionComboBox1.currentText() == "F"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section F: 16-20")
            elif(self.ui.SectionComboBox1.currentText() == "G"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section G: 21-23")
            elif(self.ui.SectionComboBox1.currentText() == "H"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section H: 24-45")
            elif(self.ui.SectionComboBox1.currentText() == "I"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section I: 46-48")
            elif(self.ui.SectionComboBox1.currentText() == "J"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section J: 49-54")
            elif(self.ui.SectionComboBox1.currentText() == "K"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section K: 55-57")
            elif(self.ui.SectionComboBox1.currentText() == "L"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section L: 58-60")
            elif(self.ui.SectionComboBox1.currentText() == "M"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section M: 61-63")
            elif(self.ui.SectionComboBox1.currentText() == "N"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section N: 64-66")
            elif(self.ui.SectionComboBox1.currentText() == "O"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section O: 67")
            elif(self.ui.SectionComboBox1.currentText() == "P"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section P: 68-70")
            elif(self.ui.SectionComboBox1.currentText() == "Q"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section Q: 71")
            elif(self.ui.SectionComboBox1.currentText() == "R"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section R: 72")
            elif(self.ui.SectionComboBox1.currentText() == "S"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section S: 73-75")
            elif(self.ui.SectionComboBox1.currentText() == "T"):
                self.ui.SectionBlocksLabel.setText("Blocks in Section T: 76")

        #End track line if-elif block

    #Method to update global clock
    def timerUpdate(self):
        #Increment seconds after timeout 
        self.gbl_seconds += 1

        #Emit seconds to all modules/functions
        signals.time_signal.emit(self.gbl_seconds, self.timer_interval)

        #Convert seconds to hours:minutes:seconds
        hour = int(self.gbl_seconds / 3600)
        minute = int( (self.gbl_seconds%3600)/60 )
        seconds = int(self.gbl_seconds%60)
        gui_time = str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':' + str(seconds).zfill(2)

        #Print updated time to GUI
        self.ui.SysTimeLabel.setText("Time: " + gui_time)

        #Check if a scheduled train needs to be dispatched
        CTCSchedule.CheckForDispatch(self.gbl_seconds)

        #Display throughput to GUI
        self.DisplayThroughput(self.gbl_seconds)

        #Update train positions on schedule table
        self.UpdateTrainPositions()

        #Update block information in block status group of maintenance mode
        self.UpdateBlockInfo()

        #Update switch information in switch status group of maintenance mode
        self.UpdateSwitchInfo()

        #Restart timout period
        self.utimer.start(self.timer_interval)
    #End method

    #Method to set track section combo box in closure tab of maintenance mode
    def CloseTabTrackSections(self):
        #Determine which track line is currently being viewed
        if(str(self.ui.TrackComboBox2.currentText()) == "Green"): #Green line is being viewed
            #Create list of Green track sections
            green_track_sections = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
                                    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

            #Clear contents of section combo box
            self.ui.SectionComboBox2.clear()

            #Populate section combo box
            for letter in green_track_sections:
                self.ui.SectionComboBox2.addItem(letter)

        elif(str(self.ui.TrackComboBox2.currentText()) == "Red"): #Red line is being viewed
            #Create list of Red track sections
            red_track_sections = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                                  "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"]
                                
            #Clear contents of section combo box
            self.ui.SectionComboBox2.clear()

            #Populate section combo box
            for letter in red_track_sections:
                self.ui.SectionComboBox2.addItem(letter)
        #End if-else block
    #End method

    #Method to set track block combo box in closure tab of maintenance mode
    def CloseTabTrackBlocks(self):
        #Check if the Green line or Red line is being viewed
        if(str(self.ui.TrackComboBox2.currentText()) == "Green"): #Green line is open
            #Print member blocks of selected track section
            if(str(self.ui.SectionComboBox2.currentText()) == "A"):
                self.ui.BlockComboBox1.clear()
                for i in range(1, 4):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "B"):
                self.ui.BlockComboBox1.clear()
                for i in range(4, 7):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "C"):
                self.ui.BlockComboBox1.clear()
                for i in range(7, 13):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "D"):
                self.ui.BlockComboBox1.clear()
                for i in range(13, 17):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "E"):
                self.ui.BlockComboBox1.clear()
                for i in range(17, 21):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "F"):
                self.ui.BlockComboBox1.clear()
                for i in range(21, 29):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "G"):
                self.ui.BlockComboBox1.clear()
                for i in range(29, 33):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "H"):
                self.ui.BlockComboBox1.clear()
                for i in range(33, 36):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "I"):
                self.ui.BlockComboBox1.clear()
                for i in range(36, 58):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "J"):
                self.ui.BlockComboBox1.clear()
                for i in range(58, 63):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "K"):
                self.ui.BlockComboBox1.clear()
                for i in range(63, 69):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "L"):
                self.ui.BlockComboBox1.clear()
                for i in range(69, 74):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "M"):
                self.ui.BlockComboBox1.clear()
                for i in range(74, 77):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "N"):
                self.ui.BlockComboBox1.clear()
                for i in range(77, 86):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "O"):
                self.ui.BlockComboBox1.clear()
                for i in range(86, 89):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "P"):
                self.ui.BlockComboBox1.clear()
                for i in range(89, 98):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "Q"):
                self.ui.BlockComboBox1.clear()
                for i in range(98, 101):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "R"):
                self.ui.BlockComboBox1.clear()
                self.ui.BlockComboBox1.addItem(str(101))
            elif(str(self.ui.SectionComboBox2.currentText()) == "S"):
                self.ui.BlockComboBox1.clear()
                for i in range(102, 105):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "T"):
                self.ui.BlockComboBox1.clear()
                for i in range(105, 110):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "U"):
                self.ui.BlockComboBox1.clear()
                for i in range(110, 117):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "V"):
                self.ui.BlockComboBox1.clear()
                for i in range(117, 122):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "W"):
                self.ui.BlockComboBox1.clear()
                for i in range(122, 144):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "X"):
                self.ui.BlockComboBox1.clear()
                for i in range(144, 147):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "Y"):
                self.ui.BlockComboBox1.clear()
                for i in range(147, 150):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "Z"):
                self.ui.BlockComboBox1.clear()
                self.ui.BlockComboBox1.addItem(str(150))
            #End track section if-elif block
        
        elif(str(self.ui.TrackComboBox2.currentText()) == "Red"): #Red line is open
            #Print member blocks of selected track section
            if(str(self.ui.SectionComboBox2.currentText()) == "A"):
                self.ui.BlockComboBox1.clear()
                for i in range(1, 4):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "B"):
                self.ui.BlockComboBox1.clear()
                for i in range(4, 7):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "C"):
                self.ui.BlockComboBox1.clear()
                for i in range(7, 10):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "D"):
                self.ui.BlockComboBox1.clear()
                for i in range(10, 13):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "E"):
                self.ui.BlockComboBox1.clear()
                for i in range(13, 16):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "F"):
                self.ui.BlockComboBox1.clear()
                for i in range(16, 21):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "G"):
                self.ui.BlockComboBox1.clear()
                for i in range(21, 24):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "H"):
                self.ui.BlockComboBox1.clear()
                for i in range(24, 46):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "I"):
                self.ui.BlockComboBox1.clear()
                for i in range(46, 49):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "J"):
                self.ui.BlockComboBox1.clear()
                for i in range(49, 55):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "K"):
                self.ui.BlockComboBox1.clear()
                for i in range(55, 58):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "L"):
                self.ui.BlockComboBox1.clear()
                for i in range(58, 61):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "M"):
                self.ui.BlockComboBox1.clear()
                for i in range(61, 64):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "N"):
                self.ui.BlockComboBox1.clear()
                for i in range(64, 67):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "O"):
                self.ui.BlockComboBox1.clear()
                self.ui.BlockComboBox1.addItem(str(67))
            elif(str(self.ui.SectionComboBox2.currentText()) == "P"):
                self.ui.BlockComboBox1.clear()
                for i in range(68, 71):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "Q"):
                self.ui.BlockComboBox1.clear()
                self.ui.BlockComboBox1.addItem(str(71))
            elif(str(self.ui.SectionComboBox2.currentText()) == "R"):
                self.ui.BlockComboBox1.clear()
                self.ui.BlockComboBox1.addItem(str(72))
            elif(str(self.ui.SectionComboBox2.currentText()) == "S"):
                self.ui.BlockComboBox1.clear()
                for i in range(73, 76):
                    self.ui.BlockComboBox1.addItem(str(i))
            elif(str(self.ui.SectionComboBox2.currentText()) == "T"):
                self.ui.BlockComboBox1.clear()
                self.ui.BlockComboBox1.addItem(str(76))
        #End track line if-elif block
    #End Method

    #Method to set track section combo box in reopen tab of maintenance mode
    def ReopenTabTrackSections(self):
        #Determine which track line is currently being viewed
        if(str(self.ui.TrackComboBox3.currentText()) == "Green"): #Green line is being view
            #Create list of Green track sections
            green_track_sections = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
                                    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

            #Clear contents of section combo box
            self.ui.SectionComboBox3.clear()

            #Populate section combo box
            for letter in green_track_sections:
                self.ui.SectionComboBox3.addItem(letter)

        elif(str(self.ui.TrackComboBox3.currentText()) == "Red"): #Red line is being viewed
            #Create list of Red track sections
            red_track_sections = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                                  "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"]
                                
            #Clear contents of section combo box
            self.ui.SectionComboBox3.clear()

            #Populate section combo box
            for letter in red_track_sections:
                self.ui.SectionComboBox3.addItem(letter)
        #End if-else block
    #End method

    #Method to set track block combo box in reopen tab of maintenance mode
    def ReopenTabTrackBlocks(self):
        #Check if the Green line or Red line is being viewed
        if(str(self.ui.TrackComboBox3.currentText()) == "Green"): #Green line is open
            #Print member blocks of selected track section
            if(str(self.ui.SectionComboBox3.currentText()) == "A"):
                self.ui.BlockComboBox2.clear()
                for i in range(1, 4):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "B"):
                self.ui.BlockComboBox2.clear()
                for i in range(4, 7):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "C"):
                self.ui.BlockComboBox2.clear()
                for i in range(7, 13):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "D"):
                self.ui.BlockComboBox2.clear()
                for i in range(13, 17):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "E"):
                self.ui.BlockComboBox2.clear()
                for i in range(17, 21):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "F"):
                self.ui.BlockComboBox2.clear()
                for i in range(21, 29):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "G"):
                self.ui.BlockComboBox2.clear()
                for i in range(29, 33):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "H"):
                self.ui.BlockComboBox2.clear()
                for i in range(33, 36):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "I"):
                self.ui.BlockComboBox2.clear()
                for i in range(36, 58):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "J"):
                self.ui.BlockComboBox2.clear()
                for i in range(58, 63):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "K"):
                self.ui.BlockComboBox2.clear()
                for i in range(63, 69):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "L"):
                self.ui.BlockComboBox2.clear()
                for i in range(69, 74):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "M"):
                self.ui.BlockComboBox2.clear()
                for i in range(74, 77):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "N"):
                self.ui.BlockComboBox2.clear()
                for i in range(77, 86):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "O"):
                self.ui.BlockComboBox2.clear()
                for i in range(86, 89):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "P"):
                self.ui.BlockComboBox2.clear()
                for i in range(89, 98):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "Q"):
                self.ui.BlockComboBox2.clear()
                for i in range(98, 101):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "R"):
                self.ui.BlockComboBox2.clear()
                self.ui.BlockComboBox2.addItem(str(101))
            elif(str(self.ui.SectionComboBox3.currentText()) == "S"):
                self.ui.BlockComboBox2.clear()
                for i in range(102, 105):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "T"):
                self.ui.BlockComboBox2.clear()
                for i in range(105, 110):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "U"):
                self.ui.BlockComboBox2.clear()
                for i in range(110, 117):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "V"):
                self.ui.BlockComboBox2.clear()
                for i in range(117, 122):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "W"):
                self.ui.BlockComboBox2.clear()
                for i in range(122, 144):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "X"):
                self.ui.BlockComboBox2.clear()
                for i in range(144, 147):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "Y"):
                self.ui.BlockComboBox2.clear()
                for i in range(147, 150):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "Z"):
                self.ui.BlockComboBox2.clear()
                self.ui.BlockComboBox2.addItem(str(150))
            #End track section if-elif block
        
        elif(str(self.ui.TrackComboBox3.currentText()) == "Red"): #Red line is open
            #Print member blocks of selected track section
            if(str(self.ui.SectionComboBox3.currentText()) == "A"):
                self.ui.BlockComboBox2.clear()
                for i in range(1, 4):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "B"):
                self.ui.BlockComboBox2.clear()
                for i in range(4, 7):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "C"):
                self.ui.BlockComboBox2.clear()
                for i in range(7, 10):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "D"):
                self.ui.BlockComboBox2.clear()
                for i in range(10, 13):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "E"):
                self.ui.BlockComboBox2.clear()
                for i in range(13, 16):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "F"):
                self.ui.BlockComboBox2.clear()
                for i in range(16, 21):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "G"):
                self.ui.BlockComboBox2.clear()
                for i in range(21, 24):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "H"):
                self.ui.BlockComboBox2.clear()
                for i in range(24, 46):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "I"):
                self.ui.BlockComboBox2.clear()
                for i in range(46, 49):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "J"):
                self.ui.BlockComboBox2.clear()
                for i in range(49, 55):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "K"):
                self.ui.BlockComboBox2.clear()
                for i in range(55, 58):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "L"):
                self.ui.BlockComboBox2.clear()
                for i in range(58, 61):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "M"):
                self.ui.BlockComboBox2.clear()
                for i in range(61, 64):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "N"):
                self.ui.BlockComboBox2.clear()
                for i in range(64, 67):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "O"):
                self.ui.BlockComboBox2.clear()
                self.ui.BlockComboBox2.addItem(str(67))
            elif(str(self.ui.SectionComboBox3.currentText()) == "P"):
                self.ui.BlockComboBox2.clear()
                for i in range(68, 71):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "Q"):
                self.ui.BlockComboBox2.clear()
                self.ui.BlockComboBox2.addItem(str(71))
            elif(str(self.ui.SectionComboBox3.currentText()) == "R"):
                self.ui.BlockComboBox2.clear()
                self.ui.BlockComboBox2.addItem(str(72))
            elif(str(self.ui.SectionComboBox3.currentText()) == "S"):
                self.ui.BlockComboBox2.clear()
                for i in range(73, 76):
                    self.ui.BlockComboBox2.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "T"):
                self.ui.BlockComboBox2.clear()
                self.ui.BlockComboBox2.addItem(str(76))
        #End track line if-elif block
    #End Method

    #Method to set track section combo box in block status group of maintenance mode
    def StatusTrackSections(self):
        #Determine which track line is currently being viewed
        if(str(self.ui.TrackComboBox4.currentText()) == "Green"): #Green line is being view
            #Create list of Green track sections
            green_track_sections = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
                                    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

            #Clear contents of section combo box
            self.ui.SectionComboBox4.clear()

            #Populate section combo box
            for letter in green_track_sections:
                self.ui.SectionComboBox4.addItem(letter)

        elif(str(self.ui.TrackComboBox4.currentText()) == "Red"): #Red line is being viewed
            #Create list of Red track sections
            red_track_sections = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                                  "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"]
                                
            #Clear contents of section combo box
            self.ui.SectionComboBox4.clear()

            #Populate section combo box
            for letter in red_track_sections:
                self.ui.SectionComboBox4.addItem(letter)
        #End if-else block

        '''
        #Evaluate block display
        if(str(self.ui.SectionComboBox4.currentText()) != '' and str(self.ui.BlockComboBox3.currentText()) != ''):
            if(str(self.ui.TrackComboBox4.currentText()) == "Green"):
                #Obtain block number
                block_num = int(self.ui.BlockComboBox3.currentText())
                #Retrieve block object
                blockObj = GreenLine.block_list[block_num-1]

                self.ui.BlockSectionLabel.setText("Section: " + blockObj.section)
                self.ui.BlockLengthLabel.setText("Block Length: " + str(blockObj.length))
                self.ui.SpeedLimitLabel.setText("Speed Limit: " + str(blockObj.speed_limit))
                self.ui.OccupancyLabel.setText("Occupancy: " + str(blockObj.occupancy))
                self.ui.BlockStatusLabel.setText("Status: " + str(blockObj.status))

            elif(str(self.ui.TrackComboBox4.currentText()) == "Red"):
                #Obtain block number
                block_num = int(self.ui.BlockComboBox3.currentText())
                #Retrieve block object
                blockObj = RedLine.block_list[block_num-1]

                self.ui.BlockSectionLabel.setText("Section: " + blockObj.section)
                self.ui.BlockLengthLabel.setText("Block Length: " + str(blockObj.length))
                self.ui.SpeedLimitLabel.setText("Speed Limit: " + str(blockObj.speed_limit))
                self.ui.OccupancyLabel.setText("Occupancy: " + str(blockObj.occupancy))
                self.ui.BlockStatusLabel.setText("Status: " + str(blockObj.status))
            #End if
        #End if
        '''
    #End method

    #Method to set track block combo box in block status group of maintenance mode
    def StatusTrackBlocks(self):
        #Check if the Green line or Red line is being viewed
        if(str(self.ui.TrackComboBox4.currentText()) == "Green"): #Green line is open
            #Print member blocks of selected track section
            if(str(self.ui.SectionComboBox4.currentText()) == "A"):
                self.ui.BlockComboBox3.clear()
                for i in range(1, 4):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "B"):
                self.ui.BlockComboBox3.clear()
                for i in range(4, 7):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "C"):
                self.ui.BlockComboBox3.clear()
                for i in range(7, 13):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "D"):
                self.ui.BlockComboBox3.clear()
                for i in range(13, 17):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "E"):
                self.ui.BlockComboBox3.clear()
                for i in range(17, 21):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "F"):
                self.ui.BlockComboBox3.clear()
                for i in range(21, 29):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "G"):
                self.ui.BlockComboBox3.clear()
                for i in range(29, 33):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "H"):
                self.ui.BlockComboBox3.clear()
                for i in range(33, 36):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "I"):
                self.ui.BlockComboBox3.clear()
                for i in range(36, 58):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "J"):
                self.ui.BlockComboBox3.clear()
                for i in range(58, 63):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "K"):
                self.ui.BlockComboBox3.clear()
                for i in range(63, 69):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "L"):
                self.ui.BlockComboBox3.clear()
                for i in range(69, 74):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "M"):
                self.ui.BlockComboBox3.clear()
                for i in range(74, 77):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "N"):
                self.ui.BlockComboBox3.clear()
                for i in range(77, 86):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "O"):
                self.ui.BlockComboBox3.clear()
                for i in range(86, 89):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "P"):
                self.ui.BlockComboBox3.clear()
                for i in range(89, 98):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "Q"):
                self.ui.BlockComboBox3.clear()
                for i in range(98, 101):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "R"):
                self.ui.BlockComboBox3.clear()
                self.ui.BlockComboBox3.addItem(str(101))
            elif(str(self.ui.SectionComboBox4.currentText()) == "S"):
                self.ui.BlockComboBox3.clear()
                for i in range(102, 105):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "T"):
                self.ui.BlockComboBox3.clear()
                for i in range(105, 110):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "U"):
                self.ui.BlockComboBox3.clear()
                for i in range(110, 117):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "V"):
                self.ui.BlockComboBox3.clear()
                for i in range(117, 122):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "W"):
                self.ui.BlockComboBox3.clear()
                for i in range(122, 144):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "X"):
                self.ui.BlockComboBox3.clear()
                for i in range(144, 147):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "Y"):
                self.ui.BlockComboBox3.clear()
                for i in range(147, 150):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "Z"):
                self.ui.BlockComboBox3.clear()
                self.ui.BlockComboBox3.addItem(str(150))
            #End track section if-elif block
        
        elif(str(self.ui.TrackComboBox4.currentText()) == "Red"): #Red line is open
            #Print member blocks of selected track section
            if(str(self.ui.SectionComboBox4.currentText()) == "A"):
                self.ui.BlockComboBox3.clear()
                for i in range(1, 4):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "B"):
                self.ui.BlockComboBox3.clear()
                for i in range(4, 7):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "C"):
                self.ui.BlockComboBox3.clear()
                for i in range(7, 10):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "D"):
                self.ui.BlockComboBox3.clear()
                for i in range(10, 13):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "E"):
                self.ui.BlockComboBox3.clear()
                for i in range(13, 16):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "F"):
                self.ui.BlockComboBox3.clear()
                for i in range(16, 21):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "G"):
                self.ui.BlockComboBox3.clear()
                for i in range(21, 24):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "H"):
                self.ui.BlockComboBox3.clear()
                for i in range(24, 46):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "I"):
                self.ui.BlockComboBox3.clear()
                for i in range(46, 49):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "J"):
                self.ui.BlockComboBox3.clear()
                for i in range(49, 55):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "K"):
                self.ui.BlockComboBox3.clear()
                for i in range(55, 58):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "L"):
                self.ui.BlockComboBox3.clear()
                for i in range(58, 61):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "M"):
                self.ui.BlockComboBox3.clear()
                for i in range(61, 64):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "N"):
                self.ui.BlockComboBox3.clear()
                for i in range(64, 67):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "O"):
                self.ui.BlockComboBox3.clear()
                self.ui.BlockComboBox3.addItem(str(67))
            elif(str(self.ui.SectionComboBox4.currentText()) == "P"):
                self.ui.BlockComboBox3.clear()
                for i in range(68, 71):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox4.currentText()) == "Q"):
                self.ui.BlockComboBox3.clear()
                self.ui.BlockComboBox3.addItem(str(71))
            elif(str(self.ui.SectionComboBox4.currentText()) == "R"):
                self.ui.BlockComboBox3.clear()
                self.ui.BlockComboBox3.addItem(str(72))
            elif(str(self.ui.SectionComboBox4.currentText()) == "S"):
                self.ui.BlockComboBox3.clear()
                for i in range(73, 76):
                    self.ui.BlockComboBox3.addItem(str(i))
            elif(str(self.ui.SectionComboBox3.currentText()) == "T"):
                self.ui.BlockComboBox3.clear()
                self.ui.BlockComboBox3.addItem(str(76))
        #End track line if-elif block

        '''
        #Evaluate block display
        if(str(self.ui.SectionComboBox4.currentText()) != '' and str(self.ui.BlockComboBox3.currentText()) != ''):
            if(str(self.ui.TrackComboBox4.currentText()) == "Green"):
                #Obtain block number
                block_num = int(self.ui.BlockComboBox3.currentText())
                #Retrieve block object
                blockObj = GreenLine.block_list[block_num-1]

                self.ui.BlockSectionLabel.setText("Section: " + blockObj.section)
                self.ui.BlockLengthLabel.setText("Block Length: " + str(blockObj.length))
                self.ui.SpeedLimitLabel.setText("Speed Limit: " + str(blockObj.speed_limit))
                self.ui.OccupancyLabel.setText("Occupancy: " + str(blockObj.occupancy))
                self.ui.BlockStatusLabel.setText("Status: " + str(blockObj.status))

            elif(str(self.ui.TrackComboBox4.currentText()) == "Red"):
                #Obtain block number
                block_num = int(self.ui.BlockComboBox3.currentText())
                #Retrieve block object
                blockObj = RedLine.block_list[block_num-1]

                self.ui.BlockSectionLabel.setText("Section: " + blockObj.section)
                self.ui.BlockLengthLabel.setText("Block Length: " + str(blockObj.length))
                self.ui.SpeedLimitLabel.setText("Speed Limit: " + str(blockObj.speed_limit))
                self.ui.OccupancyLabel.setText("Occupancy: " + str(blockObj.occupancy))
                self.ui.BlockStatusLabel.setText("Status: " + str(blockObj.status))

            #End if
        #End if
        '''
    #End Method

    #Method to update block information when specified track block changes
    def UpdateBlockInfo(self):
        #Leave function if block has not been specified
        if(str(self.ui.SectionComboBox4.currentText()) == ''):
            return

        if(str(self.ui.TrackComboBox4.currentText()) == "Green"):
            #Obtain block number
            block_num = int(self.ui.BlockComboBox3.currentText())
            #Retrieve block object
            blockObj = GreenLine.block_list[block_num-1]

            #Convert speed limit from meters/second to miles/hour
            block_speed_limit = round(blockObj.speed_limit * 2.23694, 2)

            self.ui.BlockLengthLabel.setText("Block Length: " + str(blockObj.length) + " m")
            self.ui.SpeedLimitLabel.setText("Speed Limit: " + str(block_speed_limit) + " mph")
            self.ui.OccupancyLabel.setText("Occupancy: " + str(blockObj.occupancy))
            self.ui.BlockStatusLabel.setText("Status: Open" if blockObj.status else "Status: Closed")

        elif(str(self.ui.TrackComboBox4.currentText()) == "Red"):
            #Obtain block number
            block_num = int(self.ui.BlockComboBox3.currentText())
            #Retrieve block object
            blockObj = RedLine.block_list[block_num-1]

            #Convert speed limit from meters/second to miles/hour
            block_speed_limit = round(blockObj.speed_limit * 2.23694, 2)

            self.ui.BlockLengthLabel.setText("Block Length: " + str(blockObj.length) + " m")
            self.ui.SpeedLimitLabel.setText("Speed Limit: " + str(block_speed_limit) + " mph")
            self.ui.OccupancyLabel.setText("Occupancy: " + str(blockObj.occupancy))
            self.ui.BlockStatusLabel.setText("Status: Open" if blockObj.status else "Status: Closed")
        #End if
    #End method

    #Method to set switch number combo box in switch status group of maintenance mode
    def StatusSwitchNums(self):
        #Check if the Green line or Red line is being viewed
        if(str(self.ui.TrackComboBox5.currentText()) == "Green"): #Green line is open
            self.ui.SwitchComboBox1.clear()
            #Populate switch number combo box
            for i in range(1, 7):
                self.ui.SwitchComboBox1.addItem(str(i))

        elif(str(self.ui.TrackComboBox5.currentText()) == "Red"): #Red line is open
            self.ui.SwitchComboBox1.clear()
            #Populate switch number combo box
            for i in range(1, 8):
                self.ui.SwitchComboBox1.addItem(str(i))
        #End if-elif block
    #End method

    #Method to update switch information when the specified track switch changes
    def UpdateSwitchInfo(self):
        #Leave function if switch has not been specified
        if(str(self.ui.SwitchComboBox1.currentText()) == ''):
            return

        if(str(self.ui.TrackComboBox5.currentText()) == "Green"):
            #Obtain switch ID
            switch_ID = int(self.ui.SwitchComboBox1.currentText())
            #Retrieve switch object
            switchObj = GreenLine.switch_list[switch_ID-1]

            self.ui.StemBlockLabel.setText("Stem Block ID: " + str(switchObj.root))
            self.ui.BranchBlockLabel.setText("Branch Block ID: " + str(switchObj.curr_position))

        elif(str(self.ui.TrackComboBox5.currentText()) == "Red"):
            #Obtain switch ID
            switch_ID = int(self.ui.SwitchComboBox1.currentText())
            #Retrieve switch object
            switchObj = RedLine.switch_list[switch_ID-1]

            self.ui.StemBlockLabel.setText("Stem Block ID: " + str(switchObj.root))
            self.ui.BranchBlockLabel.setText("Branch Block ID: " + str(switchObj.curr_position))
        #End if
    #End method

    #Method to determine and display updated throughput
    def DisplayThroughput(self, curr_time):
        #Display throughput for green line
        green_throughput = GreenLine.ComputeThroughput(curr_time)
        self.ui.ThroughputLabel1.setText(str(round(green_throughput, 2)))

        #Display throughput for red line
        red_throughput = RedLine.ComputeThroughput(curr_time)
        self.ui.ThroughputLabel2.setText(str(round(red_throughput, 2)))
    #End method
            
    #Method to close block at the request of the dispatcher
    def GUICloseBlock(self):
        #Initialize temporary variables to hold details of block to be closed
        track_line = str(self.ui.TrackComboBox2.currentText())
        track_section = str(self.ui.SectionComboBox2.currentText())
        block_num = int(self.ui.BlockComboBox1.currentText())

        #Send closure information to wayside controller
        signals.wayside_block_status.emit(track_line, block_num, False)

        if(track_line == "Green"):
            #Ensure block is not already closed
            if(block_num in GreenLine.closed_blocks):
                #Create error message box
                ClosureInfoMsg = QMessageBox()
                ClosureInfoMsg.setWindowTitle("Block Closure")
                ClosureInfoMsg.setText("INFO: The specified block is already closed")
                ClosureInfoMsg.setIcon(QMessageBox.Information)

                MsgWin = ClosureInfoMsg.exec()

                return
            #End if

            #Set block status to false
            GreenLine.block_list[block_num-1].status = False

            #Add block to closure list in track object
            GreenLine.closed_blocks.append(block_num)

            #Update block closure list in maintenance mode of GUI
            numRows = self.ui.BlockClosureTable.rowCount()
            self.ui.BlockClosureTable.insertRow(numRows)
            self.ui.BlockClosureTable.setItem(numRows, 0, QTableWidgetItem("Green"))
            self.ui.BlockClosureTable.setItem(numRows, 1, QTableWidgetItem(str(block_num)))
        
        elif(track_line == "Red"):
            #Ensure block is not already closed
            if(block_num in RedLine.closed_blocks):
                #Create error message box
                ClosureInfoMsg = QMessageBox()
                ClosureInfoMsg.setWindowTitle("Block Closure")
                ClosureInfoMsg.setText("INFO: The specified block is already closed")
                ClosureInfoMsg.setIcon(QMessageBox.Information)

                MsgWin = ClosureInfoMsg.exec()

                return
            #End if

            #Set block status to false
            RedLine.block_list[block_num-1].status = False

            #Add block to closure list in track object
            RedLine.closed_blocks.append(block_num)

            #Update block closure list in maintenance mode of GUI
            numRows = self.ui.BlockClosureTable.rowCount()
            self.ui.BlockClosureTable.insertRow(numRows)
            self.ui.BlockClosureTable.setItem(numRows, 0, QTableWidgetItem("Red"))
            self.ui.BlockClosureTable.setItem(numRows, 1, QTableWidgetItem(str(block_num)))

        #End if-elif block
    #End method

    #Method to close block due to track fault
    def WaysideCloseBlock(self, track_line, block_num, error_type):
        if(track_line == "Green"):
            #Ensure block is not already closed
            if(block_num in GreenLine.closed_blocks):
                #Create error message box
                ClosureInfoMsg = QMessageBox()
                ClosureInfoMsg.setWindowTitle("Block Closure")
                if(error_type == 0):
                    ClosureInfoMsg.setText("INFO: Green Line block " + str(block_num) + " has also suffered a rail failure\nThis block is already closed for maintenance")
                elif(error_type == 1):
                    ClosureInfoMsg.setText("INFO: Green Line block " + str(block_num) + " has also suffered a circuit failure\nThis block is already closed for maintenance")
                elif(error_type == 2):
                    ClosureInfoMsg.setText("INFO: Green Line block " + str(block_num) + " has also suffered a power failure\nThis block is already closed for maintenance")
                #End if-else block

                ClosureInfoMsg.setIcon(QMessageBox.Information)

                MsgWin = ClosureInfoMsg.exec()

                return
            #End if

            #Create inform user of closure
            ClosureInfoMsg = QMessageBox()
            ClosureInfoMsg.setWindowTitle("Block Closure")
            if(error_type == 0):
                ClosureInfoMsg.setText("INFO: Green Line block " + str(block_num) + " has suffered a rail failure\nThis block is now closed for maintenance")
            elif(error_type == 1):
                ClosureInfoMsg.setText("INFO: Green Line block " + str(block_num) + " has suffered a circuit failure\nThis block is now closed for maintenance")
            elif(error_type == 2):
                ClosureInfoMsg.setText("INFO: Green Line block " + str(block_num) + " has suffered a power failure\nThis block is now closed for maintenance")
            #End if-else block

            ClosureInfoMsg.setIcon(QMessageBox.Information)

            MsgWin = ClosureInfoMsg.exec()

            #Set block status to false
            GreenLine.block_list[block_num-1].status = False

            #Add block to closure list in track object
            GreenLine.closed_blocks.append(block_num)

            #Update block closure list in maintenance mode of GUI
            numRows = self.ui.BlockClosureTable.rowCount()
            self.ui.BlockClosureTable.insertRow(numRows)
            self.ui.BlockClosureTable.setItem(numRows, 0, QTableWidgetItem("Green"))
            self.ui.BlockClosureTable.setItem(numRows, 1, QTableWidgetItem(str(block_num)))
        
        elif(track_line == "Red"):
            #Ensure block is not already closed
            if(block_num in RedLine.closed_blocks):
                ClosureInfoMsg = QMessageBox()
                ClosureInfoMsg.setWindowTitle("Block Closure")
                if(error_type == 0):
                    ClosureInfoMsg.setText("INFO: Red Line block " + str(block_num) + " has also suffered a rail failure\nThis block is already closed for maintenance")
                elif(error_type == 1):
                    ClosureInfoMsg.setText("INFO: Red Line block " + str(block_num) + " has also suffered a circuit failure\nThis block is already closed for maintenance")
                elif(error_type == 2):
                    ClosureInfoMsg.setText("INFO: Red Line block " + str(block_num) + " has also suffered a power failure\nThis block is already closed for maintenance")
                #End if-else block

                ClosureInfoMsg.setIcon(QMessageBox.Information)

                MsgWin = ClosureInfoMsg.exec()

                return
            #End if

            #Create inform user of closure
            ClosureInfoMsg = QMessageBox()
            ClosureInfoMsg.setWindowTitle("Block Closure")
            if(error_type == 0):
                ClosureInfoMsg.setText("INFO: Red Line block " + str(block_num) + " has suffered a rail failure\nThis block is now closed for maintenance")
            elif(error_type == 1):
                ClosureInfoMsg.setText("INFO: Red Line block " + str(block_num) + " has suffered a circuit failure\nThis block is now closed for maintenance")
            elif(error_type == 2):
                ClosureInfoMsg.setText("INFO: Red Line block " + str(block_num) + " has suffered a power failure\nThis block is now closed for maintenance")
            #End if-else block

            ClosureInfoMsg.setIcon(QMessageBox.Information)

            MsgWin = ClosureInfoMsg.exec()

            #Set block status to false
            RedLine.block_list[block_num-1].status = False

            #Add block to closure list in track object
            RedLine.closed_blocks.append(block_num)

            #Update block closure list in maintenance mode of GUI
            numRows = self.ui.BlockClosureTable.rowCount()
            self.ui.BlockClosureTable.insertRow(numRows)
            self.ui.BlockClosureTable.setItem(numRows, 0, QTableWidgetItem("Red"))
            self.ui.BlockClosureTable.setItem(numRows, 1, QTableWidgetItem(str(block_num)))
        #End if-else block
    #End method

    #Method to reopen block at the request of the dispatcher
    def GUIReopenBlock(self):
        #Initialize temporary variables to hold details of block to be reopen
        track_line = str(self.ui.TrackComboBox3.currentText())
        track_section = str(self.ui.SectionComboBox3.currentText())
        block_num = int(self.ui.BlockComboBox2.currentText())

        #Send closure information to wayside controller
        signals.wayside_block_status.emit(track_line, block_num, True)

        if(track_line == "Green"):
            #Ensure block is not already open
            if(block_num not in GreenLine.closed_blocks):
                #Create error message box
                ClosureInfoMsg = QMessageBox()
                ClosureInfoMsg.setWindowTitle("Block Reopening")
                ClosureInfoMsg.setText("INFO: The specified block is already open")
                ClosureInfoMsg.setIcon(QMessageBox.Information)

                MsgWin = ClosureInfoMsg.exec()

                return
            #End if

            #Set block status to true
            GreenLine.block_list[block_num-1].status = True

            #Remove block from closure list in track object
            GreenLine.closed_blocks.remove(block_num)

            #Update block closure list in maintenance mode of GUI
            for row in range(0, self.ui.BlockClosureTable.rowCount()):
                if(str(self.ui.BlockClosureTable.item(row, 0).text()) == "Green" and str(self.ui.BlockClosureTable.item(row, 1).text()) == str(block_num)):
                    self.ui.BlockClosureTable.removeRow(row)
                    break
            #End for loop

        
        elif(track_line == "Red"):
            #Ensure block is not already open
            if(block_num not in RedLine.closed_blocks):
                #Create error message box
                ClosureInfoMsg = QMessageBox()
                ClosureInfoMsg.setWindowTitle("Block Reopening")
                ClosureInfoMsg.setText("INFO: The specified block is already open")
                ClosureInfoMsg.setIcon(QMessageBox.Information)

                MsgWin = ClosureInfoMsg.exec()

                return
            #End if

            #Set block status to true
            RedLine.block_list[block_num-1].status = True

            #Remove block from closure list in track object
            RedLine.closed_blocks.remove(block_num)

            #Update block closure list in maintenance mode of GUI
            for row in range(0, self.ui.BlockClosureTable.rowCount()):
                if(str(self.ui.BlockClosureTable.item(row, 0).text()) == "Red" and str(self.ui.BlockClosureTable.item(row, 1).text()) == str(block_num)):
                    self.ui.BlockClosureTable.removeRow(row)
                    break
            #End for loop

        #End if-elif block
    #End method

    #Method to update train positions on scheduling table
    def UpdateTrainPositions(self):
        for trainObj in CTCSchedule.train_list:
            currPosition = "Block " + str(trainObj.route_queue[0])

            #Append to string if current position is a station
            if(trainObj.HostTrackLine.color == "Green"):
                #Loop over all stations of Green line
                for stationObj in GreenLine.station_list:
                    if(stationObj.block_num == trainObj.route_queue[0]):
                        currPosition = currPosition + " (" + stationObj.name + ")"
                    #End if
                #End for loop
            #End if

            if(trainObj.HostTrackLine.color == "Red"):
                #Loop over all stations of Green line
                for stationObj in RedLine.station_list:
                    if(stationObj.block_num == trainObj.route_queue[0]):
                        currPosition = currPosition + " (" + stationObj.name + ")"
                    #End if
                #End for loop
            #End if

            #Display block 0 as yard
            if(trainObj.route_queue[0] == 0):
                currPosition = currPosition + " (YARD)"

            #Loop over all rows of scheduling table
            for i in range(0, self.ui.SchedTable.rowCount()):
                if(self.ui.SchedTable.item(i, 0).text() == str(trainObj.number)):
                    self.ui.SchedTable.setItem(i, 2, QTableWidgetItem(currPosition))
                #End if
            #End for loop
        #End for loop
    #End method

    #Method to set the simulation speed based on position of horization slider in GUI
    def GUISetSimSpeed(self):
        #Obtain position of slider
        slider_position = self.ui.SimSpeedSlider.value()

        #Set interval for system clock
        self.timer_interval = 1000/(slider_position + 1)
    #End method

    #Method to update switch positions at request of dispatcher
    def UpdateSwitchPos(self):
        #Initialize temporary variables to hold details of switch to be toggled
        track_line = str(self.ui.TrackComboBox5.currentText())
        switch_ID = int(self.ui.SwitchComboBox1.currentText())
        
        #Recover switch and block objects
        if(track_line == "Green"):
            SwitchObj = GreenLine.switch_list[switch_ID-1]
            
            #Determine if switch is on a closed block
            if(SwitchObj.root not in GreenLine.closed_blocks):
                #Create error message box
                ClosureInfoMsg = QMessageBox()
                ClosureInfoMsg.setWindowTitle("Switch Position")
                ClosureInfoMsg.setText("ERROR: This switch is not closed for maintenance and therefore cannot be toggled manually")
                ClosureInfoMsg.setIcon(QMessageBox.Critical)

                MsgWin = ClosureInfoMsg.exec()

                return
            #End if

            #Update switch position
            SwitchObj.TogglePosition()

        elif(track_line == "Red"):
            SwitchObj = RedLine.switch_list[switch_ID-1]

            #Determine if switch is on a closed block
            if(SwitchObj.root not in RedLine.closed_blocks):
                #Create error message box
                ClosureInfoMsg = QMessageBox()
                ClosureInfoMsg.setWindowTitle("Switch Position")
                ClosureInfoMsg.setText("ERROR: This switch is not closed for maintenance and therefore cannot be toggled manually")
                ClosureInfoMsg.setIcon(QMessageBox.Critical)

                MsgWin = ClosureInfoMsg.exec()

                return
            #End if

            #Update switch position
            SwitchObj.TogglePosition()

        #End if-elif block
    #End method

    #Method to pause or continue simulation
    def PlayPauseSim(self):
        if(str(self.ui.PlayPauseButton.text()) == "Pause\nSimulation"):
            self.utimer.stop()
            self.ui.PlayPauseButton.setText("Continue\nSimulation")
        elif(str(self.ui.PlayPauseButton.text()) == "Continue\nSimulation"):
            self.utimer.start(self.timer_interval)
            self.ui.PlayPauseButton.setText("Pause\nSimulation")
        #End if-elif block
    #End method


#End MainWindow class definition

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())