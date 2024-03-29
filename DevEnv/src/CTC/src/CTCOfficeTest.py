import TransitSystem
import unittest

#TestCase 1 - Ensure track layout is properly built
rackLine(unittest.TestCase):

    #Ensure green line is correctly configured
    def testGreenLine(self):
        #Create green line
        greenLine = TransitSystem.Trackline("Green", "Transit Schedule.xls", 2)

        self.assertEqual( greenLine.getColor, "Green")

        self.assertEqual( len(greenLine.blockList), 141 )

        self.assertEqual( len(greenLine.switchList), 6 )

        self.assertEqual( len(greenLine.stationList), 11)

        #Ensure all blocks are correctly intitialized
        for blockObj in greenLine.blockList:
            self.assertEqual(blockObj.getStatus(), 1)

            self.assertEqual(blockList.getOccupancy(), 0)

            self.assertTrue(blockList.getSpeedLimit() <= 70)

            self.assertTrue(blockObj.getLength() >= 50)

        #Ensure all switches are correctly initialized
        for switchObj in greenLine.switchList:
            self.assertTrue(switchObj.getRootBlockNum >= 1 and switchObj.getRootBlockNum <= 141)
            self.assertTrue(switchObj.getCurrPosition >= 1 and switchObj.getCurrPosition <= 141)

        #ensure all stations are correctly initialized
        for stationObj in greenLine.stationList:
            self.assertTrue(stationObj.getAssocBlockNum >= 1 and stationObj.getAssocBlockNum <= 141)

    #Ensure red line is correctly configured
    def testRedLine(self):
        #Create red line
        redLine = TransitSystem.Trackline("Red", "Transit Schedule.xls", 1)

        self.assertEqual( redLine.getColor, "Red")

        self.assertEqual( len(redLine.blockList), 60 )

        self.assertEqual( len(redLine.switchList), 7 )

        self.assertEqual( len(redLine.stationList), 7)

        #Ensure all blocks are initially open and unoccupied
        for blockObj in redLine.blockList:
            self.assertEqual(blockObj.getStatus(), 1)

            self.assertEqual(blockList.getOccupancy(), 0)

            self.assertTrue(blockList.getSpeedLimit() <= 70)

            self.assertTrue(blockObj.getLength() >= 50)

        #Ensure all switches are correctly initialized
        for switchObj in greenLine.switchList:
            self.assertTrue(switchObj.getRootBlockNum >= 1 and switchObj.getRootBlockNum <= 60)
            self.assertTrue(switchObj.getCurrPosition >= 1 and switchObj.getCurrPosition <= 60)

        #ensure all stations are correctly initialized
        for stationObj in greenLine.stationList:
            self.assertTrue(stationObj.getAssocBlockNum >= 1 and stationObj.getAssocBlockNum <= 60)


#TestCase 2 - Ensure manual dipatch operations function as expected
class TestManualDispatch(unittest.TestCase):

    #Ensure suggested speed was computed correctly
    def testSuggSpeed(self):
        demoSchedule = TransitSystem.Schedule()

        TransitSystem.Clock = 0

        #Call method to add newly dispatched train to schedule
        demoSchedule.ManualSchedule("Dormont", 60, "Green")

        self.assertEqual( demoSchedule.trainList[0].getSuggestedSpeed , .02)

    #Ensure destination and trackline are correctly
    def testAuthority(self):
        demoSchedule = TransitSystem.Schedule()

        TransitSystem.Clock = 0

        #Call method to add newly dispatched train to schedule
        demoSchedule.ManualSchedule("Dormont", 60, "Green")

        self.assertEqual( demoSchedule.trainList[0].getDestination , "Dormont" )
        self.assertEqual( demoSchedule.trainList[0].getDestination , "Green" )

#TestCase 3 - Ensure automatic dispatch operations function as expected
class TestAutomaticDispatch(unittest.TestCase):

    #Ensure proper number of trains are generated by scheduler
    def testTrainCreation(self):
        demoSchedule = TransitSystem.Schedule()

        TransitSystem.Clock = 0

        #Call method to add newly dispatched train to schedule
        demoSchedule.AutoSchedule("Transit Schedule V2", 1)

        self.assertEqual( len(demoSchedule.trainList) , 10 )

    #Ensure that trains are dispatched according to schedule
    def testTravelParameters(self):
        demoSchedule = TransitSystem.Schedule()

        TransitSystem.Clock = 0

        #Call method to add newly dispatched train to schedule
        demoSchedule.AutoSchedule("Transit Schedule V2", 1)

        self.assertEqual( demoSchedule.trainList[10].getDepartureTime , 270 )
        self.assertEqual( demoSchedule.trainList[10].getDestination , "Pioneer")
        self.assertEqual( demoSchedule.trainList[10].getArrivalTime , 271 )

#TestCase 4 - Ensure system responds appropriately to block closures/openings
class TestBlockStatus(unittest.TestCase):

    def testClosure(self):
        #Create red line
        redLine = TransitSystem.Trackline("Red", "Transit Schedule.xls", 1)

        self.assertEqual( redLine.getBlock(10).getStatus() , 1)

        redLine.CloseBlock(10)

        self.assertEqual( redLine.getBlock(10).getStatus() , 0)

    def testReopen(self):
        #Create red line
        redLine = TransitSystem.Trackline("Red", "Transit Schedule.xls", 1)

        self.assertEqual( redLine.getBlock(10).getStatus() , 1)

        redLine.CloseBlock(10)

        self.assertEqual( redLine.getBlock(10).getStatus() , 0)

        redLine.OpenBlock(10)

        self.assertEqual( redLine.getBlock(10).getStatus() , 1)


#Exectute test suite
if __name__ == '__main__':
    unittest.main()
        











        

