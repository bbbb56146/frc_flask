import numpy as np

# import local files
from recipe_embedding import menu_embedding
import KakaoLocalApi
import rest_api_key


# food_pref_dic에 user_feedback을 ratio비율 만큼 추가함
def add_user_feedback (food_pref_dic, user_feedback, ratio = 0.25):
  for food in user_feedback.keys():
    if food in food_pref_dic.keys():
      food_pref_dic[food] += user_feedback[food] * ratio
    else:
      food_pref_dic[food] = user_feedback[food] * ratio


# food_pref_dic의 각 key에 대해서 유사메뉴리스트 얻기
def get_food_sim (menu2vec, food_pref_dic, topn=10):
  food_sim = {}  # food_freq의 각 food당 유사한 음식들의 목록
  for food in food_pref_dic:
    if food not in menu2vec.index_to_key:
      food_sim[food] = []
    else:
      food_sim[food] = menu2vec.most_similar(positive=[food], topn=topn)

  print('\n')
  for menu, sim in food_sim.items():
    print(menu, end=' -> ')
    print(sim)
  print('\n')

  return food_sim

# 최종 추천 리스트 생성
def get_food_recommend (food_pref_dic, food_sim, size=10):
  food_recommend = []  # 추천할 음식 list (각 음식 당 최대 freq개 만큼, similarity>0.90인 음식 선택)
  freq_sum = 0  # food_pref_dic의 freq 총합 (menu2vec에 없는 menu 제외)
  for food, freq in food_pref_dic.items():
    if len(food_sim[food]) != 0:
      freq_sum += freq
  food_pref_dic_mod = {} # freq 총합이 size에 가까워지도록 조정 (menu2vec에 없는 menu 제외)
  for food, freq in food_pref_dic.items():
    if len(food_sim[food]) != 0:
      food_pref_dic_mod[food] = round((freq / freq_sum) * size)
  print("number of menu recommended: {}".format(food_pref_dic_mod))

  food_sim_dict = {}
  for food, freq in food_pref_dic_mod.items():
    for i, food_sim_tuple in enumerate(food_sim.get(food)):
      if i >= freq:
        break
      elif food_sim_tuple[1] > 0.90:
        food_recommend.append(food_sim_tuple[0])
        food_sim_dict[food_sim_tuple[0]] = food_sim_tuple[1]
  print("food_recommend: {}".format(food_recommend))
  return food_recommend, food_sim_dict

# food_recommend의 각 food에 대해 Kakao local Api에 query를 한 결과
def KakaoLocalQuery (food_recommend, size = 10):
  food_rec_json_object = {}  # food_recommend의 각 food에 대해 KakaoLocalAPI에 검색한 음식점 정보 Dictionary
  key = rest_api_key.key
  for food in food_recommend:
    food_rec_json_object[food] = KakaoLocalApi.local_api_keyword(rest_api_key=key, keyword=food, size=size)
  return food_rec_json_object


