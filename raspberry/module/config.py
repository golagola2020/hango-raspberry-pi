'''
    전역 변수 관리
'''

import os

# 초기 세팅
PORT = '/dev/ttyACM0'
USER_ID = 'rltn123'
SERIAL_NUMBER = '20200814042555141'

# 스피커 출력 옵션 선언
SPEAK_OPTION = '-v ko+f3 -s 160 -p 95'

# 라즈베리파이가 가공할 변수명 집합
BASIC_KEYS = {'success', 'sensed_position', 'sold_position'}

# RPi File Path
RPI_FILE_PATH = '/home/pi/hango-hardware/hardware/raspberry'




