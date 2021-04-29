#include <PID_v1.h>
#include <AutoPID.h>
float cmd_vel = 19.0;
double cur_vel = 0.0;
double old_vel = 0.0;
double buff_vel = 0;
float setpoint_vel = 17.935;
double power = 0.0;
double power2 = 0.0;
double setpoint = 0.0;
float kp = 25000.0;
float ki = 750.0;
float safety_margin = 4.0;
int auth = 1;
AutoPID pow_loop_2(&cur_vel, &setpoint, &power2, 0, 120000, kp, ki/1.7, 0);
PID pow_loop(&cur_vel,&power,&setpoint,kp,ki,0,DIRECT);
bool auto_mode = true;
bool s_brake;
bool e_brake;
bool pe_brake;
bool s_brake_reg = false;
bool s_brake_reg2 = false;


void InitPID(){
  pow_loop.SetOutputLimits(0,120000);
  pow_loop.SetSampleTime(200);
  pow_loop.SetMode(AUTOMATIC);
  pow_loop_2.setTimeStep(200);
}

double CalcPower(){
  if(auto_mode){
  setpoint = cmd_vel *.9;
  }else{
  setpoint = setpoint_vel * .9;
  }
  pow_loop.Compute();
  pow_loop_2.run();
  if((power/power2 > safety_margin|| power/power2 < 1.0/safety_margin) && !get_s_brake() ){ // safety critical portion makes sure the two loops dont differ too much
    //set_e_brake(true);
  }
  
  if(pe_brake || e_brake || s_brake){// cuts power on brake pull
  power = 0;
  power2 = 0;
  }
  
   if (get_cur_vel()> setpoint + 2){// slows us down automatically if we are speeding
    set_s_brake(true);
    s_brake_reg = true;
    return 0;
  }else if (s_brake_reg){// reset if no longer true
    set_s_brake(false);
    s_brake_reg = false;
  }

  if(auth ==0 || cmd_vel == 0.0){// brake on auth of 0
    power =0;
    power2 = 0;
    set_s_brake(true); 
    s_brake_reg2 = true;
  }else if (s_brake_reg2){// reset if no longer true 
    set_s_brake(false);
    s_brake_reg2 = false;
    toggle_states &=~(1 << 3); // Close Right Door 
    toggle_states &=~( 1 << 4); // Close Left Door
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

void set_cmd_vel(float input){
  cmd_vel = input;
}

float get_cmd_vel(){
  return cmd_vel;
}

void set_cur_vel( double input){
  old_vel = buff_vel;
  buff_vel = cur_vel;
  cur_vel = input;
  DetectFailures();

}

double get_cur_vel(){
  return cur_vel; 
}

double get_old_vel(){
  return old_vel;
}

void set_setpoint_vel(float input){
  setpoint_vel = input;
}

float get_setpoint_vel(){
  return setpoint_vel;
}

void set_auth(int input){
  auth = input;
}

int get_auth(){
  return auth; 
}


void set_kp(float input){
  kp = input;
  pow_loop.SetTunings(kp,ki,0);

}

float get_kp(){
  return kp;
}

void set_ki(float input){
  ki = input;
  pow_loop.SetTunings(kp,ki,0);

}

float get_ki(){
  return ki;
}

void set_auto_mode(bool input){
  auto_mode = input;
}

bool get_auto_mode(){
  return auto_mode; 
}

void set_s_brake(bool input){
  s_brake = input;
  if(s_brake)
  toggle_states |= 1 << 2; 
  else{
  toggle_states &= ~(1 << 2); 
  }

}

bool get_s_brake(){
  return s_brake; 
}

void set_e_brake(bool input){
  e_brake = input;
  if (e_brake){
    set_cmd_vel(0);
    set_setpoint_vel(0);
    set_auth(0);
  }
   if(e_brake)
  toggle_states |= 1 << 7; 
  else{
  toggle_states &= ~(1 << 7); 
  }
}

bool get_e_brake(){
  return e_brake; 
}

void set_pe_brake(bool input){
  pe_brake = input;
   if(pe_brake)
  toggle_states |= 1 << 6; 
  else{
  toggle_states &= ~(1 << 6); 
  }
}

bool get_pe_brake(){
  return pe_brake; 
}
