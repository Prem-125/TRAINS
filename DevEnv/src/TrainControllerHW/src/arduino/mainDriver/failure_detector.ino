bool TCFault = false;
bool EngineFault = false;
bool BrakeFault = false;


void decodeTC(long long TCEnc){
  unsigned int cmdInt = TCEnc & 255;
  unsigned int cmdFlt = (TCEnc >> 8) & 15;
  unsigned int authInt = (TCEnc >> 12) & 255;
  unsigned int authFlt = (TCEnc >> 20) & 15;
  unsigned int check = (TCEnc >> 24) & 1023;
  //digitalWrite(LEDs[9],LOW);
  if((cmdInt + cmdFlt + authInt + authFlt) != check){
    TCFault = true;
    //set_EBrake(true);
    return;
  }
  TCFault = false;
  set_cmdVel(float(cmdInt) + float(cmdFlt) / 10.0);
  set_auth(authInt);
  if(UpcomingStation && get_auth()== 0){
    StopAtStation = true;
    SendAnnouncement();
  }
}

void detectFailures(){
  if((get_curVel()-2 > get_oldVel() &&  (get_PEBrake() || get_EBrake() || get_SBrake()) && get_oldVel() != 666.0 && get_oldVel()!=0)||BrakeFault){
    digitalWrite(LEDs[10],HIGH);
    set_EBrake(true);
    BrakeFault = true;

  }
  
  
  if(get_curVel() == 666.0){
    digitalWrite(LEDs[8],HIGH); // Apply Engine Fail Light
    set_EBrake(true);
    EngineFault = true;

  }
  
  if(TCFault){
    digitalWrite(LEDs[9],HIGH); // Apply Signal Fail Light
   // set_EBrake(true);


  }
  SendFaults();
}

bool get_TCFault (){
  return TCFault;
}

bool get_EngineFault (){
  return EngineFault;
}

bool get_BrakeFault (){
  return BrakeFault;
}
