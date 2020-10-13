#include <CapacitiveSensor.h>

#define COMMON_PIN      2    // The common 'send' pin for all keys
#define NUM_OF_SAMPLES  10   // Higher number whens more delay but more consistent readings
#define NUM_OF_KEYS     8    // Number of keys that are on the keyboard

 // This macro creates a capacitance "key" sensor object for each key on the piano keyboard:
#define CS(Y) CapacitiveSensor(2, Y)
/*
   CapitiveSense Library Demo Sketch
   Paul Badger 2008
   Uses a high value resistor e.g. 10M between send pin and receive pin
   Resistor effects sensitivity, experiment with values, 50K - 50M. Larger resistor values yield larger sensor values.
   Receive pin is the sensor pin - try different amounts of foil/metal on this pin
*/
CapacitiveSensor keys[] = {CS(3), CS(4), CS(5), CS(6), CS(7), CS(8), CS(9), CS(10)};
char hand;
bool hand_exist = false;
 
void setup()
{
  // Turn off autocalibrate on all channels:
  for (int i = 0; i < 8; ++i) {
    keys[i].set_CS_AutocaL_Millis(0xFFFFFFFF);
  }
 
  Serial.begin(9600);
 
}

void loop()
{
  // Loop through each key:
  for (int i = 0; i < 8; ++i) {
    // If the capacitance reading is greater than the threshold, play a note:
    //Serial.print(keys[i].capacitiveSensor(NUM_OF_SAMPLES));
 
    if (keys[i].capacitiveSensor(NUM_OF_SAMPLES) > 1000 ){
        hand = i+49;
        hand = char(hand); //Uart only recognize ascii values.
        hand_exist = true;
      
        Serial.print(hand);
        break;
       }
  }

  hand_exist = false;
  
  delay(500);                             // arbitrary delay to limit data to serial port
}
