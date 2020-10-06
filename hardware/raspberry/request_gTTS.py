# 모듈포함
import os, sys, time            # 시스템 모듈
import serial                   # 직렬 통신 모듈
import requests, json           # HTTP 통신 및 JSON 모듈
from gtts import gTTS           # TTS 모듈    
from pygame import mixer        # 음성출력 모듈

# 초기 세팅
PORT = '/dev/ttyACM0'
SERIAL_NUMBER = '20200814042555141'

# 데이터 요청 Domain 선언
URL = str(os.environ['hangoURL'])

# 전역 변수 선언
sensings = {}                                                           # 센싱된 데이터가 키와 값으로 저장될 딕셔너리 
received_keys = set()                                                   # 아두이노에게 전달 받을 변수명 집합
basic_keys = {'success', 'sensed_position', 'sold_position', 'state'}   # 라즈베리파이가 가공할 변수명 집합

# 서버에서 전달받은 음료 정보가 저장될 전역 변수
drinks = {
    'position' : [],
    'name' : [],
    'price' : [],
    'count' : []
}

stop_ardu = True        #
sensing_data = ''       # 현재 감지 중인 데이터
def main():
    global stop_ardu
    global sensing_data

    # 아두이노와 시리얼 통신할 인스턴스 생성 
    port = serial.Serial(
        port = PORT,
        baudrate = 9600
    )

    # 캐시 비우기
    port.flushInput()
    
    # 음료수 정보 요청
    request_drinks()

    print(drinks)
    
    while True:
        if stop_ardu :
            # 센싱 데이터 한 줄 단위로 수신
            receive = port.readline()
            
        print("stop = ",end = "")
        print(stop_ardu)
        # 이용 가능한 데이터인지 검사
        receive = is_available(receive)

        print("receive")
        print(receive)
        # 이용 가능한 데이터라면 실행 
        if receive :

            # 수신한 변수명 저장 
            received_keys.add(receive[0])
            # 아두이노에서 받은 데이터를 변수명과 값의 형태로 저장, 딕셔너리 형태
            sensings[ receive[0] ] = int(receive[1])

            print(receive[0])
            print(receive[1])
            print(sensings["success"])
            
            # 라즈베리파이가 가공할 데이터를 모두 수신 했다면 실행 
            if basic_keys.difference(received_keys) == set() :

                print("received_keys")        
                print(received_keys)
                print(sensings["success"])
                
                # 아두이노에서 센싱된 데이터가 있으면 실행 
                if sensings["success"] :
                    # 출력
                    print("센싱 데이터 수신 성공")

                    # 판매된 음료수가 있을 경우에 실행
                    if sensings["sold_position"] != -1 :
                        # 감지 정보가 새로운 감지 정보와 다르면 실행 => 같은 말을 반복하지 않기 위함
                        if sensing_data != sensings["sold_position"] :
                            # 새로 감지된 정보 저장 => 같은 말을 반복하지 않기 위함
                            sensing_data = sensings["sold_position"]

                            # 실행중인 pygame 종료
                            mixer.quit()

                            # 판매된 음료수 정보 차감 요청
                            print("판매된 음료 차감 데이터를 요청하고 스피커 출력을 실행합니다.")
                            request_drinks_update()

                            # 스피커 출력
                            print("스피커 출력을 실행합니다.")
                            message = make_message("sold", sensings["sold_position"]-1)
                            speak_messaga(message,"sold.mp3")
                            time.sleep(5)
                            

                    # 손이 음료 버튼에 위치했을 경우에 실행
                    elif sensings["sensed_position"] != -1 :
                        # 감지 정보가 새로운 감지 정보와 다르면 실행 => 같은 말을 반복하지 않기 위함
                        if sensing_data != sensings["sensed_position"] :
                            # 새로 감지된 정보 저장 => 같은 말을 반복하지 않기 위함
                            sensing_data = sensings["sensed_position"]

                            # 실행중인 pygame 종료
                            mixer.quit()

                            print("물체가 감지되어 스피커 출력을 실행합니다.")

                            # 해당 음료가 품절일 경우 실행
                            if drinks["count"][sensings["sensed_position"]-1] <= 0 :
                                # 스피커 출력
                                message = make_message("sold_out", sensings["sensed_position"]-1)
                                speak_message(message, "slod_out.mp3")
                                time.sleep(5)
                                
                            else :
                                # 스피커 출력
                                message = make_message("position", sensings["sensed_position"]-1)
                                speak_message(message,"this_drink_is.mp3")
                                time.sleep(5)
                                
                                
                        # 수신한 변수명 집합 비우기 => 다음 센싱 때에도 정상 수신하는지 검사하기 위함 
                        received_keys.clear()
                    
                
            else :
                # 감지 정보가 새로운 감지 정보와 다르면 실행 => 같은 말을 반복하지 않기 위함
                if sensing_data != sensings["success"] :
                    # 새로 감지된 정보 저장 => 같은 말을 반복하지 않기 위함
                    sensing_data = sensings["success"]
                    print("수신 가능한 센싱 데이터가 아닙니다.")

                    # 실행중인 pygame 종료
                    #mixer.quit()

                    # 음료수 정보 요청
                    print("센싱 데이터가 없습니다.\n서버로부터 음료 정보를 불러옵니다...")
                    request_drinks()

                    # 스피커 출력
                    print("스피커 출력을 실행합니다.\n:인사말 ")
                    message=make_message("basic")
                    speak_message(message, "no_sensing_data.mp3")

                    #time.sleep(60)
                
                        
                        
            
                  
# 음료수 정보 요청 함수 
def request_drinks() :
    '''
        서버에게 음료수 정보를 요청 및 응답 받는 함수

        URL : /rasp/drink/read
        METHOD : POST
        CONTENT-TYPE : aplication/json
    '''

    # 서버에게 요청할 데이터 생성
    drink = {
        'serial_number' : SERIAL_NUMBER
    }

    # 서버 요청

    response = requests.post(URL + '/rasp/drink/read', data = drink)
    # 응답 JSON 데이터 변환
    response = json.loads(response.text)

    # 서버에서 정상 응답이 온 경우
    if response["success"] == True :
        # 전역 변수 초기화
        del drinks["position"][:]
        del drinks["name"][:]
        del drinks["price"][:]
        del drinks["count"][:]

        # 서버 데이터 삽입
        for drink in response["drinks"] :
            drinks["position"].append(drink["position"])
            drinks["name"].append(drink["name"])
            drinks["price"].append(drink["price"])
            drinks["count"].append(drink["count"])
        
    else :
        # 서버 에러 메세지 출력
        print("서버에서 음료 정보 조회 중 에러가 발생하였습니다.\n서버 에러 메세지 : ", response["msg"])

# 사용가능한 데이터인지 검사하는 함수 
def is_available(receive) :
    '''
        아두이노로부터 수신한 데이터가 사용가능한 데이터인지 검사

        @ receive : 아두이노와 시리얼 통신을 통해 받은 수신 데이터
    '''

    # 바이트형을 기본 문자열형으로 디코딩
    receive = list(map(lambda rcv : rcv.decode(), receive.split()))
    
    # 수신한 변수명이 라즈베리파이에서 가공하고자하는 변수명들 중에 존재하는지 검사
    if receive != [] and receive[0] in basic_keys :
        # 존재한다면 수신 데이터 반환 
        return receive
    
    # 존재하지 않는다면 False 반환
    return False

# 판매된 음료수 정보 차감 요청 함수
def request_drinks_update() :
    '''
        서버에게 판매된 음료수 정보를 전달하는 함수

        URL : /rasp/drink/update
        METHOD : POST
        CONTENT-TYPE : aplication/json
    '''

    # 서버에게 요청할 데이터 생성
    drink = {
        'serial_number' : SERIAL_NUMBER,  
        'sold_position' : sensings["sold_position"] 
        }
                            
    print('sensings : ', sensings)

    # 서버 요청
    response = requests.post(URL + '/rasp/drink/update', data = drink)
    # 응답 JSON 데이터 변환
    print("response")
    print(requests.post(URL + '/rasp/drink/update', data = drink))
    
    response = json.loads(response.text)

    # 서버에서 정상 처리 됐는지 확인
    if response["success"] :
        print("판매된 음료수 정보가 정상 차감되었습니다.")
    else :
        print("서버에서 판매 음료 정보 처리 중 에러가 발생하였습니다.\n서버 에러 메세지 : ", response["msg"])


# 스피커 출력 함수
def make_message(status, idx=None) :
    ''' 
        스피커 출력 함수
        gTTS 출력을 별도의 프로세스로 분할하여 동작시킨다.
        @ status : 현재 자판기의 상태
            (1) basic : 센싱되고 있지 않은 기본 상태
            (2) position : 손이 음료를 향해 위치한 상태
            (3) sold : 음료수가 팔린 상태
            (4) sold_out : 음료수 품절 상태
        @ idx : 음료의 포지션 배열 인덱스 ( ex : drinks["( VALUE )"][idx] )
    '''

    message = ""

    
    # 자판기 상태 검사
    if status == "basic" :
        ''' 센싱되고 있지 않은 기본 상태 '''

        # 자판기의 모든 음료 정보를 하나의 문자열로 병합
        names = ""
        for i, name in enumerate(drinks["name"]) :
            names += str(i+1) + '번 : ' + name + ' : '
                
        message = "안녕하세요, 말하는 음료수 자판기입니다. 지금부터, 음료수 위치와, 이름을 말씀드리겠습니다. " + names
        message = message + "입니다."
        
    elif status == "position" :
        ''' 손이 음료를 향해 위치한 상태  '''

        message = '선택하신' + drinks["name"][idx] + '는 : ' + str(drinks["price"][idx]) + '원, 입니다.'
    elif status == "sold" :
        ''' 음료수가 팔린 상태 '''
        message = drinks["name"][idx] + '를, 선택하셨습니다. : 맛있게 드시고 : 즐거운 하루 되십시오.'
    elif status == "sold_out" :
        ''' 음료수 품절 상태 '''
        message = drinks["name"][idx] + '는 : 품절입니다.'

    print(message)

    return message
    

def speak_message(message, mp3): #message: 출력 메시지, mp3: mp3 파일이름 지정
    # mp3 변환 및 출력, 한국어
    tts = gTTS(text = message, lang='ko')
    tts.save(mp3)

    mixer.init(25100)  #음성출력 속도 조절
    mixer.music.load(mp3)
    mixer.music.play()

# 파일이 직접 실행됐다면 (모듈로써 사용된게 아니라면) 실행
if __name__ == "__main__":
    main()
