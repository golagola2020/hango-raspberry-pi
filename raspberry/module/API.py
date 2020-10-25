import os       # 시스템 모듈

# 환경 변수명 지정
ENV = 'HANGO_URL'
try:
  # URL 환경 변수 불러오기
  URL = str(os.environ[ENV])
except:
  print(f"'{ENV}'는 존재하지 않는 환경 변수입니다.\n먼저, 환경 변수를 등록해주십시오.")
  exit(1)

# 서버 요청 및 응답 API
READ_DRINKS_PATH = URL + '/rasp/drink/read'
UPDATE_DRINKS_PATH = URL + '/rasp/drink/update'