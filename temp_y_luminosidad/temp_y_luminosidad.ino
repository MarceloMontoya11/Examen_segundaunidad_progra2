#include <Ticker.h>
#include <OneWire.h>                
#include <DallasTemperature.h>
#include <BH1750.h>  
#include <Wire.h> 

BH1750 sensor;    
 
OneWire ourWire(2);                
 
DallasTemperature sensors(&ourWire); 
const int calefaccion_1=6;
const int foco=7;
const int calefaccion_2=8;

int value_temp=0;
int value_cale=0;
float value_c_1=0;
int value_c_2=0;

void fTemperatura(){
  sensors.requestTemperatures();   
  float temp= sensors.getTempCByIndex(0);
   Serial.println("temp:"+String(temp));
}

void fluminosidad(){
  unsigned int lux = sensor.readLightLevel();
  Serial.println("lum:"+String(lux));
}

Ticker ticTemperatura (fTemperatura,500);
Ticker ticluminosidad(fluminosidad,500);


void setup() {

pinMode(calefaccion_1,OUTPUT);

pinMode(calefaccion_2,OUTPUT);
pinMode(foco,OUTPUT);
ticTemperatura.start();
ticluminosidad.start();
Serial.begin(9600);
Wire.begin();
sensors.begin();   
sensor.begin();
}
 
void fnActuadores(String cad,float tempo,unsigned int luxo){
  int pos;
  String label,value;
  cad.trim();
  cad.toLowerCase();
  pos=cad.indexOf(':');
  label=cad.substring(0,pos);
  value=cad.substring(pos+1);
  Serial.println(cad);
  if(label.equals("foco")){
    if(value_temp !=value.toInt()){
       value_temp=value.toInt();
       digitalWrite(foco,value_temp);
    }
      
  }
  if(label.equals("cale")){
     if(value_cale !=value.toInt()){
        value_cale=value.toInt();
        digitalWrite(calefaccion_1,value_cale);
        digitalWrite(calefaccion_2,value_cale);
}
  }
   
      
      
      
    }





void loop() {
   
  ticTemperatura.update();
  ticluminosidad.update();
 
  
 

  if(Serial.available()){
    fnActuadores(Serial.readString(),sensors.getTempCByIndex(0),sensor.readLightLevel());
    
  }



                     
}
