#include <PID_v1.h>
#include <AutoPID.h>
float cmdVel = 19.0;
double curVel = 0.0;
double oldVel = 0.0;
double buffVel = 0;
float setpointVel = 17.935;
double power = 0.0;
double power2 = 0.0;
double setpoint = 0.0;
float kp = 25000.0;
float ki = 750.0;
float SafetyMargin = 4.0;
int auth = 1;
AutoPID powLoop2(&curVel, &setpoint, &power2, 0, 120000, kp, ki/1.7, 0);
PID powLoop(&curVel,&power,&setpoint,kp,ki,0,DIRECT);
bool AutoMode = true;
bool SBrake;
bool EBrake;
bool PEBrake;
bool SBrakeReg = false;

void initPID(){
  powLoop.SetOutputLimits(0,120000);
  powLoop.SetSampleTime(200);
  powLoop.SetMode(AUTOMATIC);
  powLoop2.setTimeStep(200);
}

double calcPower(){
  if(AutoMode){
  setpoint = cmdVel *.9;
  }else{
  setpoint = setpointVel * .9;
  }
  powLoop.Compute();
  powLoop2.run();
  if((power/power2 > SafetyMargin|| power/power2 < 1.0/SafetyMargin) && !get_SBrake() ){
    //set_EBrake(true);
  }
  
  if(PEBrake || EBrake || SBrake){
  power = 0;
  power2 = 0;
  }
  
   if (get_curVel()> setpoint + 2){
    set_SBrake(true);
    SBrakeReg = true;
    return 0;
  }else if (SBrakeReg){
    set_SBrake(false);
    SBrakeReg = false;
  }

  if(auth ==0 || cmdVel == 0.0){
    power =0;
    power2 = 0;
    set_SBrake(true); 
  }

 

  return power;
}



//get and set

double get_power(){
  return power;
}

double get_power2(){
  return power2;
}

void set_cmdVel(float input){
  cmdVel = input;
}

float get_cmdVel(){
  return cmdVel;
}

void set_curVel( double input){
  oldVel = buffVel;
  buffVel = curVel;
  curVel = input;
  detectFailures();

}

double get_curVel(){
  return curVel; 
}

double get_oldVel(){
  return oldVel;
}

void set_setpointVel(float input){
  setpointVel = input;
}

float get_setpointVel(){
  return setpointVel;
}

void set_auth(int input){
  auth = input;
}

int get_auth(){
  return auth; 
}


void set_kp(float input){
  kp = input;
  powLoop.SetTunings(kp,ki,0);

}

float get_kp(){
  return kp;
}

void set_ki(float input){
  ki = input;
  powLoop.SetTunings(kp,ki,0);

}

float get_ki(){
  return ki;
}

void set_AutoMode(bool input){
  AutoMode = input;
}

bool get_AutoMode(){
  return AutoMode; 
}

void set_SBrake(bool input){
  SBrake = input;
  if(SBrake)
  ToggleStates |= 1 << 2; 
  else{
  ToggleStates &= ~(1 << 2); 
  }

}

bool get_SBrake(){
  return SBrake; 
}

void set_EBrake(bool input){
  EBrake = input;
  if (EBrake){
    set_cmdVel(0);
    set_setpointVel(0);
    set_auth(0);
  }
   if(EBrake)
  ToggleStates |= 1 << 7; 
  else{
  ToggleStates &= ~(1 << 7); 
  }
}

bool get_EBrake(){
  return EBrake; 
}

void set_PEBrake(bool input){
  PEBrake = input;
   if(PEBrake)
  ToggleStates |= 1 << 6; 
  else{
  ToggleStates &= ~(1 << 6); 
  }
}

bool get_PEBrake(){
  return PEBrake; 
}
