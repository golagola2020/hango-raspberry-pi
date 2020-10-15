
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
        # 전역 변수 초기화
        del self.drinks["position"][:]
        del self.drinks["name"][:]
        del self.drinks["price"][:]
        del self.drinks["count"][:]

        # 데이터 삽입
        for drink in response["drinks"]:
            self.drinks["position"].append(drink["position"])
            self.drinks["name"].append(drink["name"])
            self.drinks["price"].append(drink["price"])
            self.drinks["count"].append(drink["count"])
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