

# 초기 세팅
PORT = '/dev/ttyACM1'
SERIAL_NUMBER = '20200814042555141'

# 스피커 출력 옵션 선언
SPEAK_OPTION = '-v ko+f3 -s 160 -p 95'

# 전역 변수 선언
sensings = {}           # 센싱된 데이터가 키와 값으로 저장될 딕셔너리
received_keys = set()   # 아두이노에게 전달 받을 변수명 집합

# 라즈베리파이가 가공할 변수명 집합
basic_keys = {'success', 'sensed_position', 'sold_position'}#, 'state'}

# 멀티프로세싱에 사용될 변수
pid = 0                 # 프로세스 아이디
sensing_data = ''       # 현재 감지 중인 데이터

# 음성 파일명 변수
sound_msgs = {
    'basic': '',
    'position': {},
    'sold': {},
    'sold_out': {}
}

