# hango-arduino
> 주의 : [GitHub Pages](https://pages.github.com/)에 대해서 충분히 숙지할 것.  
주의 : [Collaborating with issues and pull requests](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests)을 정독할 것

## 시작하기에 앞서
> 이용하고있는 환경에서 [Arduiono IDE](https://www.arduino.cc/en/main/software)가 설치되어있는지 확인해주세요.

## 설치

https://github.com/golagola2020/hango-client 에 push 권한이 있다면 :  
   1. git fetch or pull or clone
```
$ git clone https://github.com/golagola2020/hango-client.git
$ cd hango-client/hardware/arduino
```

https://github.com/golagola2020/hango-client 에 push 권한이 없다면 :  
   1. https://github.com/golagola2020/hango-client 에서 ```Fork```버튼 클릭하고,
   2. 포크 저장소 계정(maybe 개인 계정) 선택
   3. git fetch or pull or clone
   4. 포크 설정 [Configuring a remote for a fork](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/configuring-a-remote-for-a-fork)
   5. 포크 동기화 [Syncing a fork](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork)
```
$ git clone https://github.com:YOUR_GITHUB_ACCOUNT/hango-client.git
$ cd hango-client/hardware/arduino
$ git remote add upstream https://github.com/golagola2020/hango-client.git
$ git fetch upstream
$ git checkout master
$ git merge upstream/master
```

## 실행(로컬)
   1. 초음파 센서 연결
      * (fritzing 소프트웨어 이용) 아래의 회로도는 arduino.ino 파일을 실행시킬 아두이노의 회로도입니다. 
      * 초음파센서 4개 중 1번과 2번은 음료수를 선택하는 버튼과 같은 행에 존재하고, 3번과 4번은 음료수가 나오는 곳과 같은 행에 존재합니다. ([예시 사진](#참고))  
      
![아두이노회로도(번호추가)](https://user-images.githubusercontent.com/67812466/91624116-7054c480-e9d9-11ea-92f0-77129b903d9e.jpg)

   2. 입출력 핀 정의
      * 각 초음파 센서들의 trig핀은 순서대로 2,7,8,12에 연결하고 echo핀은 3,6,9,11에 연결합니다.
```cpp
const int trigPin[PIN_COUNT] = {2, 7, 8, 12};
const int echoPin[PIN_COUNT] = {3, 6, 9, 11};
```

   3. 환경 설정
      * 'Hango-v1.0'의 소스코드는 총 8 종류의 음료수를 판매하며 한 줄에 4종류를 판매하는 총 2개의 라인을 갖습니다.  
```cpp
/*
   ROOP_CNT는 현재 자판기에서 손을 인식할 때, 초음파 센서에 한번 인식 되는것이 아닌 여러번 인식해 그 횟수를 더합니다. 이때 가장 많이 센싱된 곳을 실제 측정된다고 보기 때문에 정확도가 높아집니다.
*/

#define MAX_LINE 2          // 자판기 전체 라인 수
#define MAX_POSITION 8      // 자판기 전체 칸 수
#define PIN_COUNT 4         // 핀 개수
#define ROOP_CNT 5          // 정확도를 위해 손 측정시 몇번의 루프를 돌것인지 결정(i의 최대값을 결정.)
#define BOTH_SIDE_SPACE 10  // 자판기에서 버튼이 존재하지 않는 양옆 구간의 거리(cm)
#define BUTTON_RANGE 10     // 버튼과 버튼 사이의 거리
```
   
   4. 아두이노 실행
      * hango-client/hardware/arduino/arduino.ino 파일을 실행시킵니다.
   

## 배포(발행)
https://github.com/golagola2020/hango-client 에 push 권한이 있다면 :
```
$ git checkout -b 'features to develop'
$ git commit -m '[features to develop] message...'
$ git push origin 'features to develop'
```
https://github.com/golagola2020/hango-client 에 push 권한이 없다면 :
   1. 포크 동기화 [Syncing a fork](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork)
   2. Pull Request 보내기 [Creating a pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request) 

## 개발 환경

   * Arduino IDE @1.8.13

## 기여하기

[CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) 를 읽으신 후 기여를 해주십시오. 자세한 Pull Request 절차와 행동 규칙을 확인하실 수 있습니다.

## 개발자

**안혜수** [shehdn](https://github.com/suehdn)   

[기여자 목록](https://github.com/golagola2020/hango-client/graphs/contributors)을 확인하여 이 프로젝트에 참가하신 분들을 보실 수 있습니다.

### 참고 
** 초음파 센서의 위치에 대한 이해를 돕기 위해 아래의 사진을 첨부합니다. 위의 회로도의 전선 색에 맞춰 변경하시기 바랍니다. 
![자판기예시](https://user-images.githubusercontent.com/67812466/91648593-5207cb00-eaa4-11ea-8af1-d01680747228.PNG)
