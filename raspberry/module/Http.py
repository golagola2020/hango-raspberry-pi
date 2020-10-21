# 외장모듈
import requests, json           # HTTP 통신 및 JSON 모듈

# 내장모듈
import API
from DataManager import DataManager
from Serial import Serial
from config import *


class Http:
  '''
      @ Http Class
  '''

  @staticmethod
  # 음료수 정보 요청 함수
  def request_drinks(serial_number):
    '''
        서버에게 음료수 정보를 요청 및 응답 받는 함수

        URL : /rasp/drink/read
        METHOD : POST
        CONTENT-TYPE : application/json
    '''

    # 서버에게 요청할 데이터 생성
    drink = {
        'serial_number': serial_number
    }

    # 서버 요청
    response = requests.post(API.READ_DRINKS_PATH, data=drink)
    # 응답 JSON 데이터 변환
    response = json.loads(response.text)

    return response
  
  @staticmethod
  # 판매된 음료수 정보 차감 요청 함수
  def update_sold_drink(user_id, serial_number, drink) :
    '''
        서버에게 판매된 음료수 정보를 전달하는 함수

        URL : /rasp/drink/update
        METHOD : POST
        CONTENT-TYPE : application/json
    '''

    # 서버에게 요청할 데이터 생성
    request = {
        'user_id' : USER_ID,
        'serial_number' : SERIAL_NUMBER,
        'drink_name' : drink['name'],
        'drink_price' : drink['price'],
        'drink_sold_position' : drink['sold_position'] + 1
    }

    # 서버 요청
    response = requests.post(API.UPDATE_DRINKS_PATH, data = request)
    
    # 응답 JSON 데이터 변환
    response = json.loads(response.text)

    return response

   