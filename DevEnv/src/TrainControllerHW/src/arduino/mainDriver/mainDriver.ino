#include <PID_v1.h>

#include "pinMaps.h"
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 20 chars and 4 line display
unsigned int ToggleBtnStates = 0;
unsigned int ToggleStates = 0;
unsigned int CntrlBtnStates = 0; 
int LCDViewIndex = 6;

void LCDSpeed();
void LCDBeacon();
void LCDTemp();
void LCDPower();
void LCDAuth();
void SendAnnounce();
void TempUp();
void TempDown();
void SpeedUp();
void SpeedDown();

void (*funcSel[10])() = { SpeedDown , SpeedUp, SendAnnounce,  TempUp, LCDBeacon, LCDTemp, 
                        LCDSpeed, LCDAuth, LCDPower, TempDown };


char readbuff[70]; 
float cmdVel = 70.0;
double curVel = 0.0;
double oldVel = 0.0;
float setpointVel = 60.0;
float auth = 0.0;
double power = 0.0;
double setpoint = 0.0;
bool refresh = true;
long long TCEnc;
int beaconEnc;
int temperature = 72;
int flags; 
bool BLDoorsOpen;
bool BRDoorsOpen;
bool ExtLightsOn;
bool AutoMode;
bool SBrake;
bool EBrake;
bool PEBrake;
bool LDoorsOpen;
bool RDoorsOpen;
bool TCFault = false;
bool EngineFault = false;
bool BrakeFault = false;
bool UpcomingStation = false;
bool OnPowLCD = false;
const String  Stations[] = {"Shadyside","Herron Ave","Swissville","Penn Station","Steel Plaza","First Ave","Station Square","South Hills Junction", 
                            "Pioneer","Edgebrook","Whited","South Bank","Central","Inglewood","Overbrook","Glenburry","Dormont","Mt Lebanon", "Poplar","Castle Shannon"};
String announcement = "No Announcement at this Time";

PID powLoop(&curVel,&power,&setpoint,2.2,1,0,DIRECT);
void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  pinSetup();
  for (int i = 0; i < NUMLED; i++)
  digitalWrite(LEDs[i],LOW);
  lcd.init();  //initialize the lcd
  lcd.backlight();  //open the backlight
  powLoop.SetOutputLimits(0,120000);
  powLoop.SetSampleTime(200);
  powLoop.SetMode(AUTOMATIC);

}

void loop() {
  // put your main code here, to run repeatedly:
  readToggleBtns();
  updateToggleStates();
 
  readCntrlBtns();
  processCntrlBtns();
  serialRead();
  if(refresh || OnPowLCD){
  (*funcSel[LCDViewIndex])(); // Refreshes LCD incase data changed from serial comms 
  refresh = false;
  }
  calcPower();
  if (AutoMode){
  autoOps();
  }
  brakeCheck();
  detectFailures();
  updateToggleLEDs();
  SendPower();
  SendToggleStates();
  SendTemperature();

//  lcd.clear();
//  lcd.setCursor(0,0);
//  lcd.print(ToggleBtnStates);
//  lcd.setCursor(0,1);
//  lcd.print(CntrlBtnStates);
  delay(400);
}

void pinSetup(){

// buttons  all use the internal pullup, inverted logic
for (int i =0; i < NUMBTN; i++)
  pinMode(Buttons[i],INPUT_PULLUP);

//Leds 
for (int i = 0; i < NUMLED; i++)
  pinMode(LEDs[i],OUTPUT);

}

void readToggleBtns(){
  ToggleBtnStates = 0;
  int temp = 0;
  for (int i =0; i < NUMTOGGLE; i++){
      //Serial.println((!(digitalRead(Buttons[i])& 1)));
      ToggleBtnStates += long(!(digitalRead(Buttons[i])& 1)) << i;
  }
}

void readCntrlBtns(){
  CntrlBtnStates = 0;
  int temp = 0;
  for (int i =NUMTOGGLE; i < NUMBTN; i++){
      //Serial.println((!(digitalRead(Buttons[i])& 1)));
      CntrlBtnStates += long(!(digitalRead(Buttons[i])& 1)) << i-NUMTOGGLE;
  }
}

void updateToggleStates(){
    ToggleStates ^= (ToggleBtnStates & int(pow(2,NUMTOGGLE)- 1));
    AutoMode = (ToggleStates >> 5) & 1;
    SBrake =  (ToggleStates >> 2) & 1;
    LDoorsOpen = (ToggleStates >> 4) & 1;
    RDoorsOpen = (ToggleStates >> 3) & 1;
    EBrake = (ToggleStates >> 7) & 1;
    PEBrake = (ToggleStates >> 6) & 1;
    
}
void autoOps(){
ToggleStates &=~(1 << 3); // Override Right Door 
ToggleStates &=~( 1 << 4); // Override Left Door
if(ExtLightsOn)  
ToggleStates |=(1); // Force lights on if needed
if(UpcomingStation)
stationSequence(); // Initates Station Sequence 
 

  
}
void brakeCheck(){
if(PEBrake || EBrake || SBrake){
  power = 0;
}
}

void detectFailures(){
  if((oldVel >= curVel && power != 0 && !(PEBrake || EBrake || SBrake) && oldVel != 666.0 && oldVel!=0)||BrakeFault){
    digitalWrite(LEDs[10],HIGH);
    ToggleStates |= 1 << 7; // Apply EBrake
    power = 0;
    BrakeFault = true;

  }else{
    digitalWrite(LEDs[10],LOW); // Reset Brake Fail Light
  }
  if(BrakeFault && curVel > oldVel){
    BrakeFault = false;
  }
  if(curVel == 666.0){
    digitalWrite(LEDs[8],HIGH); // Apply Engine Fail Light
    ToggleStates |= 1 << 7; // Apply EBrake
    power = 0;

  }else{
    digitalWrite(LEDs[8],LOW); // Reset Fail Light
    
  }
  if(TCFault){
    digitalWrite(LEDs[9],HIGH); // Apply Signal Fail Light
    ToggleStates |= 1 << 7; // Apply EBrake
    power = 0;

  }else{
    digitalWrite(LEDs[9],LOW); // Reset  Signal Fail Light
  }
}

void calcPower(){
  if(AutoMode){
  setpoint = cmdVel;
  }else{
  setpoint = setpointVel;
  }
  powLoop.Compute();
}


void stationSequence(){
power = 0;
ToggleStates |= 1 << 2; // Apply S Brake
updateToggleLEDs ();
SendToggleStates();
SendPower();
SendAnnouncement();
while (curVel!=0){
   readCntrlBtns();
  processCntrlBtns();
  serialRead();
  if(refresh || OnPowLCD){
  (*funcSel[LCDViewIndex])(); // Refreshes LCD incase data changed from serial comms 
  refresh = false;
  }
  brakeCheck();
  updateToggleLEDs(); 
}
if(BRDoorsOpen)
ToggleStates |= 1 << 3; // Open Right Door if needed
if(BLDoorsOpen)
ToggleStates |= 1 << 4; // Open Left Door if needed
updateToggleLEDs ();
//sendToggleStates();
delay(5000);
ToggleStates &=~(1 << 3); // Close Right Door 
ToggleStates &=~( 1 << 4); // Close Left Door 
updateToggleLEDs ();
UpcomingStation=false;
}

void updateToggleLEDs() {

  for (int i = 0; i < NUMTOGGLE; i++){
    digitalWrite(LEDs[i],(ToggleStates >> i) & 1);
  }
  if((LDoorsOpen || RDoorsOpen) & curVel != 0){
    digitalWrite(LEDs[3],LOW);
    digitalWrite(LEDs[4],LOW);
    lcd.clear();
    lcd.print("Cant open doors while moving");
    ToggleStates &=~(1 << 3); // Close Right Door 
    ToggleStates &=~( 1 << 4); // Close Left Door 
    delay(1000);
    refresh = true;

  }
}

void processCntrlBtns(){
  for (int i = 0; i < NUMBTN - NUMTOGGLE; i++){
    if(((CntrlBtnStates >> i) & 1) == 1){
      LCDViewIndex = i;
      (*funcSel[i])();
      
      break;
    }
  }
}


void LCDSpeed(){
   lcd.clear();
  lcd.setCursor(0,0);
   lcd.setCursor ( 0, 0 );          
  lcd.print("Cmd Vel: "); 
  lcd.setCursor ( 9, 0 );            
  lcd.print(cmdVel / 1.6);
  lcd.setCursor ( 15, 0 );            
  lcd.print("MPH");
  lcd.setCursor(0,1);
  lcd.print("Set Vel: ");
  lcd.setCursor(9,1);
  lcd.print(setpointVel / 1.6 ); 
  lcd.setCursor ( 15, 1 );            
  lcd.print("MPH");
  lcd.setCursor(0,2);
  lcd.print("Cur Vel: ");
  lcd.setCursor(9,2);
  lcd.print(curVel / 1.6);
  lcd.setCursor ( 15, 2 );            
  lcd.print("MPH");  
      OnPowLCD = false;

}
void LCDBeacon(){
   lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(announcement);
      OnPowLCD = false;

}
void LCDTemp(){
   lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Set Temp is:");
    lcd.setCursor(0,1);
  lcd.print(temperature);
    lcd.setCursor(3,1);
  lcd.print("F");
      OnPowLCD = false;

}
void LCDPower(){
   lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Power Output: ");
    lcd.setCursor(0,1);
  lcd.print(power/1000.0);
   lcd.setCursor(10,1);
  lcd.print("kW");
  LCDViewIndex = 8;
  refresh = true;
  OnPowLCD = true;
}
void LCDAuth(){
   lcd.clear();
  lcd.setCursor(0,1);
  lcd.print("Authourity: ");
  lcd.setCursor(6,1);
  lcd.print(auth);
    OnPowLCD = false;

}
void SendAnnounce(){
  SendAnnouncement();
}
void TempUp(){
  if (temperature < 80){
    temperature+=1;
  }else {
    temperature = 80;
  }
   LCDViewIndex = 5;
  refresh = true;
}
void TempDown(){
  if (temperature > 60){
    temperature-=1;
  }else {
    temperature = 60;
  }
   LCDViewIndex = 5;
  refresh = true;
}
void SpeedUp(){
  if (setpointVel < cmdVel - 2.5){
    setpointVel+=2.5;
  }else {
    setpointVel = cmdVel;
  }
  LCDViewIndex = 6;
  refresh = true;

 
}
void SpeedDown(){
    if (setpointVel >2.5){
    setpointVel-=2.5;
  }else {
    setpointVel = 0;
  }
  LCDViewIndex = 6;
  refresh = true;
}

long long atoll(const char* ptr) {
  long long result = 0;
  while (*ptr && isdigit(*ptr)) {
    result *= 10;
    result += *ptr++ - '0';
  }
  return result;
}

void decodeTC(){
  unsigned int cmdInt = TCEnc & 255;
  unsigned int cmdFlt = (TCEnc >> 8) & 15;
  unsigned int authInt = (TCEnc >> 12) & 255;
  unsigned int authFlt = (TCEnc >> 20) & 15;
  unsigned int check = (TCEnc >> 24) & 1023;
  digitalWrite(LEDs[9],LOW);
  if((cmdInt + cmdFlt + authInt + authFlt) != check){
    TCFault = true;
    cmdVel = 0;
    auth = 0;
    return;
  }
  TCFault = false;
  cmdVel = float(cmdInt) + float(cmdFlt) / 10.0;
  auth = float(authInt) + float(authFlt) / 10.0;
  if(auth == 0)
  ToggleStates |= 1 << 7; // Apply EBrake
}

void decodeBeacon(){
  UpcomingStation = beaconEnc & 1;
  BLDoorsOpen = (beaconEnc >> 1) & 1;
  BRDoorsOpen = (beaconEnc >> 2) & 1;
  ExtLightsOn = (beaconEnc >> 3) & 1;
  String station = Stations[((beaconEnc >> 4) & 31)];
  if(UpcomingStation){
  announcement = "Arriving at " + station + " Station. The doors will open on the ";
  if(BLDoorsOpen && BRDoorsOpen){
    announcement += "Left and Right.\n";
  }else if (BLDoorsOpen){
    announcement += "Left.\n";
  }else{
    announcement += "Right.\n";
  }
  } else {
    announcement = "No upcoming Station at this time";
  }
}

void serialRead(){
  while(Serial.available() > 0){
    int numRead = Serial.readBytesUntil('\n',readbuff,20);
    int sel = atoi(readbuff);
    memset(readbuff,0,sizeof readbuff); // clear buffer
    if (numRead == 0 || sel < 1 || sel > 3)
      continue; 
    delay(10);
    numRead = Serial.readBytesUntil('\n',readbuff,70);
    switch(sel){
      case 1: // Got CurVel
              oldVel = curVel;
              curVel = atof(readbuff);
              break;
      case 2: // Got TC
              TCEnc = atoll(readbuff);
              decodeTC();
              break;
      default:// Got Beacon
              beaconEnc = atoi(readbuff);
              decodeBeacon();
  }
      memset(readbuff,0,sizeof readbuff); // clear buffer
      refresh = true; 
  }
}

void SendToggleStates(){
  Serial.println("1");
  Serial.println(ToggleStates);
}

void SendPower(){
  Serial.println("2");
  Serial.println(power);
}

void SendAnnouncement(){
  Serial.println("3");
  Serial.println(announcement);
}

void SendTemperature(){
  Serial.println("4");
  Serial.println(temperature);
}
