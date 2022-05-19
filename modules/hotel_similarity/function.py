import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

# Min-max normalization
def min_max_normalization(arr:List) -> List:
  minimum = min(arr)
  maximum = max(arr)

  if (maximum - minimum) == 0:
    return arr

  for i in range(len(arr)):
    arr[i] = (arr[i] - minimum) / (maximum - minimum)
  return arr

# Preprocess df
def preprocess_dataframe(df_in: pd.DataFrame) -> pd.DataFrame:
  df = df_in.copy()
  column_not_processed = ["latitude", "longitude"]

  for i in df.columns:
    current_list = df[i].to_list()

    if i in column_not_processed:
      continue
    
    if df[i].dtypes in ["float64", "int64"]:
      df[i] = min_max_normalization(current_list)
    
    if df[i].dtypes == "bool":
      df[i] = df[i].astype(int)

  return df

def index_to_id(idx: int|List[int], df: pd.DataFrame) -> int:
  return df.iloc[idx]["id"]

def id_to_index(id: int, df: pd.DataFrame) -> int:
  return df[df["id"] == id].index[0]

def id_is_available(id: int, df: pd.DataFrame) -> bool:
  return  id in df["id"].to_list()

def give_recommendation(idx:int, num_recs:int, df:pd.DataFrame) -> np.ndarray:
  df_att = df.copy().drop(columns=["name", "neighborhood", "type_nearby_destination", "image_links"])
  df_att_norm = preprocess_dataframe(df_att)
  df_att_norm.drop(columns=["latitude", "longitude"], inplace=True)
  df_att_norm.dropna(inplace=True)
  pivoted = df_att_norm.iloc[idx].to_list()
  similarity = cosine_similarity(df_att_norm.values.tolist(), np.asarray(pivoted).reshape(1,-1)).reshape((1,-1))[0]
  sorted = np.argsort(similarity)[::-1][:num_recs+1]
  sorted_wo_first = sorted[1:]
  return sorted_wo_first