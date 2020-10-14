#define PIN_COUNT 8

const int PIN[PIN_COUNT] = {2, 3, 4, 5, 6, 7, 9, 10};

int sold_position;
int sensed_position;
int btn[8];

void setup() {
  //시리얼 통신을 설정(전송속도 9600bps)
  Serial.begin(9600);
  for (int i = 0; i < PIN_COUNT; i++) {
    pinMode(PIN[i] , INPUT);
  }
}

void loop() {
  for (int i = 0; i < PIN_COUNT; i++) {
    btn[i] = digitalRead(PIN[i]);
    if (btn[i] == 0) {
      sold_position = i;
      break;
    }
    else sold_position = -1;
  }

  if (Serial.available()) {
    char data = Serial.read();
    if (data >= 49 && data <= 56 ) {
      sensed_position = int(data - 49);
    }
  }

  else {

    sensed_position = -1;

  }



  Serial.print("success ");

  Serial.println(true);

  Serial.print("sensed_position ");

  Serial.println(sensed_position);

  Serial.print("sold_position ");

  Serial.println(sold_position);





  delay(500);





}
