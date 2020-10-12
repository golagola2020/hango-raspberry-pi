# 외장모듈
import os
import sys                  # 시스템 모듈
import gtts           # TTS 모듈
from pygame import mixer        # 음성출력 모듈

# 내장모듈
from Http import Http
from Env import *


class Gspeak:

    @staticmethod
    # 사운드 저장 함수
    def save_sound(file_name, message):
        # mp3 변환 및 출력, 한국어
        tts = gTTS(text=message, lang='ko')
        tts.save(f'sounds/{file_name}.mp3')

    @staticmethod
    # 사운드 메세지 제작 함수
    def set_message():
        # 자판기의 모든 음료 정보를 하나의 문자열로 병합
        names = ""
        for i, name in enumerate(drinks["name"]):
            names += f"{str(i+1)}번 {name} "

        # 센싱되고 있지 않은 기본 상태 메세지
        sound_msgs["basic"] = f"안녕하세요. 말하는 음료수 자판기입니다. 지금부터 음료수 위치와 이름을 말씀드리겠습니다. {names}"

        # 음료수 이름을 파일명으로 하고 메세지 만들기
        for idx in range(len(drinks["name"])):
            # 손이 음료를 향해 위치한 상태 메세지
            sound_msgs["position"][drinks["name"][idx]] = f"{drinks['name'][idx]} {str(drinks['price'][idx])}원. "
            # 음료수가 팔린 상태
            sound_msgs["sold"][drinks["name"][idx]] = f"{drinks['name'][idx]} 선택. 맛있게 드시고 즐거운 하루 되십시오. "
            # 음료수 품절 상태
            sound_msgs["sold_out"][drinks["name"][idx]] = f"{drinks['name'][idx]} 품.절. "

    @staticmethod
    # 자판기 음료수 중 수정된 것이 있는지, 없는지 반환하는 함수
    def update_message():
        
        # 서버로부터 전달된 음료수 이름들 순회
        for idx, drink_name in enumerate(drinks["name"]):
            # 사운드로 만들어지지 않은 음료수가 있다면 실행
            if drink_name not in sound_msgs["position"]:
                # 자판기의 모든 음료 정보를 하나의 문자열로 병합
                names = ""
                for i, name in enumerate(drinks["name"]):
                    names += f"{str(i+1)}번 {name} "

                # 센싱되고 있지 않은 기본 상태 메세지
                sound_msgs["basic"] = f"안녕하세요. 말하는 음료수 자판기입니다. 지금부터 음료수 위치와 이름을 말씀드리겠습니다. {names}"
                # 손이 음료를 향해 위치한 상태 메세지
                sound_msgs["position"][drinks["name"][idx]] = f"{drinks['name'][idx]} {str(drinks['price'][idx])}원. "
                # 음료수가 팔린 상태
                sound_msgs["sold"][drinks["name"][idx]] = f"{drinks['name'][idx]} 선택. 맛있게 드시고 즐거운 하루 되십시오. "
                # 음료수 품절 상태
                sound_msgs["sold_out"][drinks["name"][idx]] = f"{drinks['name'][idx]} 품.절. "

    @staticmethod
    # 구글 TTS로 말하는 함수
    def say(option, status, drink_name=None):
        # 자판기 상태 검사
        if status == "basic":
            ''' 센싱되고 있지 않은 기본 상태 '''

            mixer.init(25100)  # 음성출력 속도 조절
            mixer.music.load(f'sounds/basic.mp3')
            mixer.music.play()
        else:
            '''
                각 상태에 따라 출력 메세지가 달라진다.

                1. position : 손이 음료를 향해 위치한 상태
                2. sold : 음료수가 팔린 상태
                3. sold_out : 음료수 품절 상태
            '''

            mixer.init(25100)  # 음성출력 속도 조절
            mixer.music.load(f'sounds/{sound_msgs[status][drink_name]}.mp3')
            mixer.music.play()


class Espeak:

  @staticmethod
  # 스피커 출력 함수
  def say(option, status, idx=None):
    ''' 
        스피커 출력 함수
        espeak 출력을 별도의 프로세스로 분할하여 동작시킨다.

        @ option : 음성 옵션  ( ex : '-v ko+f3 -s 160 -p 95' )
        @ status : 현재 자판기의 상태
            (1) basic : 센싱되고 있지 않은 기본 상태
            (2) position : 손이 음료를 향해 위치한 상태
            (3) sold : 음료수가 팔린 상태
            (4) sold_out : 음료수 품절 상태
        @ idx : 음료의 포지션 배열 인덱스 ( ex : drinks["( VALUE )"][idx] )
    '''

    message = ""

    # 자식 프로세스 생성
    pid = os.fork()
    # 자식 프로세스만 실행하는 구문
    if pid == 0:
        # 자판기 상태 검사
        if status == "basic":
            ''' 센싱되고 있지 않은 기본 상태 '''

            # 자판기의 모든 음료 정보를 하나의 문자열로 병합
            names = ""
            for i, name in enumerate(drinks["name"]):
                names += str(i+1) + '번 : ' + name + ' : '

            message = "안녕하세요, 말하는 음료수 자판기입니다. 지금부터, 음료수 위치와, 이름을 말씀드리겠습니다. " + names

        elif status == "position":
            ''' 손이 음료를 향해 위치한 상태  '''

            message = '선택하신' + drinks["name"][idx] + \
                '는 : ' + str(drinks["price"][idx]) + '원, 입니다.'
        elif status == "sold":
            ''' 음료수가 팔린 상태 '''
            message = drinks["name"][idx] + \
                '를, 선택하셨습니다. : 맛있게 드시고 : 즐거운 하루 되십시오.'
        elif status == "sold_out":
            ''' 음료수 품절 상태 '''
            message = drinks["name"][idx] + '는 : 품, 절, 입니다.'
        # 스피커 출력
        os.system(f"espeak {option} '{message}'")

        # 자식 프로세스 종료
        sys.exit(0)

    # 부모 프로세스가 실행하는 구문
    # 센싱이 기본 상태가 아니면 실행
    if status != "basic":
        # 자식 프로세스가 종료될 때까지 대기
        os.waitpid(pid, 0)

  @staticmethod
  # espeak 프로세스 종료 함수
  def exit():
    '''
        실행중인 'espeak' 프로세스 종료
    '''

    # 할당된 프로세스가 있다면 실행
    if pid:
        # 자식프로세스 아이디 출력 후 종료
        print(pid, "espeak 프로세스를 종료합니다.")
        os.system("killall -9 espeak")
