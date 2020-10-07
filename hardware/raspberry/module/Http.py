# 외장모듈
import requests, json           # HTTP 통신 및 JSON 모듈

# 내장모듈
from Env import *

class Http:
  '''
      @ Http Class
  '''

  @staticmethod
  # 음료수 정보 요청 함수
  def request_drinks():
    '''
        서버에게 음료수 정보를 요청 및 응답 받는 함수

        URL : /rasp/drink/read
        METHOD : POST
        CONTENT-TYPE : application/json
    '''

    # 서버에게 요청할 데이터 생성
    drink = {
        'serial_number': SERIAL_NUMBER
    }

    # 서버 요청
    response = requests.post(URL + '/rasp/drink/read', data=drink)
    # 응답 JSON 데이터 변환
    response = json.loads(response.text)

    # 서버에서 정상 응답이 온 경우
    if response["success"] == True:
        # 전역 변수 초기화
        del drinks["position"][:]
        del drinks["name"][:]
        del drinks["price"][:]
        del drinks["count"][:]

        # 서버 데이터 삽입
        for drink in response["drinks"]:
            drinks["position"].append(drink["position"])
            drinks["name"].append(drink["name"])
            drinks["price"].append(drink["price"])
            drinks["count"].append(drink["count"])

    else:
        # 서버 에러 메세지 출력
        print("서버에서 음료 정보 조회 중 에러가 발생하였습니다.\n서버 에러 메세지 : ", response["msg"])
  
  @staticmethod
  # 판매된 음료수 정보 차감 요청 함수
  def request_drinks_update() :
    '''
        서버에게 판매된 음료수 정보를 전달하는 함수

        URL : /rasp/drink/update
        METHOD : POST
        CONTENT-TYPE : application/json
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
    response = json.loads(response.text)

    # 서버에서 정상 처리 됐는지 확인
    if response["success"] :
        print("판매된 음료수 정보가 정상 차감되었습니다.")
    else :
        print("서버에서 판매 음료 정보 처리 중 에러가 발생하였습니다.\n서버 에러 메세지 : ", response["msg"])