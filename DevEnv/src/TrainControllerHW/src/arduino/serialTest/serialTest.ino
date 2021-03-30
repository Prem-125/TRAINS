
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 20 chars and 4 line display
char readbuff[70]; 
int x;
float cmdVel = 0.0;
float curVel = 0.0;
float auth = 0.0;
long long TCEnc;
int beaconEnc;
int flags; 
bool LDoorsOpen;
bool RDoorsOpen;
bool ExtLightsOn;
bool UpcomingStation;
const String  Stations[] = {"Shadyside","Herron Ave","Swissville","Penn Station","Steel Plaza","First Ave","Station Square","South Hills Junction", 
                            "Pioneer","Edgebrook","Whited","South Bank","Central","Inglewood","Overbrook","Glenburry","Dormont","Mt Lebanon", "Poplar","Castle Shannon"};
String announcement = "";
void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  x=0;
  lcd.init();  //initialize the lcd
  lcd.backlight();  //open the backlight 
   
  
//  lcd.setCursor ( 0, 0 );            // go to the top left corner
//  lcd.print("    Hello,world!    "); // write this string on the top row
//  lcd.setCursor ( 0, 1 );            // go to the 2nd row
//  lcd.print("   IIC/I2C LCD2004  "); // pad string with spaces for centering
//  lcd.setCursor ( 0, 2 );            // go to the third row
//  lcd.print("  20 cols, 4 rows   "); // pad with spaces for centering
// // lcd.setCursor ( 0, 3 );            // go to the fourth row
//  lcd.print(" www.sunfounder.com ");
}
long long atoll(const char* ptr) {
  long long result = 0;
  while (*ptr && isdigit(*ptr)) {
    result *= 10;
    result += *ptr++ - '0';
  }
  return result;
}
void serialRead(){
  int val = Serial.readBytesUntil('\n',readbuff,20);
  flags = atoi(readbuff);
  memset(readbuff,0,sizeof readbuff); // clear buffer 
  delay(10);
  val = Serial.readBytesUntil('\n',readbuff,70);
  TCEnc = atoll(readbuff);
  memset(readbuff,0,sizeof readbuff); // clear buffer
  delay(10);
  val = Serial.readBytesUntil('\n',readbuff,20);
  curVel = atof(readbuff);
  memset(readbuff,0,sizeof readbuff); // clear buffer  
  delay(10);
  val = Serial.readBytesUntil('\n',readbuff,20);
  beaconEnc = atoi(readbuff);
  memset(readbuff,0,sizeof readbuff); // clear buffer
  while(Serial.available()){
    Serial.read();
  }
}

void decodeTC(){
  unsigned int cmdInt = TCEnc & 255;
  unsigned int cmdFlt = (TCEnc >> 8) & 15;
  unsigned int authInt = (TCEnc >> 12) & 255;
  unsigned int authFlt = (TCEnc >> 20) & 15;
  unsigned int check = (TCEnc >> 24) & 1023;
  if((cmdInt + cmdFlt + authInt + authFlt) != check){
    //do the light
    cmdVel = 999;
    auth = 999;
    return;
  }
  cmdVel = float(cmdInt) + float(cmdFlt) / 10.0;
  auth = float(authInt) + float(authFlt) / 10.0;
}

void decodeBeacon(){
  UpcomingStation = beaconEnc & 1;
  LDoorsOpen = (beaconEnc >> 1) & 1;
  RDoorsOpen = (beaconEnc >> 2) & 1;
  ExtLightsOn = (beaconEnc >> 3) & 1;
  String station = Stations[((beaconEnc >> 4) & 31)];
  if(UpcomingStation){
  announcement = "Arriving at " + station + " Station. The doors will open on the ";
  if(LDoorsOpen && RDoorsOpen){
    announcement += "Left and Right.\n";
  }else if (LDoorsOpen){
    announcement += "Left.\n";
  }else{
    announcement += "Right.\n";
  }
  }
}

void updateDisplay(){
lcd.clear();
  lcd.setCursor ( 0, 0 );          
  lcd.print("Cmd Speed: "); 
  lcd.setCursor ( 10, 0 );            
  lcd.print(cmdVel);
  lcd.setCursor(0,1);
  lcd.print("Auth: ");
  lcd.setCursor(6,1);
  lcd.print(auth);
  lcd.setCursor(0,2);
  lcd.print("Cur Vel: ");
  lcd.setCursor(9,2);
  lcd.print(curVel);  

  lcd.setCursor(0,3);
  lcd.print("Beacon: ");
  lcd.setCursor(8,3);
  lcd.print(beaconEnc);
  
  
}

void loop() {
  serialRead();
  decodeTC();
  decodeBeacon();
  updateDisplay();
  x+=1;
  
  Serial.println(announcement);
  delay(1000);
 
  
  
}
