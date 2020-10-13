

# 서버에서 전달받은 음료 정보가 저장될 전역 변수
drinks = {
  'position': [],
  'name': [],
  'price': [],
  'count': []
}

class DataManager:
  '''
      @ DataManager Class
  '''

  @staticmethod
  def get_drinks():
    '''
        음료 정보를 반환해주는 함수
    '''
    return drinks

  @staticmethod
  def set_drinks(response={'success': False}):
    '''
        서버에서 전달받은 데이터를 전역변수로 설정하는 함수
    '''

    # 서버의 성공 여부와 음료수 정보를 응답 받았는지 검사
    if response["success"] == True and "drinks" in response:
        # 전역 변수 초기화
        del drinks["position"][:]
        del drinks["name"][:]
        del drinks["price"][:]
        del drinks["count"][:]

        # 데이터 삽입
        for drink in response["drinks"]:
            drinks["position"].append(drink["position"])
            drinks["name"].append(drink["name"])
            drinks["price"].append(drink["price"])
            drinks["count"].append(drink["count"])
    else:
        # 서버 에러 메세지 출력
        print("음료를 세팅할 수 없습니다.\n서버 에러 메세지 : ", response["msg"])

  @staticmethod
  def check_drink_update(response={'success': False}):
    '''
        판매된 음료가 정상 차감됐는지 확인하는 함수
    '''

     # 서버에서 정상 처리 됐는지 확인
    if response["success"] :
        print("판매된 음료수 정보가 정상 차감되었습니다.")
    else :
        print("서버에서 판매 음료 정보 처리 중 에러가 발생하였습니다.\n서버 에러 메세지 : ", response["msg"])