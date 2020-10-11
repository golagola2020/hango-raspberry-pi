#include <math.h>

#define MAX_LINE 2          // 자판기 전체 라인 수
#define MAX_POSITION 4      // 자판기 한 라인의 칸 수
#define PIN_COUNT 2         // 핀 개수
#define BOTH_SIDE_SPACE 10  // 자판기에서 버튼이 존재하지 않는 양옆 구간의 공간(cm)
#define BUTTON_RANGE 10     // 버튼과 버튼 사이의 공간(cm)
 

// 입출력 핀 정의
const int trigPin[PIN_COUNT] = {4, 6};
const int echoPin[PIN_COUNT] = {5, 7};

// 지속시간 및 거리 선언
long duration[PIN_COUNT], distance[PIN_COUNT];

int drinks_numbers[MAX_LINE][(MAX_POSITION / MAX_LINE) + 1]; //음료 번호 지정 ex.1,2,3,4 ...
int solded_drink = 0;                                      //선택되어 판매되는 음료수, -1은 음료가 판매되지 않았음을 의미

void setup() {
  //시리얼 통신을 설정(전송속도 9600bps)
  Serial.begin(9600);

  // 입출력 핀 설정
  for (int i = 0; i < PIN_COUNT; i++) {
    pinMode(trigPin[i], OUTPUT);
    pinMode(echoPin[i], INPUT);
  }
  
}

void loop() {
  
  for (int i = 0; i < PIN_COUNT; i++) {
    digitalWrite(trigPin[i], LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin[i], HIGH);
    delayMicroseconds(2);
    digitalWrite(trigPin[i], LOW);
    duration[i] = pulseIn(echoPin[i], HIGH);

    //초음파는 29마이크로초 당 1센치를 이동
    //초음파의 이동 거리 = duration(왕복에 걸린시간) / 29 / 2
    distance[i] = (duration[i] / 2) / 29.1;
  }

  for (int i = 0; i < MAX_LINE; i++){
    solded_drink = solded(distance[i],i);
    if (solded_drink != 0) break;
  }
  solded_drink = char(solded_drink);
  Serial.println(solded_drink);
  delay(1000);

  solded_drink = 0; //초기화
 

}

int solded(int distance, int line_num) {
  int solded_drink = 0;
  if (BOTH_SIDE_SPACE <= distance && distance < (MAX_POSITION * BUTTON_RANGE) + BOTH_SIDE_SPACE)
    solded_drink = ceil((distance - BOTH_SIDE_SPACE)/BUTTON_RANGE+(line_num*MAX_POSITION))+1;

  return solded_drink;
}