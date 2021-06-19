from flask import Flask, jsonify
from flask import request
import json

import recommend_foods
from recipe_embedding import menu_embedding
import KakaoLocalApi

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
        food_recommend = recommend_foods.get_food_recommend(food_freq, food_sim, size=10) # 최종 추천 리스트 생성

        food_rec_query_result = recommend_foods.KakaoLocalQuery(food_recommend, size=10) # 최종 추천리스트에 해당하는 음식점 검색

        return food_rec_query_result

if __name__ == '__main__':
    app.run()