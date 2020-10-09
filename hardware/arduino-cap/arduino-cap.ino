#include <CapacitiveSensor.h>
#include <avr/wdt.h>
/*
   CapitiveSense Library Demo Sketch
   Paul Badger 2008
   Uses a high value resistor e.g. 10M between send pin and receive pin
   Resistor effects sensitivity, experiment with values, 50K - 50M. Larger resistor values yield larger sensor values.
   Receive pin is the sensor pin - try different amounts of foil/metal on this pin
*/

CapacitiveSensor cs_12[4] = {CapacitiveSensor(12, 3), CapacitiveSensor(12, 5), CapacitiveSensor(12, 7), CapacitiveSensor(12, 9)};
/*
  CapacitiveSensor   cs_12_3 = CapacitiveSensor(12,3);        // 10M resistor between pins 4 & 2, pin 2 is sensor pin, add a wire and or foil if desired
  CapacitiveSensor   cs_12_5 = CapacitiveSensor(12,5);        // 10M resistor between pins 4 & 6, pin 6 is sensor pin, add a wire and or foil
  CapacitiveSensor   cs_12_7 = CapacitiveSensor(12,7);        // 10M resistor between pins 4 & 8, pin 8 is sensor pin, add a wire and or foil
  CapacitiveSensor   cs_12_9 = CapacitiveSensor(12,9);
*/
long button[4][50] = {0};
long sum[4] = {0};
long avg[4] = {0};
int reset = 0;
void setup()
{
  //cs_4_2.set_CS_AutocaL_Millis(0xFFFFFFFF);     // turn off autocalibrate on channel 1 - just as an example
  Serial.begin(9600);
  Serial.println("restart...");
  wdt_disable();
 
}

void loop()
{
  wdt_reset();
  long start = millis();
  for (int j = 0; j < 50; j++) {
    for (int i = 0; i < 4; i++) {
      button[i][j] =  cs_12[i].capacitiveSensor(30);
      if (button[i][j] > 10000) button[i][j] = 0;
      sum[i] += button[i][j];
    }
  }

  for (int i = 0; i < 4; i++) {
    avg[i] = sum[i] / 50;
  }


  /*
      long total1 =  cs_12_3.capacitiveSensor(30);
    long total2 =  cs_12_5.capacitiveSensor(30);
    long total3 =  cs_12_7.capacitiveSensor(30);
    long total4 =  cs_12_9.capacitiveSensor(30);
  */
  int runtime =  millis() - start;
  Serial.print(runtime);        // check on performance in milliseconds
  Serial.print("\t");                    // tab character for debug windown spacing

  Serial.print(avg[0]);                  // print sensor output 1
  Serial.print("\t");
  Serial.print(avg[1]);                  // print sensor output 2
  Serial.print("\t");
  Serial.print(avg[2]);
  Serial.print("\t");
  // print sensor output 3
  Serial.println(avg[3]);                // print sensor output 3

  for (int j = 0; j < 50; j++) {
    for (int i = 0; i < 4; i++) {
      button[i][j] = 0;
      sum[i] = 0;
      avg[i] = 0;
    }
  }

  if (runtime > 3000){
    wdt_enable(WDTO_15MS);
    delay(15);
  }

  delay(10);                             // arbitrary delay to limit data to serial port
}
