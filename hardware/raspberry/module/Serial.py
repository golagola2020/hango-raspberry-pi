# 외장모듈
import serial                   # 직렬 통신 모듈

# 내장모듈
from config import *  

# 전역 변수 선언
sensings = {}           # 센싱된 데이터가 키와 값으로 저장될 딕셔너리
received_keys = set()   # 아두이노에게 전달 받을 변수명 집합

class Serial:

  # 현재 감지 중인 데이터
  current_sensing_data = ''     

  @staticmethod
  def get_receive_data(port):
    '''
        아두이노 센싱 데이터 반환하는 함수
    '''

    # 센싱 데이터 한 줄 단위로 수신
    receive = port.readline()

    # 바이트형을 기본 문자열형으로 디코딩
    receive = list(map(lambda rcv: rcv.decode(), receive.split()))

    return receive
  
  @staticmethod
  def get_received_keys():
    '''
        received_keys 반환 함수
    '''

    return received_keys

  @staticmethod
  def get_sensings():
    '''
        sensings 반환 함수
    '''

    return sensings

  @staticmethod
  def save_received_data(receive):
    '''
        아두이노에게 수신한 데이터를 전역변수에 저장하는 함수
    '''
    # 수신한 변수명 저장 
    received_keys.add(receive[0])

    # 아두이노에서 받은 데이터를 변수명과 값의 형태로 저장, 딕셔너리 형태)
    sensings[ receive[0] ] = int(receive[1])

  @staticmethod
  def is_available(receive):
    '''
        아두이노로부터 수신한 데이터가 사용가능한 데이터인지 검사

        @ receive : 아두이노와 시리얼 통신을 통해 받은 수신 데이터
    '''

    # 수신한 변수명이 라즈베리파이에서 가공하고자하는 변수명들 중에 존재하는지 검사
    if receive != [] and receive[0] in BASIC_KEYS:
      # 존재한다면 수신 데이터 반환
      return True

    # 존재하지 않는다면 False 반환
    return False
