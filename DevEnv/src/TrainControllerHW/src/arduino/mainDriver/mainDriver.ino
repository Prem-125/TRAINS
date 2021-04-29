
  

#include <PID_v1.h>
#include "pinMaps.h"
#include <Wire.h> 
#include <string.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 20 chars and 4 line display
unsigned int ToggleBtnStates = 0;
unsigned int ToggleStates = 32;
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



bool refresh = true;
long long TCEnc;
int beaconEnc;
long long kpkienc;

int temperature = 72;
int flags; 
bool BLDoorsOpen;
bool BRDoorsOpen;
bool ExtLightsOn;
bool StopAtStation = false;
bool LDoorsOpen;
bool RDoorsOpen;
bool UpcomingStation = false;
bool OnPowLCD = false;
const String  Stations[] = {"Shadyside","Herron Ave","Swissville","Penn Station","Steel Plaza","First Ave","Station Square","South Hills Junction", 
                            "Pioneer","Edgebrook","Whited","South Bank","Central","Inglewood","Overbrook","Glenburry","Dormont","Mt Lebanon", "Poplar","Castle Shannon"};
String announcement = "No Announcement at this Time";
String StationAnnouncement = "";
String Ads[] = {"Choose Duquesne Light for all your home power needs", "Universtiy of Pittsburgh, a quality education", "Save money Today at Walmart!", "Thank you for riding the North Shore Expansion" };
int timeCount = 0;
int adIndex = 0;
void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  pinSetup();
  for (int i = 0; i < NUMLED; i++)
  digitalWrite(LEDs[i],LOW);
  lcd.init();  //initialize the lcd
  lcd.backlight();  //open the backlight
  initPID();


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
  };
  
  if (get_AutoMode()){
  autoOps();
  }
  
  updateToggleLEDs();
  SendToggleStates();
  SendTemperature();
  if(timeCount %10 == 0){
    sendAds();
  }

//  lcd.clear();
//  lcd.setCursor(0,0);
//  lcd.print(ToggleBtnStates);
//  lcd.setCursor(0,1);
//  lcd.print(CntrlBtnStates);
  timeCount++;
  delay(200);
}

void sendAds(){
  if(!StopAtStation){
    announcement = Ads[adIndex % 4];
    adIndex++;
    SendAnnouncement();
  }
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
    set_AutoMode((ToggleStates >> 5) & 1);
    set_SBrake((ToggleStates >> 2) & 1);
    LDoorsOpen = (ToggleStates >> 4) & 1;
    RDoorsOpen = (ToggleStates >> 3) & 1;
    set_EBrake((ToggleStates >> 7) & 1);
    set_PEBrake((ToggleStates >> 6) & 1);
    
}
void autoOps(){
ToggleStates &=~(1 << 3); // Override Right Door 
ToggleStates &=~( 1 << 4); // Override Left Door
if(ExtLightsOn)  
ToggleStates |=(3); // Force lights on if needed
if(StopAtStation && get_curVel() == 0){
  stationSequence();
}
}







void stationSequence(){// rework
if(BRDoorsOpen)
ToggleStates |= 1 << 3; // Open Right Door if needed
if(BLDoorsOpen)
ToggleStates |= 1 << 4; // Open Left Door if needed
updateToggleLEDs ();
SendToggleStates();
delay(5000);
ToggleStates &=~(1 << 3); // Close Right Door 
ToggleStates &=~( 1 << 4); // Close Left Door 
set_SBrake(false);

updateToggleLEDs ();
SendToggleStates();
UpcomingStation=false;
StopAtStation = false;

}

void updateToggleLEDs() {

  for (int i = 0; i < NUMTOGGLE; i++){
    digitalWrite(LEDs[i],(ToggleStates >> i) & 1);
  }
  if((LDoorsOpen || RDoorsOpen) & get_curVel() != 0){
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
  lcd.print(get_cmdVel() * 2.23);
  lcd.setCursor ( 15, 0 );            
  lcd.print("MPH");
  lcd.setCursor(0,1);
  lcd.print("Set Vel: ");
  lcd.setCursor(9,1);
  lcd.print(get_setpointVel() * 2.23 ); 
  lcd.setCursor ( 15, 1 );            
  lcd.print("MPH");
  lcd.setCursor(0,2);
  lcd.print("Cur Vel: ");
  lcd.setCursor(9,2);
  lcd.print(get_curVel()* 2.23);
  lcd.setCursor ( 15, 2 );            
  lcd.print("MPH");  
      OnPowLCD = false;

}
void LCDBeacon(){
  int len = announcement.length();
   lcd.clear();
  lcd.setCursor(0,0);
  if (len < 20){
  lcd.print(announcement);
  }else{
    lcd.print(announcement.substring(0,20));
    lcd.setCursor(0,1);
 if (len < 40){
  lcd.print(announcement.substring(20));
  }else{
    lcd.print(announcement.substring(20,40));
  
  lcd.setCursor(0,2);
 if (len < 40){
  lcd.print(announcement.substring(40));
  }else{
    lcd.print(announcement.substring(40,60));
  
  lcd.setCursor(0,3);
  lcd.print(announcement.substring(60));
  }
  }
  }
  
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
  lcd.print(get_power()/1000.0);
   lcd.setCursor(7,1);
  lcd.print("kW");
      lcd.setCursor(10,1);
  lcd.print(get_power2()/1000.0);
   lcd.setCursor(15,1);
  lcd.print("kW");
  lcd.setCursor(0,2);
  lcd.print("Kp:");
  lcd.setCursor(4,2);
  lcd.print(get_kp());
  lcd.setCursor(0,3);
  lcd.print("Ki:");
  lcd.setCursor(4,3);
  lcd.print(get_ki());
  LCDViewIndex = 8;
  refresh = true;
  OnPowLCD = true;
}
void LCDAuth(){
   lcd.clear();
  lcd.setCursor(0,1);
  lcd.print("Authourity: ");
  lcd.setCursor(0,2);
  lcd.print(get_auth() );
    lcd.setCursor(8,2);
  lcd.print("block");
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
  if (get_setpointVel() < get_cmdVel() - .45){
    set_setpointVel(get_setpointVel()+.45);
  }else {
    set_setpointVel(get_cmdVel());
  }
  LCDViewIndex = 6;
  refresh = true;

 
}
void SpeedDown(){
    if (get_setpointVel() >.45){
    set_setpointVel(get_setpointVel()-.45);
  }else {
    set_setpointVel(0);
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



void decodeBeacon(){
  UpcomingStation = beaconEnc & 1;
  BLDoorsOpen = (beaconEnc >> 1) & 1;
  BRDoorsOpen = (beaconEnc >> 2) & 1;
  ExtLightsOn = (beaconEnc >> 3) & 1;
  String station = Stations[((beaconEnc >> 4) & 31)];
  if(UpcomingStation){
  StationAnnouncement = "Arriving at " + station + " Station. The doors will open on the ";
  if(BLDoorsOpen && BRDoorsOpen){
    announcement += "Left and Right.\n";
  }else if (BLDoorsOpen){
    StationAnnouncement += "Left.\n";
  }else{
    StationAnnouncement += "Right.\n";
  }
  } else {
    StationAnnouncement = "No upcoming Station at this time";
  }
}

void decodeKpKi(){
float  kp = float(kpkienc & 0xFFFF) + float((kpkienc >> 16) & 0xFFFF)/1000.0 ;
  float ki = float((kpkienc >> 32) & 0xFFFF) + float((kpkienc >> 48) & 0xFFFF)/1000.0 ;
  set_kp(kp);
  set_ki(ki);
}

void serialRead(){
  while(Serial.available() > 0){
    int numRead = Serial.readBytesUntil('\n',readbuff,20);
    int sel = atoi(readbuff);
    memset(readbuff,0,sizeof readbuff); // clear buffer
    if (numRead == 0 || sel < 1 || sel > 5)
      continue; 
    delay(10);
    numRead = Serial.readBytesUntil('\n',readbuff,70);
    switch(sel){
      case 1: // Got CurVel
              set_curVel(atof(readbuff));
              SendPower(calcPower());
              
              break;
      case 2: // Got TC
              TCEnc = atoll(readbuff);
              decodeTC(TCEnc);
              break;
      case 3:// Got Beacon
              beaconEnc = atoi(readbuff);
              decodeBeacon();
              break;
      case 4: // got Kp and Ki
              kpkienc = atoll(readbuff);
              decodeKpKi();
              break;
      case 5:
              set_PEBrake(true);
              break;
  }
      memset(readbuff,0,sizeof readbuff); // clear buffer
      refresh = true; 
  }
}

void SendToggleStates(){
  Serial.println("1");
  Serial.println(ToggleStates);
}

void SendPower(double power){
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

void SendFaults(){
  Serial.println("5");
  int faults = 0;
  faults += int(get_BrakeFault());
  faults += int(get_EngineFault()) << 1;
  faults += int(get_TCFault()) << 2;
  Serial.println(faults);
  
}
