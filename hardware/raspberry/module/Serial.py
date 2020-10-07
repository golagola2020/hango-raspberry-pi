# 외장모듈
import serial                   # 직렬 통신 모듈

# 내장모듈
from Env import *

class Serial :

  @staticmethod
  # 아두이노 센싱 데이터 반환하는 함수
  def get_receive_data(port) :
    # 센싱 데이터 한 줄 단위로 수신
    receive = port.readline()

    # 바이트형을 기본 문자열형으로 디코딩
    receive = list(map(lambda rcv : rcv.decode(), receive.split()))
    
    return receive
  
  @staticmethod
  # 사용가능한 데이터인지 검사하는 함수 
  def is_available(receive) :
    '''
        아두이노로부터 수신한 데이터가 사용가능한 데이터인지 검사

        @ receive : 아두이노와 시리얼 통신을 통해 받은 수신 데이터
    '''
    
    # 수신한 변수명이 라즈베리파이에서 가공하고자하는 변수명들 중에 존재하는지 검사
    if receive != [] and receive[0] in basic_keys :
        # 존재한다면 수신 데이터 반환 
        return True
    
    # 존재하지 않는다면 False 반환
    return False