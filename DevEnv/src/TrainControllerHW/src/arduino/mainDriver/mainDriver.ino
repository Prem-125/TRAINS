
  

#include <PID_v1.h>
#include "pinMaps.h"
#include <Wire.h> 
#include <string.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 20 chars and 4 line display
unsigned int toggle_btn_states = 0;
unsigned int toggle_states = 32;
unsigned int cntrl_btn_states = 0; 
int lcd_view_index = 6;

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

void (*func_sel[10])() = { SpeedDown , SpeedUp, SendAnnounce,  TempUp, LCDBeacon, LCDTemp, // array of functions to call depending on what buttons are pressed. 
                        LCDSpeed, LCDAuth, LCDPower, TempDown };


char readbuff[70]; 



bool refresh = true;
long long tc_enc;
int beacon_enc;
long long kpki_enc;

int temperature = 72;
int flags; 
bool b_l_doors_open;
bool b_r_doors_open;
bool ext_lights_on;
bool stop_at_station = false;
bool l_doors_open;
bool r_doors_open;
bool upcoming_station = false;
bool on_pow_lcd = false;
const String  stations[] = {"Shadyside","Herron Ave","Swissville","Penn Station","Steel Plaza","First Ave","Station Square","South Hills Junction", 
                            "Pioneer","Edgebrook","Whited","South Bank","Central","Inglewood","Overbrook","Glenburry","Dormont","Mt Lebanon", "Poplar","Castle Shannon"};
String announcement = "No Announcement at this Time";
String station_announcement = "";
String ads[] = {"Choose Duquesne Light for all your home power needs", "Universtiy of Pittsburgh, a quality education", "Save money Today at Walmart!", "Thank you for riding the North Shore Expansion" };
int time_count = 0;
int ad_index = 0;
void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  PinSetup();
  for (int i = 0; i < NUMLED; i++)
  digitalWrite(leds[i],LOW);
  lcd.init();  //initialize the lcd
  lcd.backlight();  //open the backlight
  InitPID();


}

void loop() {
  // button handling functions 
  ReadToggleBtns();
  UpdateToggleStates();
  ReadCntrlBtns();
  ProcessCntrlBtns();

  SerialRead();
  
  if(refresh || on_pow_lcd){
  (*func_sel[lcd_view_index])(); // Refreshes LCD incase data changed from serial comms 
  refresh = false;
  };
  
  if (get_auto_mode()){
  AutoOps(); // override doors and force beacon lights
  }

  //update UI
  UpdateToggleLEDs();
  
  SendToggleStates();
  SendTemperature();
  if(time_count %20 == 0){//sends an add every 4 seconds 
    SendAds();
  }

//  lcd.clear();
//  lcd.setCursor(0,0);
//  lcd.print(toggle_btn_states);
//  lcd.setCursor(0,1);
//  lcd.print(cntrl_btn_states);
  time_count++;
  delay(200);
}

void SendAds(){
  if(!stop_at_station){
    announcement = ads[ad_index % 4];
    ad_index++;
    SendAnnouncement();
  }
}

void PinSetup(){

  // buttons  all use the internal pullup, inverted logic
  for (int i =0; i < NUMBTN; i++)
    pinMode(buttons[i],INPUT_PULLUP);
  
  //Leds 
  for (int i = 0; i < NUMLED; i++)
    pinMode(leds[i],OUTPUT);
  
  }

void ReadToggleBtns(){
  toggle_btn_states = 0;
  int temp = 0;
  for (int i =0; i < NUMTOGGLE; i++){
      //Serial.println((!(digitalRead(buttons[i])& 1)));
      toggle_btn_states += long(!(digitalRead(buttons[i])& 1)) << i;
  }
}

void ReadCntrlBtns(){
  cntrl_btn_states = 0;
  int temp = 0;
  for (int i =NUMTOGGLE; i < NUMBTN; i++){
      //Serial.println((!(digitalRead(buttons[i])& 1)));
      cntrl_btn_states += long(!(digitalRead(buttons[i])& 1)) << i-NUMTOGGLE;
  }
}

void UpdateToggleStates(){
    toggle_states ^= (toggle_btn_states & int(pow(2,NUMTOGGLE)- 1));
    set_auto_mode((toggle_states >> 5) & 1);
    set_s_brake((toggle_states >> 2) & 1);
    l_doors_open = (toggle_states >> 4) & 1;
    r_doors_open = (toggle_states >> 3) & 1;
    set_e_brake((toggle_states >> 7) & 1);
    set_pe_brake((toggle_states >> 6) & 1);
    
}
void AutoOps(){
  toggle_states &=~(1 << 3); // Override Right Door 
  toggle_states &=~( 1 << 4); // Override Left Door
  if(ext_lights_on)  
  toggle_states |=(3); // Force lights on if needed
  if(stop_at_station && get_cur_vel() == 0){
    StationSequence();
  }
}







void StationSequence(){
  if(b_r_doors_open)
    toggle_states |= 1 << 3; // Open Right Door if needed
  if(b_l_doors_open)
    toggle_states |= 1 << 4; // Open Left Door if needed
  UpdateToggleLEDs ();
  SendToggleStates();
  //delay(5000);
 // toggle_states &=~(1 << 3); // Close Right Door 
 // toggle_states &=~( 1 << 4); // Close Left Door 
  //set_s_brake(false);
  
  UpdateToggleLEDs ();
  SendToggleStates();
  upcoming_station=false;
  stop_at_station = false;

}

void UpdateToggleLEDs() {

  for (int i = 0; i < NUMTOGGLE; i++){
    digitalWrite(leds[i],(toggle_states >> i) & 1);
  }
  if((l_doors_open || r_doors_open) & get_cur_vel() != 0){
    digitalWrite(leds[3],LOW);
    digitalWrite(leds[4],LOW);
    lcd.clear();
    lcd.print("Cant open doors while moving");
    toggle_states &=~(1 << 3); // Close Right Door 
    toggle_states &=~( 1 << 4); // Close Left Door 
    delay(1000);
    refresh = true;

  }
}

void ProcessCntrlBtns(){
  for (int i = 0; i < NUMBTN - NUMTOGGLE; i++){
    if(((cntrl_btn_states >> i) & 1) == 1){
      lcd_view_index = i;
      (*func_sel[i])();
      
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
  lcd.print(get_cmd_vel() * 2.23);
  lcd.setCursor ( 15, 0 );            
  lcd.print("MPH");
  lcd.setCursor(0,1);
  lcd.print("Set Vel: ");
  lcd.setCursor(9,1);
  lcd.print(get_setpoint_vel() * 2.23 ); 
  lcd.setCursor ( 15, 1 );            
  lcd.print("MPH");
  lcd.setCursor(0,2);
  lcd.print("Cur Vel: ");
  lcd.setCursor(9,2);
  lcd.print(get_cur_vel()* 2.23);
  lcd.setCursor ( 15, 2 );            
  lcd.print("MPH");  
      on_pow_lcd = false;

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
  
      on_pow_lcd = false;

}
void LCDTemp(){
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Set Temp is:");
  lcd.setCursor(0,1);
  lcd.print(temperature);
  lcd.setCursor(3,1);
  lcd.print("F");
  on_pow_lcd = false;

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
  lcd_view_index = 8;
  refresh = true;
  on_pow_lcd = true;
}
void LCDAuth(){
  lcd.clear();
  lcd.setCursor(0,1);
  lcd.print("Authourity: ");
  lcd.setCursor(0,2);
  lcd.print(get_auth() );
  lcd.setCursor(8,2);
  lcd.print("block");
  on_pow_lcd = false;

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
   lcd_view_index = 5;
  refresh = true;
}
void TempDown(){
  if (temperature > 60){
    temperature-=1;
  }else {
    temperature = 60;
  }
   lcd_view_index = 5;
  refresh = true;
}
void SpeedUp(){
  if (get_setpoint_vel() < get_cmd_vel() - .45){ // checks bounds 1 mph incements 
    set_setpoint_vel(get_setpoint_vel()+.45);
  }else {
    set_setpoint_vel(get_cmd_vel());
  }
  lcd_view_index = 6;
  refresh = true;

 
}
void SpeedDown(){
    if (get_setpoint_vel() >.45){ // checks bounds 1 mph incements
    set_setpoint_vel(get_setpoint_vel()-.45);
  }else {
    set_setpoint_vel(0);
  }
  lcd_view_index = 6;
  refresh = true;
}

long long atoll(const char* ptr) { //convert string to long
  long long result = 0;
  while (*ptr && isdigit(*ptr)) {
    result *= 10;
    result += *ptr++ - '0';
  }
  return result;
}



void DecodeBeacon(){
  upcoming_station = beacon_enc & 1;
  b_l_doors_open = (beacon_enc >> 1) & 1;
  b_r_doors_open = (beacon_enc >> 2) & 1;
  ext_lights_on = (beacon_enc >> 3) & 1;
  String station = stations[((beacon_enc >> 4) & 31)];
  if(upcoming_station){
    station_announcement = "Arriving at " + station + " Station. The doors will open on the ";
  if(b_l_doors_open && b_r_doors_open){
    announcement += "Left and Right.\n";
  }else if (b_l_doors_open){
    station_announcement += "Left.\n";
  }else{
    station_announcement += "Right.\n";
  }
  } else {
    station_announcement = "No upcoming Station at this time";
  }
}

void DecodeKpKi(){
  float  kp = float(kpki_enc & 0xFFFF) + float((kpki_enc >> 16) & 0xFFFF)/1000.0 ;
  float ki = float((kpki_enc >> 32) & 0xFFFF) + float((kpki_enc >> 48) & 0xFFFF)/1000.0 ;
  set_kp(kp);
  set_ki(ki);
}

void SerialRead(){
  while(Serial.available() > 0){// each communication is one line with the sel value then another with the actual data 
    int numRead = Serial.readBytesUntil('\n',readbuff,20);
    int sel = atoi(readbuff);
    memset(readbuff,0,sizeof readbuff); // clear buffer
    if (numRead == 0 || sel < 1 || sel > 5)
      continue; 
    delay(10);
    numRead = Serial.readBytesUntil('\n',readbuff,70);
    switch(sel){
      case 1: // Got CurVel
              set_cur_vel(atof(readbuff));
              SendPower(CalcPower());
              
              break;
      case 2: // Got TC
              tc_enc = atoll(readbuff);
              DecodeTC(tc_enc);
              break;
      case 3:// Got Beacon
              beacon_enc = atoi(readbuff);
              DecodeBeacon();
              break;
      case 4: // got Kp and Ki
              kpki_enc = atoll(readbuff);
              DecodeKpKi();
              break;
      case 5:
              set_pe_brake(true);
              break;
  }
      memset(readbuff,0,sizeof readbuff); // clear buffer
      refresh = true; 
  }
}

void SendToggleStates(){
  Serial.println("1");
  Serial.println(toggle_states);
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
  faults += int(get_brake_fault());
  faults += int(get_engine_fault()) << 1;
  faults += int(get_tc_fault()) << 2;
  Serial.println(faults);
  
}
