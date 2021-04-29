bool tc_fault = false;
bool engine_fault = false;
bool brake_fault = false;


void DecodeTC(long long tc_enc){
  unsigned int cmdInt = tc_enc & 255;
  unsigned int cmdFlt = (tc_enc >> 8) & 15;
  unsigned int authInt = (tc_enc >> 12) & 255;
  unsigned int authFlt = (tc_enc >> 20) & 15;
  unsigned int check = (tc_enc >> 24) & 1023;
  //digitalWrite(leds[9],LOW);
  if((cmdInt + cmdFlt + authInt + authFlt) != check){
    tc_fault = true;
    set_e_brake(true);
    return;
  }
  tc_fault = false;
  set_cmd_vel(float(cmdInt) + float(cmdFlt) / 10.0);
  set_auth(authInt);
  if(upcoming_station && get_auth()== 0){
    stop_at_station = true;
    announcement = station_announcement;
    SendAnnouncement();
  }
  if(get_setpoint_vel()>get_cmd_vel())
    set_setpoint_vel(get_cmd_vel()); // edgecase on tc change  
}

void DetectFailures(){ // if we are not slowing down fast enough when a brake is active the fault occurs 
  if((get_cur_vel()- 2 > get_old_vel() &&  (get_pe_brake() || get_e_brake() || get_s_brake()) && get_old_vel() != 666.0 && get_old_vel()!=0)||brake_fault){
    digitalWrite(leds[10],HIGH);
    set_e_brake(true);
    brake_fault = true;

  }
  
  
  if(get_cur_vel() == 666.0){// specific value train model sends us for engine failure 
    digitalWrite(leds[8],HIGH); // Apply Engine Fail Light
    set_e_brake(true);
    engine_fault = true;

  }
  
  if(tc_fault){// set in tc decoding 
    digitalWrite(leds[9],HIGH); // Apply Signal Fail Light
    set_e_brake(true);
    tc_fault = true;


  }
  SendFaults();
}

bool get_tc_fault (){
  return tc_fault;
}

bool get_engine_fault (){
  return engine_fault;
}

bool get_brake_fault (){
  return brake_fault;
}
