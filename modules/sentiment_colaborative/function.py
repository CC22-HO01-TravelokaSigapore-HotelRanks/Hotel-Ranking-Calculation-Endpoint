import pandas as pd
import numpy as np
from typing import List
from sklearn.metrics.pairwise import cosine_similarity

def create_matrix(df_in: pd.DataFrame, users_id: pd.DataFrame, hotels_id: pd.DataFrame):
  """
  Will create sentiment matrix of the users and the hotel. 
  It will returned matrix filled with 0, 0.5, 1 (0 negative, 0.5 not reviewed / neutral, 1 positives)
  """
  df = df_in
  user_id = users_id["id"].to_list()
  hotels_id = hotels_id["id"].to_list()

  data = {
      "user_id_cols" : user_id
  }
  matrix = pd.DataFrame(data).set_index("user_id_cols", drop=True)
  num_users = len(user_id)
  for i in hotels_id:
    # Init column
    temp_arr = np.empty(num_users)
    temp_arr[:] = 0.5
    matrix[i] = temp_arr

    # Fill User and sentiment
    user_sentiments = df[df["hotel_id"] == i][["user_id", "labels"]].values
    for j in user_sentiments:
      # Example of user_sentiments
      # ([[ 67,   1],
      #  [ 96,   0],
      #  [ 83,   1],
      #  [  6,   1],
      #  [ 31,   1], ...
      matrix.at[j[0], i] = j[1]

  return matrix.copy()

def get_user_similarity(matrix: pd.DataFrame, user_id: int):
  y = matrix.loc[user_id].values
  x = matrix.values
  return cosine_similarity(x, y.reshape(1,-1)).reshape(1,-1)[0]

def get_hotel_not_reviewed(matrix: pd.DataFrame, user_id: int):
  return matrix.loc[user_id][matrix.loc[user_id] == 0.5].index.values  

def give_recommendation(num_recs:int, matrix: np.ndarray, 
                        hotel_not_reviewed: np.ndarray, 
                        user_weights: np.ndarray) -> List:
  # Let's try to calculate predicted sentiment (higher is better becasue 1 is positive and 0 is negative)
  predicted_values = np.zeros(len(hotel_not_reviewed))
  for i in range(len(hotel_not_reviewed)):
    predicted_values[i] = (matrix[matrix.columns[i]].values @ user_weights) / sum(user_weights)
  hotel_order = np.argsort(predicted_values)[::-1][:len(hotel_not_reviewed)]
  final_recs = []
  for i in range(min([len(hotel_not_reviewed), num_recs])):
    final_recs.append(int(hotel_not_reviewed[hotel_order[i]]))

  return final_recs