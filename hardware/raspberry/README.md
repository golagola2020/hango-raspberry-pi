# hango-raspberry 
> 주의 : [GitHub Pages](https://pages.github.com/)에 대해서 충분히 숙지할 것.  
주의 : [Collaborating with issues and pull requests](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests)을 정독할 것

## 시작하기에 앞서 
[hango-raspberry](https://github.com/golagola2020/hango-client/tree/master/hardware/raspberry) 프로젝트를 실행시키기 위한 도구 및 프로그램 설치
   1. 라즈베리파이 업데이트 및 업그레이드
```
$ sudo apt-get update
$ sudo apt-get upgrade
```
   2. [arduino](https://www.arduino.cc/en/main/software) 설치
```
$ sudo apt-get install arduino
```
   3. [python3](https://www.python.org/downloads/) 설치
   4. pip3 설치
```
$ sudo apt-get install python3
$ sudo apt-get install python3-pip
```
   5. TTS 모듈 'espeak' 설치
```
$ sudo apt-get install espeak

# 테스트
$ espeak "Hello World"
$ espeak -v ko "테스트 성공"
```
   6. HTTP 통신 모듈 'requests' 설치
```
$ sudo pip3 install requests
```

## 설치

https://github.com/golagola2020/hango-client 에 push 권한이 있다면 :  
   1. git fetch or pull or clone
```
$ git clone https://github.com/golagola2020/hango-client.git
$ cd hango-client/hardware/raspberry
```

https://github.com/golagola2020/hango-client 에 push 권한이 없다면 :  
   1. https://github.com/golagola2020/hango-client 에서 ```Fork```버튼 클릭하고,
   2. 포크 저장소 계정(maybe 개인 계정) 선택
   3. git fetch or pull or clone
   4. 포크 설정 [Configuring a remote for a fork](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/configuring-a-remote-for-a-fork)
   5. 포크 동기화 [Syncing a fork](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork)
```
$ git clone https://github.com:YOUR_GITHUB_ACCOUNT/hango-client.git
$ cd hango-client/hardware/raspberry
$ git remote add upstream https://github.com/golagola2020/hango-client.git
$ git fetch upstream
$ git checkout master
$ git merge upstream/master
```

## 실행(로컬)
> [hango-raspberry](https://github.com/golagola2020/hango-client/tree/master/hardware/raspberry)를 실행하기 위해서는 [hango-server](https://github.com/golagola2020/hango-server)가 먼저 실행 중인 상태여야 하며, [hango-arduino](https://github.com/golagola2020/hango-client/tree/docs/hardware/arduino)와 시리얼 통신이 진행 중 이어야 합니다.

   1. main.py 수정
```python3
# 웹서버 연결을 위한 요청 URL 수정
URL = 'your server url'

# 아두이노 시리얼 통신을 위한 PORT 수정
PORT = 'your arduino port'
```
   2. 라즈베리파이 실행
```
$ python3 main.py
```

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

## 기여하기

[CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) 를 읽으신 후 기여를 해주십시오. 자세한 Pull Request 절차와 행동 규칙을 확인하실 수 있습니다.

## 개발자

**박우림** [woorim960](https://github.com/woorim960)
**안혜수** [shehdn](https://github.com/suehdn) 

[기여자 목록](https://github.com/golagola2020/hango-client/graphs/contributors)을 확인하여 이 프로젝트에 참가하신 분들을 보실 수 있습니다.
