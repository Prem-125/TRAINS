import xlrd

#Define Block class
class Block:

    #Constructor
    def __init__(self, blockNumber, trackSection, blockLength, blockGrade, blockSpeedLimit, blockElevation, blockCumElevation):
        #Initialize Block instance variables
        self.number = blockNumber
        self.section = trackSection
        self.length = blockLength
        self.grade = blockGrade
        self.speedLimit = blockSpeedLimit
        self.elevation = blockElevation
        self.cumElevation = blockCumElevation
        self.occupancy = 0
        self.status = 1

    #Define Mutator Methods
    def setOccupancy(self, blockOccupancy):
        self.occupancy = blockOccupancy

    def setStatus(self, blockStatus):
        self.status = blockStatus

    #Define Accessor Methods
    def getNumber(self):
        return self.number

    def getSection(self):
        return self.section

    def getLength(self):
        return self.length

    def getGrade(self):
        return self.grade

    def getSpeedLimit(self):
        return self.speedLimit

    def getElevation(self):
        return self.elevation

    def getCumElevation(self):
        return self.cumElevation

    def getOccupancy(self):
        return self.occupancy

    def getStatus(self):
        return self.status


#Define Switch Class
class Switch:

    #Constructor
    def __init__(self, blockNum0, blockNum1, blockNum2):
        #Initialize instance variable to hold root block number
        self.rootBlockNum = blockNum0

        #Initialize instance variable to hold branch block numbers
        self.branch1Num = blockNum1
        self.branch2Num = blockNum2

        #Initialize instance variable to hold current swtich position
        self.currPosition = blockNum1

    #Define Accessor Methods
    def getRootBlockNum(self):
        return self.rootBlockNum

    def getCurrPosition(self):
        return self.currPosition

    #Define method to toggle switch position
    def TogglePosition(self):
        if self.currPosition == self.branch1Num:
            self.currPosition = self.branch2Num
        else:
            self.currPosition = self.branch1Num


#Define Station class
class Station:

    #Constructor
    def __init__(self, stationName, blockNum, blockList):
        #Initialize instance variable to hold name of station
        self.name = stationName

        #Initialize instance variable to hold the block on which the station is located
        self.assocBlockNum = blockNum

        #Determine the travel time (expressed in minutes) from the yard to the station
        self.travelTime = self.ComputeTravelTime()

        #Initialize instance varialbe to hold the total number of tickets sold at the station
        self.ticketSales = 0

    #Define method to compute travel time from yard to station
    def ComputeTravelTime(self): #STUB
        return 1

    #Define method to accumulate ticket sales
    def setTicketSales(self, sales):
        self.ticketSales = sales

    #Define Accessor Methods
    def getName(self):
        return self.name

    def getAssocBlockNum(self):
        return self.assocBlockNum

    def getTravelTime(self):
        return self.travelTime

    def getTicketSales(self):
        return self.ticketSales


#Define Train class
class Train:

    #Constructor
    def __init__(self, trainNumber, trainDestination, line, trainArrivalTime, trainDepartureTime):
        #Initialize Block instance variables
        self.number = trainNumber
        self.destination = trainDestination
        self.trackLine = line
        self.arrivalTime = trainArrivalTime
        self.departureTime = trainDepartureTime
            
    #Define Accessor Methods
    def getNumber(self):
        return self.number

    def getDestination(self):
        return self.destination

    def getTrackLine(self):
        return self.trackLine

    def getArrivalTime(self):
        return self.arrivalTime

    def getDepartureTime(self):
        return self.departureTime

    def getSuggestedSpeed(self):
        return self.suggestedSpeed

    #Define Mutator Methods
    def setDepartureTime(self, trainDepartureTime):
        self.departureTime = trainDepartureTime

    def setSuggestedSpeed(self, trainSuggestedSpeed):
        self.suggestedSpeed = trainSuggestedSpeed



#Define TrackLine class
class Trackline:

    #Constructor
    def __init__(self, lineColor, filePath, sheetIndex):
        #Initialize color instance variable
        self.color = lineColor

        #Initialize block composition of TrackLine
        self.TrackSetup(filePath, sheetIndex)
    
    #Define method to establish track layout
    def TrackSetup(self, filePath, sheetIndex):
        #Open excel file
        exlWorkbook = xlrd.open_workbook(filePath)
        #Navigate to specified excel sheet within file
        exlSheet = exlWorkbook.sheet_by_index(sheetIndex)

        #Declare a list of track blocks
        self.blockList = []

        #Declare a list of track blocks
        self.switchList = []

        #Declare a list of stations
        self.stationList = []

        #Loop through contents of sheet row-wise
        for i in range(1, exlSheet.nrows): #Skip first row of column headers

            #All valid track layout spreadsheets have 10 columns per row
            #Initialize temporary variables to hold cell contents of current row
            trackSection = exlSheet.cell_value(i, 1) 
            blockNum = exlSheet.cell_value(i, 2)
            blockLength = exlSheet.cell_value(i, 3)
            blockGrade = exlSheet.cell_value(i, 4)
            blockSpeedLimit = exlSheet.cell_value(i, 5)
            blockElevation = exlSheet.cell_value(i, 8)
            blockCumElevation = exlSheet.cell_value(i, 9)

            #Add a block object to the track line block list
            self.blockList.append( Block(blockNum, trackSection, blockLength, blockGrade, blockSpeedLimit, blockElevation, blockCumElevation) )

            #Check if current block is the root of a switch or station
            blockInfrastructure = exlSheet.cell_value(i, 6)

            if ('SWITCH' in blockInfrastructure):
                #Declare temporary list of numerical values in infrastructure string
                blockNums = []

                #Capture block numbers from the infrastructure cell
                for element in blockInfrastructure:
                    #Initialize temporary string to hold block numbers associated with the switch
                    tempStr = ''

                    #Form block numbers from component digits while eliminating all other characters
                    while(element.isdigit()):
                        tempStr += element
                    
                    #Add to blockNums list only if the temporary string contains a block number
                    if(tempStr != ''):
                        #Identify associate block
                        if (int(tempStr) in blockNums):
                            rootBlockNum = int(tempStr)
                        else:
                            blockNums.append( int(tempStr) )

                #Add a switch object to the track line switch list
                self.switchList.append(rootBlockNum, blockNums[0], blockNums[1])

            elif('STATION' in blockInfrastructure):
                #Capture station name from the infrastructure cell
                parsedBlockInfrastructure = blockInfrastructure.split()
                stationName = parsedBlockInfrastructure[1]
                
                #Add a station object to the track line station list
                self.stationList.append( Station(stationName, blockNum, self.blockList) )
        
    #Define Accessor Methods
    def getColor(self):
        return self.color

    def getBlock(self, blockNum):
        return self.blockList[blockNum-1]

    def getSwitchPos(self, blockNum):
        #Perform linear search of switch list
        for switchObj in self.switchList:
            if(switchObj.getRootBlockNum() == blockNum):
                return switchObj

    def getStation(self, stationName):
        #Perform linear search of switch list
        for stationObj in self.stationList:
            if(switchObj.getName() == stationName.upper()):
                return switchObj

    #Define Mutator Methods
    def CloseBlock(self, blockNum):
        self.blockList[blockNum-1].setStatus(0)

    def OpenBlock(self, blockNum):
        self.blockList[blockNum-1].setStatus(1)

    def setBlockOccupied(self, blockNum):
        self.blockList[blockNum-1].setOccupancy(1)

    def setBlockUnoccupied(self, blockNum):
        self.blockList[blockNum-1].setOccupancy(0)

    def ToggleSwitchPosition(self, blockNum):
        #Perform linear search of switch list
        for switchObj in self.switchList:
            if(switchObj.getRootBlockNum() == blockNum):
                switchObj.TogglePosition()


                    
#Define Schedule class
class Schedule:

    #Constructor
    def __init__(self):
        #Initialize operational mode to manual
        #self.mode = manual

        #Declare a list of trains
        self.trainList = []

    #Define method to add train to schedule
    def ManualSchedule(self, trainDestination, trainArrivalTime, trackLine, trainSuggestedSpeed):
        #Assigne train number
        trainNumber = len(self.trainList) + 1

        # #Assign train an unused number
        # trainNumber = 1
        # match = 1 #Set while loop flag logic high
        # while(match == 1):
        #     #Reset flag to logic low
        #     match = 0

        #     #Compare candidate train number with active train numbers
        #     for trainObj in self.trainList:
        #         if tranNumber == trainObj.getNumber():
        #             match = 1
        #             break

        #     if(match == 1):
        #         trainNumber += 1

        #Compute train departure time
        trainDepartureTime = self.ComputeDepartureTime(trainArrivalTime, trainDestination, trainSuggestedSpeed)

        #Ensure specified arrival time is valid
        # if (trainDepartureTime > currentTime):
        #     #ERROR WINDOW
        #     return

        #Add train object to the schedule train list
        self.trainList.append( Train(trainNumber, trainDestination, trackLine.getColor(), trainArrivalTime, trainDepartureTime) )


    #Define method to compute train departure time
    def ComputeDepartureTime(self, trainArrivalTime, trainDestination, trainSuggestedSpeed):
        #STUB - departure time is one minute prior to arrival time
        if (arrivalTime < 60):
            return 86400 - (60 - arrivalTime)
        else:
            return arrivalTime - 60


    #Define method to automatically load in schedule
    def AutoSchedule(self, filePath, sheetIndex):
        #Open excel file
        exlWorkbook = xlrd.open_workbook(filePath)
        #Navigate to specified excel sheet within file
        exlSheet = exlWorkbook.sheet_by_index(sheetIndex)

        #Identify color of trackline
        trackColor = exlSheet.cell_value(1, 0)

        #Loop through contents of sheet column-wise
        for j in range(7, exlSheet.ncols):
            #Loop through contents of sheet row-wise
            for i in range(1, exlSheet.nrows):
                
                if (i == 1):
                    #First row of spreadsheet contains train dispatch times
                    trainDepartureTime = self.timeConv( exlSheet.cell_value(i, j) )

                #Determine destination and arrival time
                elif(exlSheet.cell_value(i,j) != ''):
                    #Train arrival time located in cell
                    trainArrivalTime = self.timeConv( exlSheet.cell_value(i,j) )

                    #Train destination located in left adjacent cell
                    infrastructure = exlSheet.cell_value(i, 6) 

                    #Capture station name from the infrastructure cell
                    parsedInfrastructure = infrastructure.split()
                    trainDestination = parsedInfrastructure[1]

                    break

            trainNumber = len(self.trainList) + 1

            self.trainList.append( Train(trainNumber, trainDestination, trackColor, trainArrivalTime, trainDepartureTime) )


    #Define method to convert excel time to python time
    def timeConv(self, timeVal):
        #Compute number of seconds
        seconds = timeVal * 86400

        return seconds

