from gensim.models import KeyedVectors
import csv
import os


def get_sum (recipe_tot):
  ans = 0
  i=1
  for i in range(recipe_tot):
    ans+=i
  return ans

def get_menu2vec(loaded_wv, filepath = '../recipe_data/'):
  menu2vec = KeyedVectors(vector_size=100) # menu embedding 결과를 저장

  menu_name = ""  # 메뉴명 문자열
  # menu_dict = {}  # 메뉴 딕셔너리
  recipe_sum=0 #csv 파일 속 레시피 수
  recipe_idx = 0
  # direction = './recipe_data/'
  print(os.listdir(filepath))
  recipe_folder = os.listdir(filepath)
  for i, folder in enumerate(recipe_folder):  # 폴더 속 탐색
    csv_filepath = os.listdir(filepath + folder)
    for j, csv_file in enumerate(csv_filepath):  # csv 파일 속 탐색
      fi = open(filepath + folder + '/' + csv_file, 'rt', encoding='UTF8')
      rdr = csv.reader(fi)
      recipe_vec = [0 for i in range(100)]  # 100 : wv size
      for k, row in enumerate(rdr):
        if k == 0:
          print(row)
          menu_name = row[0]  # 메뉴 이름
          recipe_idx = int(row[2]) # total recipe number
          recipe_sum = get_sum(recipe_idx)
          continue
        elif k % 2 == 0:
          # 레시피별 벡터 계산(wv 활용)
          # 모든 레시피 평균 구하기
          tmp_vec = [0 for i in range(100)]  # 100 : wv size
          for l, ingredient in enumerate(row): #추천순대로 비중을 둬서 반영
            tmp_vec = [tmp_vec[i]+(loaded_wv[ingredient][i] / len(row)) for i in range(100)]
          recipe_vec = [recipe_vec[i]+ (tmp_vec[i]*recipe_idx/recipe_sum) for i in range(100)]
          recipe_idx-=1
      #menu_dict[menu_name] = recipe_vec
      menu2vec.add_vector(menu_name, recipe_vec)
      fi.close()

  print("length of menu2vec: %i" %(len(menu2vec.index_to_key)))
  print("menu2vec embedding finished!")
  return menu2vec


def save_menu2vec(menu2vec, filepath = './recipe_embedding/', filename = '_menu2vec_wv'):
  menu2vec.save(filepath + filename)

def load_menu2vec(filepath = './recipe_embedding/', filename = '_menu2vec_wv'):
  return KeyedVectors.load(filepath + filename)


