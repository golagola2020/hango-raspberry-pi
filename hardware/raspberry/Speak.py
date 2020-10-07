# 외장모듈
import os, sys       # 시스템 모듈

# 내장모듈
from Http import Http
from Env import *

class Speak :

  @staticmethod
  # 스피커 출력 함수
  def say(option, status, idx=None) :
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
    if pid == 0 :
        # 자판기 상태 검사
        if status == "basic" :
            ''' 센싱되고 있지 않은 기본 상태 '''

            # 자판기의 모든 음료 정보를 하나의 문자열로 병합
            names = ""
            for i, name in enumerate(drinks["name"]) :
                names += str(i+1) + '번 : ' + name + ' : '
                
            message = "안녕하세요, 말하는 음료수 자판기입니다. 지금부터, 음료수 위치와, 이름을 말씀드리겠습니다. " + names
            
        elif status == "position" :
            ''' 손이 음료를 향해 위치한 상태  '''

            message = '선택하신' + drinks["name"][idx] + '는 : ' + str(drinks["price"][idx]) + '원, 입니다.'
        elif status == "sold" :
            ''' 음료수가 팔린 상태 '''
            message = drinks["name"][idx] + '를, 선택하셨습니다. : 맛있게 드시고 : 즐거운 하루 되십시오.'
        elif status == "sold_out" :
            ''' 음료수 품절 상태 '''
            message = drinks["name"][idx] + '는 : 품, 절, 입니다.'
        # 스피커 출력
        os.system(f"espeak {option} '{message}'")
        
        # 자식 프로세스 종료
        sys.exit(0)
    
    # 부모 프로세스가 실행하는 구문
    # 센싱이 기본 상태가 아니면 실행
    if status != "basic" :
        # 자식 프로세스가 종료될 때까지 대기
        os.waitpid(pid, 0)

  @staticmethod
  # espeak 프로세스 종료 함수
  def exit() :
    '''
        실행중인 'espeak' 프로세스 종료
    '''

    # 할당된 프로세스가 있다면 실행
    if pid :
        # 자식프로세스 아이디 출력 후 종료
        print(pid, "espeak 프로세스를 종료합니다.")
        os.system("killall -9 espeak")