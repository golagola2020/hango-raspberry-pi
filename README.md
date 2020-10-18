# hango-client (행고 클라이언트)
> 주의 : [GitHub Pages](https://pages.github.com/)에 대해서 충분히 숙지할 것.  
주의 : [Collaborating with issues and pull requests](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests)을 정독할 것

## 안내
#### 하드웨어
   1. [아두이노 시작하기](https://github.com/golagola2020/hango-arduino)를 통해 사물을 감지하고, 라즈베리파이로 감지 데이터를 송신할 수 있습니다.
   2. [라즈베리파이 시작하기](https://github.com/golagola2020/hango-raspberry-pi)를 통해 아두이노의 감지 데이터를 수신하고, 데이터를 가공하여 스피커로 출력할 수 있습니다.
   
#### 모바일
   1. [안드로이드 시작하기](https://github.com/golagola2020/hango-mobile)를 통해 hango 자판기를 관리하고, 음료 잔량을 파악하는 등의 데이터를 제공받을 수 있습니다.
   
#### 웹서버
   1. [웹서버 시작하기](https://github.com/golagola2020/hango-server)를 통해 hango-server와 hango-mysql을 구축하고, API 서버를 통해 클라이언트에게 데이터를 제공하며, 고객 관리 시스템을 이용할 수 있습니다.
   
## 시작하기에 앞서
[hango-raspberry-pi](https://github.com/golagola2020/hango-raspberry-pi) 프로젝트를 실행시키기 위한 도구 및 프로그램 설치
   1. pip 설치
   ```
   $ sudo apt-get install python-pip
   ```
   2. virtualenv 설치
   ```
   $ sudo pip install virtualenv
   ```

## 설치(로컬)
> 주의 : 패키지 충돌을 방지하기 위해 가상환경에 설치하는 것을 권장합니다.
* 가상환경 만들기
   ```
   $ virtualenv hango-raspberry
   $ cd hango-raspberry
   $ source bin/activate
   ```
   
* https://github.com/golagola2020/hango-raspberry-pi 에 push 권한이 있다면 :  
   * git fetch or pull or clone
   ```
   $ git clone https://github.com/golagola2020/hango-raspberry-pi.git
   $ cd hango-server
   ```

* https://github.com/golagola2020/hango-raspberry-pi 에 push 권한이 없다면 :  
   1. https://github.com/golagola2020/hango-raspberry-pi 에서 ```Fork```버튼 클릭하고,
   2. 포크 저장소 계정(maybe 개인 계정) 선택
   3. git fetch or pull or clone
   ```
   # 포크한 저장소 clone
   $ git clone https://github.com:YOUR_GITHUB_ACCOUNT/hango-raspberry-pi.git
   $ cd hango-server
   
   # hango-server 레포지터리를 upstream으로 리모트 설정
   $ git remote add upstream https://github.com/golagola2020/hango-raspberry-pi.git
   
   # 로컬 코드와 hango-server 동기화
   $ git fetch upstream
   $ git checkout master
   $ git merge upstream/master
   ```

## 실행(로컬)
> 주의 : 먼저, [설치](https://github.com/golagola2020/hango-raspberry-pi#설치로컬)를 통해 hango-raspberry-pi를 설치해주십시오.    
> 주의 : 아래 명령은 hango-raspberry-pi의 [requirements.txt](https://github.com/golagola2020/hango-raspberry-pi/blob/master/requirements.txt) 파일이 있는 루트 경로에서 실행되어야 합니다.
   1. 패키지 설치하기
   ```
   $ pip install -r requirements.txt
   ```
   2. [config.py](https://github.com/golagola2020/hango-raspberry-pi/blob/master/raspberry/module/config.py) 설정 파일 수정
      * /mobule 로 이동 후 수정
   ```
   $ cd raspberry/module
   $ vi config.py
   ```      
   ```python3
   PORT = 아두이노_시리얼_포트
   USER_ID = 자판기_소유자_아이디  # 모바일에서 회원가입한 유저 아이디를 의미한다. 초기 데이터 셋은 'rltn123'으로 하면 잘 동작할 것임
   SERIAL_NUMBER = 자판기_고유_번호 # 자판기마다 부여되는 고유번호를 의미한다. [hango-server](https://github.com/golagola2020/hango-server)의 고객 관리 시스템에서 등록할 수 있다. 초기 데이터 셋은 '20200814042555141'으로 하면 잘 동작할 것임
   ```
   3. 실행
      * hango-raspberry-pi 루트 경로의 raspberry 폴더 안에 있는 [main.py](https://github.com/golagola2020/hango-raspberry-pi/blob/master/raspberry/main.py) 실행
      * 주의 : 해당 경로까지 이동한 뒤에 실행시켜야 합니다.
   ```
   $ cd ../
   $ python3 main.py
   ```
   
## 배포(발행)

* https://github.com/golagola2020/hango-raspberry-pi 에 push 권한이 있다면 :  
```
$ git checkout -b 'features to develop'
$ git commit -m '[features to develop] message...'
$ git push origin 'features to develop'
```

* https://github.com/golagola2020/hango-raspberry-pi 에 push 권한이 없다면 :  
   1. 포크 동기화 [Syncing a fork](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork)
   2. Pull Request 보내기 [Creating a pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request)
   
## 데모
#### 클라이언트 데모
> v1.0 : https://youtu.be/D2CXURqW8qs
#### 모바일 데모
> v1.0 : https://youtu.be/K7cLH89WKPQ


## 기여하기
[CONTRIBUTING.md](https://github.com/golagola2020/hango-raspberry-pi/blob/master/CONTRIBUTING.md) 를 읽으신 후 기여를 해주십시오.     
자세한 Pull Request 절차와 행동 규칙을 확인하실 수 있습니다.

## 개발자

  - **박우림** [woorim960](https://github.com/woorim960)


[기여자 목록](https://github.com/golagola2020/hango-server/graphs/contributors)을 확인하여 이 프로젝트에 참가하신 분들을 보실 수 있습니다.

