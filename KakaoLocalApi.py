import json
import requests


def local_api_keyword(rest_api_key, keyword, size=10, page=1):
  headers = {"Authorization": "KakaoAK {}".format(rest_api_key)}
  url_keyword = "https://dapi.kakao.com/v2/local/search/keyword.json?"  # 키워드로 검색
  params = {'query': keyword}  # 검색할 quary
  params['x'] = '126.93927007202764'  # 중심좌표 (서강대학교의 x,y 좌표)
  params['y'] = '37.55123227549557'
  params['radius'] = '3000'  # (x,y)좌표의 반경 3000m 내에서 검색
  params['size'] = size  # 전체 데이터를 'size'개씩 나누어서 받음
  params['page'] = page  # 'size'개씩 나누어진 데이터 중 'page'번째 페이지

  req = requests.get(url_keyword, headers=headers, params=params)
  json_object = json.loads(req.text)
  return json_object
