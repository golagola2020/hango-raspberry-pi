

from config import *

class DataManager:
  '''
      @ DataManager Class
  '''

  def __init__(self):
    self.drinks = {
      'position': [],
      'name': [],
      'price': [],
      'count': []
    }

  def get_drinks(self):
    '''
        음료 정보를 반환해주는 함수
    '''
    return self.drinks

  def refresh_drinks(self, response={'success': False}):
    '''
        서버에서 전달받은 데이터를 전역변수로 설정하는 함수
    '''

    # 서버의 성공 여부와 음료수 정보를 응답 받았는지 검사
    print(f'서버 응답 데이터 : {response}') 
    if response["success"] == True and "drinks" in response:
        # 데이터 삽입
        if response["drinks"]:
          for i in range(len(response["drinks"])):
              if self.drinks["name"] and (self.drinks["name"][i] != response["drinks"][i]["name"] or self.drinks["price"][i] != response["drinks"][i]["price"]):
                # 기존 음료의 음성 파일들 삭제
                os.remove(f'{RPI_FILE_PATH}/sounds/basic/basic.mp3')
                os.remove(f'{RPI_FILE_PATH}/sounds/position/{self.drinks["name"][i]}.mp3')
                os.remove(f'{RPI_FILE_PATH}/sounds/sold/{self.drinks["name"][i]}.mp3')
                os.remove(f'{RPI_FILE_PATH}/sounds/sold_out/{self.drinks["name"][i]}.mp3')

                # 변경된 데이터 변경
                print(f'음료 데이터가 변경되었습니다.\n음료수 변경됨 : {drinks["name"][i]} -> {response["drinks"]["name"][i]}')
                self.drinks["name"][i] = response["drinks"][i]["name"]
                self.drinks["position"][i] = response["drinks"][i]["position"]
                self.drinks["price"][i] = response["drinks"][i]["price"]
                self.drinks["count"][i] = response["drinks"][i]["count"]
              elif not self.drinks["name"]:
                # 서버로부터 음료 데이터를 처음 수신하여 리스트에 저장
                print("서버로부터 수신한 데이터를 저장합니다...")
                for i in range(len(response["drinks"])):
                  self.drinks["name"].append(response["drinks"][i]["name"])
                  self.drinks["position"].append(response["drinks"][i]["position"])
                  self.drinks["price"].append(response["drinks"][i]["price"])
                  self.drinks["count"].append(response["drinks"][i]["count"])
                return
    else:
        # 서버 에러 메세지 출력
        print("음료를 세팅할 수 없습니다.\n서버 에러 메세지 : ", response["msg"])

  def check_drink_update(self, response={'success': False}):
    '''
        판매된 음료가 정상 차감됐는지 확인하는 함수
    '''

     # 서버에서 정상 처리 됐는지 확인
    if response["success"] :
        print("판매된 음료수 정보가 정상 차감되었습니다.")
    else :
        print("서버에서 판매 음료 정보 처리 중 에러가 발생하였습니다.\n서버 에러 메세지 : ", response["msg"])
