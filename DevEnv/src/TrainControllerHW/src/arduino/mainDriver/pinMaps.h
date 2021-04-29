#ifndef __pinMaps_h__
#define __pinMaps_h__

const int NUMBTN = 18;
const int NUMLED = 11;
const int NUMTOGGLE = 8;
//buttons 

int pass_brake_btn = 13;
int service_brake_btn = 22;
int auto_sel_btn= 23;
int speed_l_btn = 24;
int speed_r_btn = 25;
int r_door_btn = 26;
int l_door_btn = 27;
int announce_btn = 28;
int temp_r_btn = 29;
int beacon_btn = 30;
int temp_disp_btn = 31;
int ext_light_btn = 32;
int speed_btn = 33;
int int_lights_btn = 34;
int e_brake_btn = 50;
int auth_btn = 51;
int temp_l_btn = 52;
int power_btn = 53;

//Leds

int e_brake_led = 37;
int ext_lights_led = 38;
int int_lights_led = 39;
int engine_failure_led = 40;
int signal_failure_led = 41;
int brake_failure_led = 42;
int service_brake_led = 43;
int r_door_led = 44;
int l_door_led = 45;
int pass_brake_led = 46;
int auto_sel_led = 47;

// Arrays for group opeprations
int buttons[NUMBTN]={ext_light_btn , int_lights_btn , service_brake_btn , r_door_btn ,l_door_btn , auto_sel_btn, pass_brake_btn, e_brake_btn ,  speed_l_btn , speed_r_btn , announce_btn ,
		     temp_r_btn ,beacon_btn ,temp_disp_btn ,speed_btn ,auth_btn ,
                     power_btn ,temp_l_btn  };

int leds[NUMLED]={ext_lights_led , int_lights_led , service_brake_led , r_door_led , l_door_led  , auto_sel_led,  pass_brake_led, e_brake_led, engine_failure_led , signal_failure_led , brake_failure_led };
  
#endif // __pinMaps_h__


