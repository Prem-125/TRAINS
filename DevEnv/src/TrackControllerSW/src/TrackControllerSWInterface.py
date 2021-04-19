"""import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from .UI import Ui_TrackControllerUI
from signals import signals
from TrackControllerSW import TrackControllerSW

class MainWindow(QMainWindow):
    def __init__(self):
        #call parent constructor
        super(MainWindow, self).__init__()
        self.ui = Ui_TrackControllerUI()
        self.ui.setupUi(self)

        TrackController Green1
        TrackController Green2
        TrackController Green3
        TrackController Green4

        self.setControllerOffset(Green1,0)
        self.setControllerOffset(Green2,33)
        self.setControllerOffset(Green3,74)
        self.setControllerOffset(Green4,105)

        #UI used variables
        self.ui_block = 0
        self.plc_name = ""
        
        #UI Functions
        self.ui.BlockInput.currentTextChanged.connect(self.UIBlockOutput)
        self.ui.ImportButton.clicked.connect(self.ImportPLC)


        #Signal Functions
        signals.track_model_occupancy.connect(self.getOccupancy)
        signals.CTC_authority.connect(self.getAuthority)
        signals.track_break.connect(self.setBlockClosure)
        signals.wayside_block_status.connect(self.UpdateBlockStatus)
        #signals.CTC_suggested_speed.connect(self.getSugSpeed)
        #need wayside to track switch signals
        #need crossing signals


        



    
    def setControllerOffset(self, track_controller, offset):
        track_controller.setBlockOffset(offset)

    def setFirstSwitchBlocks(self, track_controller, in_a, in_b, end):
        track_controller.switch_1_in_a = in_a
        track_controller.switch_1_in_b = in_b
        track_controller.switch_1_end = end

    def setSecondSwitchBlocks(self, track_controller, in_a, in_b, end):
        track_controller.switch_2_in_a = in_a
        track_controller.switch_2_in_b = in_b
        track_controller.switch_2_end = end

    #Output for the UI
    def UIBlockOutput(self):
        if (self.ui.BlockInput.currentText() == "Choose"):
            self.ui.BlockStatus.setText("N/A")
            self.ui.Occupancy.setText("N/A")
            self.ui.Authority.setText("N/A")
            self.ui.CommandedSpeed.setText("N/A")
            self.ui.CrossingStatus.setText("N/A")
            self.ui.SwitchStatus.setText("N/A")
        else:
            self.ui_block = int(self.ui.BlockInput.currentText()) #Convert block input to string
            
            if(self.block_open[self.ui_block-self.block_offset] == True):
                self.ui.BlockStatus.setText("Open")
                self.ui.Occupancy.setText(str(self.occupancy[self.ui_block-self.block_offset]))
                self.ui.Authority.setText(str(self.authority[self.ui_block-self.block_offset]))
                self.ui.CommandedSpeed.setText(str(self.commanded_speed[self.ui_block-self.block_offset]))
                self.ui.CrossingStatus.setText("N/A")
                self.ui.SwitchStatus.setText("N/A")
            else:
                self.ui.BlockStatus.setText("Closed")
                self.ui.Occupancy.setText("N/A")
                self.ui.Authority.setText("N/A")
                self.ui.CommandedSpeed.setText("N/A")
                self.ui.CrossingStatus.setText("N/A")
                self.ui.SwitchStatus.setText("N/A")
    
if __name__ == "__main__":
app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec_())    
    """