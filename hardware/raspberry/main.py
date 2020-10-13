'''
    @ Hango Project
    @ This raspberry.py file is the main file of the Hango Project
'''    

# 외장모듈
import os, sys                  # 시스템 모듈
import serial                   # 직렬 통신 모듈

# 경로설정
sys.path.append('/home/pi/hango-hardware/hardware/raspberry/module')

# 내장모듈
from module.config import *
from module.Http import Http
from module.DataManager import DataManager
from module.Speak import Espeak, Gspeak
from module.Serial import Serial
    
# 메인 함수
def main():
    # 아두이노와 시리얼 통신할 인스턴스 생성 
    port = serial.Serial(
        port = PORT,
        baudrate = 9600
    )
    # 캐시 비우기
    port.flushInput()

    # 음료수 정보 요청
    response = Http.request_drinks()
    DataManager.set_drinks(response)

    # 초기 사운드 메세지 설정
    drinks = DataManager.get_drinks()
    Gspeak.set_message(drinks)

    sound_msgs = Gspeak.get_sound_msgs()

    # 음료수 이름을 파일명으로하는 사운드 만들고 저장
    for file_path in sound_msgs.keys() :
        for file_name, message in sound_msgs[file_path].items() :
            Gspeak.save_sound(file_path, file_name, message)

    # 무한 반복
    while True:
        # 아두이노 센싱 데이터 한 줄 단위로 수신
        receive = Serial.get_receive_data(port)

        # 이용 가능한 데이터인지 검사
        if Serial.is_available(receive) :
            # 아두이노 수신 데이터 저장
            Serial.save_received_data(receive)
            received_keys = Serial.get_received_keys()

            # 아두이노 센싱 데이터 불러오기
            sensings = Serial.get_sensings()

            # 라즈베리파이가 가공할 데이터를 모두 수신 했다면 실행 
            if BASIC_KEYS.difference(received_keys) == set() :

                # 아두이노에서 센싱된 데이터가 있으면 실행 
                if sensings["success"] :
                    # 출력
                    print("센싱 데이터 수신 성공")
                    
                    # 판매된 음료수가 있을 경우에 실행
                    if sensings["sold_position"] != -1 :
                        # 감지 정보가 새로운 감지 정보와 다르면 실행 => 같은 말을 반복하지 않기 위함
                        if Serial.current_sensing_data != sensings["sold_position"] :
                            # 새로 감지된 정보 저장 => 같은 말을 반복하지 않기 위함
                            Serial.current_sensing_data = sensings["sold_position"]

                            # 판매된 음료수 정보 차감 요청
                            print("판매된 음료 차감 데이터를 요청하고 스피커 출력을 실행합니다.")
                            response = Http.update_sold_drink(drinks, sensings["sold_position"]+1)
                            DataManager.check_drink_update(response)

                            # 스피커 출력
                            print("스피커 출력을 실행합니다.")
                            Gspeak.say("sold", drinks["name"][sensings["sold_position"]-1])
                            
                    # 손이 음료 버튼에 위치했을 경우에 실행
                    elif sensings["sensed_position"] != -1 :
                        # 감지 정보가 새로운 감지 정보와 다르면 실행 => 같은 말을 반복하지 않기 위함
                        if Serial.current_sensing_data != sensings["sensed_position"] :
                            # 새로 감지된 정보 저장 => 같은 말을 반복하지 않기 위함
                            Serial.current_sensing_data = sensings["sensed_position"]

                            print("물체가 감지되어 스피커 출력을 실행합니다.")

                            # 해당 음료가 품절일 경우 실행
                            if drinks["count"][sensings["sensed_position"]-1] <= 0 :
                                # 스피커 출력
                                Gspeak.say("sold_out", drinks["name"][sensings["sold_position"]-1])
                            else :
                                # 스피커 출력
                                Gspeak.say("position", drinks["name"][sensings["sold_position"]-1])
                            
                    # 수신한 변수명 집합 비우기 => 다음 센싱 때에도 정상 수신하는지 검사하기 위함 
                    received_keys.clear()
                        
            # 아두이노에서 False만 보냈을 경우 => 아두이노에서 센싱된 데이터가 없으면 실행
            elif received_keys == {"success"} and sensings["success"] == False :
                # 감지 정보가 새로운 감지 정보와 다르면 실행 => 같은 말을 반복하지 않기 위함
                if Serial.current_sensing_data != sensings["success"] :
                    # 새로 감지된 정보 저장 => 같은 말을 반복하지 않기 위함
                    Serial.current_sensing_data = sensings["success"]

                    # 음료수 정보 요청 후 수정된 음료수가 있다면 사운드 파일 업데이트
                    print("센싱 데이터가 없습니다.\n서버로부터 음료 정보를 불러옵니다...")
                    response = Http.request_drinks()
                    DataManager.set_drinks(response)
                    drinks = DataManager.get_drinks()
                    Gspeak.update_message(drinks)

                    # 스피커 출력
                    print("스피커 출력을 실행합니다.\n:인사말 ")
                    Gspeak.say("basic")
        else :
            print("수신 가능한 센싱 데이터가 아닙니다.")
                


# 파일이 직접 실행됐다면 (모듈로써 사용된게 아니라면) 실행
if __name__ == "__main__":
    main()
