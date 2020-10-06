# hango-client (행고 클라이언트)
> 주의 : [GitHub Pages](https://pages.github.com/)에 대해서 충분히 숙지할 것.  
주의 : [Collaborating with issues and pull requests](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests)을 정독할 것

## 안내
[hango-client](https://github.com/golagola2020/hango-client)는 [하드웨어](https://github.com/golagola2020/hango-client/tree/docs/hardware)와 [모바일](https://github.com/golagola2020/hango-client/tree/docs/mobile)로 구분되며, 하드웨어는 [아두이노](https://github.com/golagola2020/hango-client/tree/docs/hardware/arduino)와 [라즈베리파이](https://github.com/golagola2020/hango-client/tree/docs/hardware/raspberry)로 다시 구분됩니다.

## 설치

https://github.com/golagola2020/hango-client 에 push 권한이 있다면 :  
   1. git fetch or pull or clone
```
$ git clone https://github.com/golagola2020/hango-client.git
$ cd hango-client
```

https://github.com/golagola2020/hango-client 에 push 권한이 없다면 :  
   1. https://github.com/golagola2020/hango-client 에서 ```Fork```버튼 클릭하고,
   2. 포크 저장소 계정(maybe 개인 계정) 선택
   3. git fetch or pull or clone
   4. 포크 설정 [Configuring a remote for a fork](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/configuring-a-remote-for-a-fork)
   5. 포크 동기화 [Syncing a fork](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork)
```
$ git clone https://github.com:YOUR_GITHUB_ACCOUNT/hango-client.git
$ cd hango-server
$ git remote add upstream https://github.com/golagola2020/hango-client.git
$ git fetch upstream
$ git checkout master
$ git merge upstream/master
```

## 실행(로컬)

#### 하드웨어
   1. [아두이노 시작하기](https://github.com/golagola2020/hango-client/tree/docs/hardware/arduino)를 통해 사물을 감지하고, 라즈베리파이로 감지 데이터를 송신할 수 있습니다.
   2. [라즈베리파이 시작하기](https://github.com/golagola2020/hango-client/tree/docs/hardware/raspberry)를 통해 아두이노의 감지 데이터를 수신하고, 데이터를 가공하여 스피커로 출력할 수 있습니다.
   
#### 모바일
   1. [안드로이드 시작하기](https://github.com/golagola2020/hango-client/tree/docs/mobile)를 통해 hango 자판기를 관리하고, 음료 잔량을 파악하는 등의 데이터를 제공받을 수 있습니다.

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
   
## 데모
#### 클라이언트 데모
> https://youtu.be/D2CXURqW8qs
#### 모바일 데모
> https://youtu.be/K7cLH89WKPQ


## 기여하기

[CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) 를 읽으신 후 기여를 해주십시오. 자세한 Pull Request 절차와 행동 규칙을 확인하실 수 있습니다.

## 개발자

**안혜수** [shehdn](https://github.com/suehdn) : 아두이노와 센서를 이용한 사물 감지 후 사용가능한 형태로 가공하고, 이를 라즈베리파이에게 송신 및 수신  
**박우림** [woorim960](https://github.com/woorim960) : 라즈베리파이를 이용하여 수신한 센싱 데이터를 가공하고 스피커로 출력  
**송기수** [thdrltn684](https://github.com/thdrlcks784) : 안드로이드 'hango' 관리자 어플리케이션 구현  

[기여자 목록](https://github.com/golagola2020/hango-client/graphs/contributors)을 확인하여 이 프로젝트에 참가하신 분들을 보실 수 있습니다.

