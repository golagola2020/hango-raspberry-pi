'''
    Copyright (C) 2020 Golagola

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
 
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
'''    

# 외장모듈
import os, sys                  # 시스템 모듈
import serial                   # 직렬 통신 모듈

# 경로설정
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{CURRENT_PATH}/module')

# 내장모듈
from module.config import *
from module.Http import Http
from module.DataManager import DataManager
from module.Speak import Gspeak
from module.Serial import Serial
    
# 메인 함수
def main():
    try:
        # 아두이노와 시리얼 통신할 인스턴스 생성 
        port = serial.Serial(
            port = PORT,
            baudrate = 9600
        )
        print(f'아두이노로부터 데이터를 수신합니다.\n현 메세지 출력 후 동작이 멈췄다면 아두이노와 라즈베리파이의 시리얼 포트가 일치하는지 config.py를 확인해주십시오.\n현재 포트 : {PORT}')
        # 캐시 비우기
        port.flushInput()
    except:
        print(f'오류 : {PORT} -> 잘못된 신호입니다.\n시리얼 모니터를 꺼주시거나 연결된 포트가 올바른지 config.py를 확인해주십시오.')
        exit(1)

    # 아두이노 센싱 데이터 한 줄 단위로 수신 -> 현 시리얼 포트가 통신 가능한지 테스트용으로 먼저 수신해보는 것.
    receive = Serial.get_receive_data(port)

    # 인스턴스 생성
    data_manager = DataManager()    # 음료 데이터 관리용 인스턴스
    speak = Gspeak(25100)           # gTTS를 사용하여 Hango 음성 출력을 제공하는 인스턴스 => 인자는 음성 출력 속도

    # 음료수 정보 요청
    response = Http.request_drinks(SERIAL_NUMBER)
    data_manager.refresh_drinks(response)

    # 초기 사운드 메세지 설정
    drinks = data_manager.get_drinks()
    speak.refresh_message(drinks)

    # 설정된 메세지 오브젝트 불러오기
    sound_msgs = speak.get_sound_msgs()
    
    # 음료수 이름을 파일명으로하는 사운드 만들고 저장
    for file_path in sound_msgs.keys() :
        try :
            file_name_items = os.listdir(f"{CURRENT_PATH}/sounds/{file_path}")
        except :
            print(f"'main.py'와 같은 경로에 'sounds' 폴더가 존재하는지 확인해주십시오.\n'sounds' 폴더 안에는 'basic', 'position', 'duplicate', 'sold', 'soldout' 폴더가 필수로 존재해야 합니다.")
            exit()
        for file_name, message in sound_msgs[file_path].items() :
            # 이미 만들어진 음성 파일이 아닐 경우에만 새로 만든다
            if file_name+'.mp3' not in file_name_items :
                print(f"음성 파일 생성\nFILE_PATH : {file_path}\nFILE_NAME : {file_name}\nMESSAGE : {message}")
                speak.save_sound(file_path, file_name, message)

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

                    # 캐시 비우기
                    port.flushInput()
                    
                    # 판매된 음료수가 있을 경우에 실행
                    if sensings["sold_position"] != -1 :
                        # 감지 정보가 새로운 감지 정보와 다르면 실행 => 같은 말을 반복하지 않기 위함
                        if Serial.current_sensing_data != sensings["sold_position"] :
                            # 새로 감지된 정보 저장 => 같은 말을 반복하지 않기 위함
                            Serial.current_sensing_data = f"sold_position {sensings['sold_position']}"

                            drink = {
                                'name' : drinks["name"][sensings["sold_position"]],
                                'price' : drinks["price"][sensings["sold_position"]],
                                'sold_position' : sensings["sold_position"]
                            }

                            # 판매된 음료수 정보 차감 요청
                            print("판매된 음료 차감 데이터를 요청하고 스피커 출력을 실행합니다.")
                            response = Http.update_sold_drink(USER_ID, SERIAL_NUMBER, drink)
                            data_manager.check_drink_update(response)

                            # 스피커 출력
                            speak.stop()
                            print("스피커 출력을 실행합니다.")

                            # 해당 음료가 품절일 경우 실행
                            if drinks["count"][sensings["sold_position"]] <= 0 :
                                # 스피커 출력
                                speak.say("sold_out", drinks["name"][sensings["sold_position"]])
                            else :
                                # 스피커 출력
                                speak.say("sold", drinks["name"][sensings["sold_position"]])

                    elif sensings["duplicate"] :
                        # 감지 정보가 새로운 감지 정보와 다르면 실행 => 같은 말을 반복하지 않기 위함
                        if Serial.current_sensing_data != sensings["duplicate"] :
                            # 새로 감지된 정보 저장 => 같은 말을 반복하지 않기 위함
                            Serial.current_sensing_data = f"duplicate {sensings['duplicate']}"

                            # speak.exit()
                            speak.stop()
                            print("물체가 감지되어 스피커 출력을 실행합니다.")

                            # 스피커 출력
                            speak.say("duplicate", "duplicate")
                            
                    # 손이 음료 버튼에 위치했을 경우에 실행
                    elif sensings["sensed_position"] != -1 :
                        # 감지 정보가 새로운 감지 정보와 다르면 실행 => 같은 말을 반복하지 않기 위함
                        if Serial.current_sensing_data != sensings["sensed_position"] :
                            # 새로 감지된 정보 저장 => 같은 말을 반복하지 않기 위함
                            Serial.current_sensing_data = f"sensed_position {sensings['sensed_position']}"

                            # speak.exit()
                            speak.stop()
                            print("물체가 감지되어 스피커 출력을 실행합니다.")

                            # 해당 음료가 품절일 경우 실행
                            if drinks["count"][sensings["sensed_position"]] <= 0 :
                                # 스피커 출력
                                speak.say("sold_out", drinks["name"][sensings["sensed_position"]])
                            else :
                                # 스피커 출력
                                speak.say("position", drinks["name"][sensings["sensed_position"]])
                            
                    # 수신한 변수명 집합 비우기 => 다음 센싱 때에도 정상 수신하는지 검사하기 위함 
                    received_keys.clear()
            
            # 음성 출력이 가능하면 실행 => 이미 음성이 출력 중일 땐 실행되지 않는다.
            if "success" in sensings and speak.is_available():

                # 음료수 정보 요청
                print("센싱 데이터가 없습니다.\n서버로부터 음료 정보를 불러옵니다...")
                response = Http.request_drinks(SERIAL_NUMBER)
                data_manager.refresh_drinks(response)

                # 수정된 음료수가 있다면 사운드 파일 업데이트
                drinks = data_manager.get_drinks()
                speak.update_message(drinks)

                # 스피커 출력
                print("스피커 출력을 실행합니다.\n:인사말 ")
                speak.stop()
                speak.say("basic")
        else :
            print("수신 가능한 센싱 데이터가 아닙니다.")
                


# 파일이 직접 실행됐다면 (모듈로써 사용된게 아니라면) 실행
if __name__ == "__main__":
    main()
