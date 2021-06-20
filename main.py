#-*-coding: utf-8-*-
from flask import Flask, jsonify
from flask import request
import json

import recommend_foods
from recipe_embedding import menu_embedding
import KakaoLocalApi
import rest_api_key


app = Flask(__name__)

food_freq = {}
user_feedback = {}
dummy_data = {'anme':'이름', 'age':'나이'}

@app.route('/method', methods=['GET'])
def method():
    if request.method == 'GET':
        #print(request.args.to_dict())
        food_freq = json.loads(request.args.to_dict()['food_freq'])
        user_feedback = json.loads(request.args.to_dict()['user_feedback'])
        for key in food_freq.keys():
            food_freq[key] = int(food_freq[key])
        for key in user_feedback.keys():
            user_feedback[key] = int(user_feedback[key])
        print("food_freq: {}".format(food_freq))
        print("user_feedback: {}".format(user_feedback))
        print("\n")

        # ---- Recommend_foods ----
        recommend_foods.add_user_feedback(food_freq, user_feedback) # food_freq에 user_feedback 적용

        menu2vec = menu_embedding.load_menu2vec(filepath='./recipe_embedding/', filename='_menu2vec_wv')

        food_freq = dict(sorted(food_freq.items(), key=(lambda x: x[1]), reverse=True)) # food_pref_dict를 정렬
        print("sorted food_preference_dict: {}".format(food_freq))

        food_sim = recommend_foods.get_food_sim(menu2vec, food_freq, 10)  # 각 key값에 대해 유사메뉴 리스트 생성
        food_recommend, food_sim_dict = recommend_foods.get_food_recommend(food_freq, food_sim, size=10) # 최종 추천 리스트 생성

        food_rec_query_result = recommend_foods.KakaoLocalQuery(food_recommend, size=10) # 최종 추천리스트에 해당하는 음식점 검색

        # ----json 데이터 정리----
        frc_response = {}
        food_rec_info = []
        for key, sim in food_sim_dict.items():
            tmp_dict = {}
            tmp_dict['name'] = key
            tmp_dict['similarity'] = sim
            tmp_dict['num'] = food_rec_query_result[key]['meta']['total_count']
            food_rec_info.append(tmp_dict)
        frc_response['info'] = food_rec_info

        food_rec_data = []
        for key in food_rec_query_result.keys():
            food_rec_data_dict = {}
            food_rec_data_dict['menuName'] = key
            food_rec_data_dict['meta'] = food_rec_query_result[key]['meta']
            food_rec_data_dict['document'] = food_rec_query_result[key]['documents']
            food_rec_data.append(food_rec_data_dict)
        frc_response['data'] = food_rec_data

        return frc_response

@app.route('/reco', methods=['GET'])
def reco():
    if request.method == 'GET':
        #print(request.args.to_dict())
        food_freq = json.loads(request.args.to_dict()['food_freq'])
        user_feedback = json.loads(request.args.to_dict()['user_feedback'])
        for key in food_freq.keys():
            food_freq[key] = int(food_freq[key])
        for key in user_feedback.keys():
            user_feedback[key] = int(user_feedback[key])
        print("food_freq: {}".format(food_freq))
        print("user_feedback: {}".format(user_feedback))
        print("\n")

        # ---- Recommend_foods ----
        recommend_foods.add_user_feedback(food_freq, user_feedback) # food_freq에 user_feedback 적용

        menu2vec = menu_embedding.load_menu2vec(filepath='./recipe_embedding/', filename='_menu2vec_wv')

        food_freq = dict(sorted(food_freq.items(), key=(lambda x: x[1]), reverse=True)) # food_pref_dict를 정렬
        print("sorted food_preference_dict: {}".format(food_freq))

        food_sim = recommend_foods.get_food_sim(menu2vec, food_freq, 10)  # 각 key값에 대해 유사메뉴 리스트 생성
        food_recommend, food_sim_dict = recommend_foods.get_food_recommend(food_freq, food_sim, size=10) # 최종 추천 리스트 생성

        food_rec_query_result = recommend_foods.KakaoLocalQuery(food_recommend, size=10) # 최종 추천리스트에 해당하는 음식점 검색

        # ----json 데이터 정리----
        frc_response = {}
        food_rec_info = []
        for key, sim in food_sim_dict.items():
            tmp_dict = {}
            tmp_dict['name'] = key
            tmp_dict['similarity'] = sim
            tmp_dict['num'] = food_rec_query_result[key]['meta']['total_count']
            food_rec_info.append(tmp_dict)
            print("appended"+key)
        frc_response['info'] = food_rec_info

        return food_rec_info)   
    
@app.route('/detail/<menu_name>', methods=['GET'])
def datail(menu_name):
    if request.method == 'GET':
        
        key = rest_api_key.key

        return KakaoLocalApi.local_api_keyword(rest_api_key=key, keyword=menu_name, size=10)
    
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
