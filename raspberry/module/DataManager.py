
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
    if response["success"] == True and "drinks" in response:
        # 데이터 삽입
        for i in range(len(response["drinks"])):
            if self.drinks["name"][i] != response["drinks"]["name"][i]:
              # 기존 음료의 음성 파일들 삭제
              os.remove(f'{RPI_FILE_PATH}/sounds/basic/basic.mp3')
              os.remove(f'{RPI_FILE_PATH}/sounds/position/{self.drinks["name"][i]}.mp3')
              os.remove(f'{RPI_FILE_PATH}/sounds/sold/{self.drinks["name"][i]}.mp3')
              os.remove(f'{RPI_FILE_PATH}/sounds/sold_out/{self.drinks["name"][i]}.mp3')

              # 변경된 데이터 변경
              self.drinks["name"][i] = response["drinks"]["name"][i]
              self.drinks["position"][i] = response["drinks"]["position"][i]
              self.drinks["price"][i] = response["drinks"]["price"][i]
              self.drinks["count"][i] = response["drinks"]["count"][i]
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