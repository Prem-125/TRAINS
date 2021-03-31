#ifndef __pinMaps_h__
#define __pinMaps_h__

const int NUMBTN = 18;
const int NUMLED = 11;
const int NUMTOGGLE = 8;
//Buttons 

int PassBrakeBtn = 13;
int ServiceBrakeBtn = 22;
int AutoSelBtn= 23;
int SpeedLBtn = 24;
int SpeedRBtn = 25;
int RDoorBtn = 26;
int LDoorBtn = 27;
int AnnounceBtn = 28;
int TempRBtn = 29;
int BeaconBtn = 30;
int TempDispBtn = 31;
int ExtLightBtn = 32;
int SpeedBtn = 33;
int IntLightsBtn = 34;
int EBrakeBtn = 50;
int AuthBtn = 51;
int TempLBtn = 52;
int PowerBtn = 53;

//Leds

int EBrakeLED = 37;
int ExtLightsLED = 38;
int IntLightsLED = 39;
int EngineFailureLED = 40;
int SignalFailureLED = 41;
int BrakeFailureLED = 42;
int ServiceBrakeLED = 43;
int RDoorLED = 44;
int LDoorLED = 45;
int PassBrakeLED = 46;
int AutoSelLED = 47;

// Arrays for group opeprations
int Buttons[NUMBTN]={ExtLightBtn , IntLightsBtn , ServiceBrakeBtn , RDoorBtn ,LDoorBtn , AutoSelBtn, PassBrakeBtn, EBrakeBtn ,  SpeedLBtn , SpeedRBtn , AnnounceBtn ,
		     TempRBtn ,BeaconBtn ,TempDispBtn ,SpeedBtn ,AuthBtn ,
                     PowerBtn ,TempLBtn  };

int LEDs[NUMLED]={ExtLightsLED , IntLightsLED , ServiceBrakeLED , RDoorLED , LDoorLED  , AutoSelLED,  PassBrakeLED, EBrakeLED, EngineFailureLED , SignalFailureLED , BrakeFailureLED };
  
#endif // __pinMaps_h__


