/*
    이 코드는 공개SW개발자 대회 출품을 위해 작성 및 공개된 아두이노 코드입니다.

    팀 명: 골라골라
    프로젝트 명 : 행고
*/

// 최대값 '상수' 선언 -> 아래쪽의 함수 및 setup,loop의 코드 변경 없이 상수의 변경만을 통해 자판기의 전체적인 변경이 가능합니다.

#define MAX_LINE 2          // 자판기 전체 라인 수
#define MAX_POSITION 8      // 자판기 전체 칸 수
#define PIN_COUNT 4         // 핀 개수
#define ROOP_CNT 5          // 정확도를 위해 손 측정시 몇번의 루프를 돌것인지 결정(i의 최대값을 결정.)
#define BOTH_SIDE_SPACE 10  // 자판기에서 버튼이 존재하지 않는 양옆 구간의 공간(cm)
#define BUTTON_RANGE 10     // 버튼과 버튼 사이의 공간(cm) 


// 입출력 핀 정의
const int trigPin[PIN_COUNT] = {2, 7, 8, 12};
const int echoPin[PIN_COUNT] = {3, 6, 9, 11};

// 지속시간 및 거리 선언
long duration[PIN_COUNT], distance[PIN_COUNT];

int drinks_numbers[MAX_LINE][(MAX_POSITION / MAX_LINE) + 1]; //음료 번호 지정 ex.1,2,3,4 ...
int sensed_position[MAX_LINE];                               //사용자가 선택한 음료 버튼 번호 저장할 곳
int sold_position = -1;                                      //선택되어 판매되는 음료수, -1은 음료가 판매되지 않았음을 의미
int final_sensed_position = -1;                              //센싱된 손의 영역 확정, -1은 손이 감지되지 않았음을 의미
int state = 0;

int sensed_cnt[PIN_COUNT][(MAX_POSITION / MAX_LINE) + 1] = {0, }; //초음파 센서에 감지되는걸 카운트해 기록하는 곳.
int i = 0;  // 정확도를 위해 돌려보는 횟수


void setup() {
  // 초기 변수 설정
  setInitVariable();

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

    //손 센싱 회수를 더함.
    hand_count(distance[i], i, (MAX_POSITION / MAX_LINE) + 1);
  }

  i += 1;

  //sold_position에 값을 넣음. 음료 판매 측정
  sensing_drink((MAX_POSITION / MAX_LINE) + 1);


  if (final_sensed_position != -1) {
    Serial.print("Sold_drink:");
    Serial.println(sold_position);
  }
  else {
    if ( i == ROOP_CNT) {
      most_hand_detect((MAX_POSITION / MAX_LINE) + 1);
      for (int a = 0; a < PIN_COUNT; a++) {
        for (int b = 0; b < (MAX_POSITION / MAX_LINE) + 1; b++) {
          sensed_cnt[a][b] = 0; //다음 음료 선택을 위해 초기화.
        }
      }

      multi_chosen_check(MAX_LINE);

      if (final_sensed_position != -1 || sold_position != -1 || state != 0) {
        /*
          라즈베리 파이로 시리얼을 전송할 때
          @success:
          (1)true: 센싱된 값이 존재한다면 true 전송
          (2)false: 센싱된 값이 존재하지 않는다면 false 전송
          @sensed_position: success가 true일 때 final_sensed_positiond을 전송
          @sold_position: success가 true일 때 sold_position을 전송
        */
        Serial.print("success ");
        Serial.println(true);

        Serial.print("sensed_position ");
        Serial.println(final_sensed_position);

        Serial.print("sold_position ");
        Serial.println(sold_position);

        Serial.print("state ");
        Serial.println(state);
      } else {
        Serial.print("success ");
        Serial.println(false);
      }

      i = 0; //루프횟수 초기화
    }
  }
  //모든 변수 초기화
  for (int c = 0; c < MAX_LINE; c++) {
    sensed_position[c] = -1;
  }
  final_sensed_position = -1;
  sold_position = -1;
  state = 0;

  delay(250); //센싱 및 전송 속도 조절
}


void setInitVariable() {
  /*
    setInitVariable():
    drinks_numbers 초기 변수 설정
    MAX_LINE, MAX_POSITION에 따라 자판기 정보 셋업
  */
  int cnt = 1;
  for (int i = 0; i < MAX_LINE; i++) {
    for (int j = 0; j < (MAX_POSITION / MAX_LINE) + 1; j++) {
      if (j == 0) {
        drinks_numbers[i][j] = -1;
      } else {
        drinks_numbers[i][j] = cnt;
        cnt++;
      }
    }
  }
}


void hand_count(float distance, int i, int cell) {
  /*
    hand_count():
    senesd_cnt를 카운트 하는 함수
    BOTH_SIDE_SPACE, BUTTON_RANGE, cell = ((MAX_POSITION/MAX_LINE) + 1) 에 따라 자판기 정보 셋업
    @distance : 초음파센서와 인식된 손 사이의 거리
    @i : 몇번째 라인인지 결정
    @cell : 한 라인에 음료수가 몇개 들어가는지. (칸)
  */
  if (BOTH_SIDE_SPACE <= distance && distance < (cell * BUTTON_RANGE) + BOTH_SIDE_SPACE)
    for (int k = 0; k < cell ; k++ ) {
      if ( ((cell * BUTTON_RANGE) + BOTH_SIDE_SPACE - BUTTON_RANGE * (k + 1)) <= distance && distance < ((cell * BUTTON_RANGE) + BOTH_SIDE_SPACE - BUTTON_RANGE * k ) ) {
        sensed_cnt[i][k]++;
        break;
      }
    }
  if (distance >= (cell * BUTTON_RANGE) + BOTH_SIDE_SPACE)
    sensed_cnt[i][0]++;
}


void sensing_drink(int drink) {
  /*
    sensing_drink():
    sold_position을 결정하는 함수
    음료수가 판매될 때 카운트 되는 센서값을 통해 판매된 음료의 번호를 결정.
  */
  for (int j = PIN_COUNT - 1; j >= MAX_LINE; j--) {
    for (int i = 1; i < drink; i++) {
      if (sensed_cnt[j][i] != 0) sold_position = drinks_numbers[j - MAX_LINE][i];
    }
  }
}


void most_hand_detect(int drink) {
  /*
    most_hand_detect():
    sensed_position[i]를 결정하는 함수
    각 라인의 어떤곳에서 손이 제일 많이 센싱되었는지 결정한다.
  */
  for (int j = 0; j < drink; j++) {
    for (int i = 0; i < MAX_LINE; i++)
      if (sensed_cnt[i][j] > sensed_cnt[i][0]) sensed_position[i] = drinks_numbers[i][j];
  }
}


void multi_chosen_check(int line) {
  /*
    multi_chosen_check():
    not_0 변수를 통해 음료수 버튼이 복수 센싱 되었는지 체크하는 함수
    여러 라인이 복수 센싱이 되었다면 가장 윗라인의 버튼을 출력한다.
  */
  int not_0 = 0;
  int min = drinks_numbers[MAX_LINE - 1][(MAX_POSITION / MAX_LINE)] ;
  //Serial.print(min);
  for (int i = 0; i < line; i++) {
    if (sensed_position[i] != -1) not_0 += 1;
  }
  if (not_0 == 0) {
    state = 0;
  }
  else if (not_0 == 1) {
    state = 1;
    for (int i = 0; i < line; i++)
      if (sensed_position[i] != -1) final_sensed_position = sensed_position[i];
  }
  else
    for (int i = 0; i < line; i++) {
      state = 1;
      if (sensed_position[i] != -1) {
        if (min > sensed_position[i])
          min = sensed_position[i];
      }
      final_sensed_position = min;
    }

}
