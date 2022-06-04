import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

from sqlalchemy import column

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
  
  df = delete_hotel_reconstruct(df)
  
  column_not_processed = ["latitude", "longitude", "name", "neighborhood", "type_nearby_destination", "image_links"]
  df.drop(columns=column_not_processed, inplace=True)
  
  # Min max normalization on all float or int64 columns
  # And changing boolean to number
  for i in df.columns:
    current_list = df[i].to_list()

    if i in column_not_processed + ["id"]:
      continue
    
    if df[i].dtypes in ["float64", "int64"]:
      df[i] = min_max_normalization(current_list)
    
    if df[i].dtypes == "bool":
      df[i] = df[i].astype(int)
      
  df.reset_index(drop=True, inplace=True)

  return df

def index_to_id(idx: int|List[int], df: pd.DataFrame) -> int:
  return df.iloc[idx]["id"]

def id_to_index(id: int, df: pd.DataFrame) -> int:
  return df[df["id"] == id].index[0]

def id_is_available(id: int, df: pd.DataFrame) -> bool:
  return  id in df["id"].to_list()

def delete_hotel_reconstruct(df_in:pd.DataFrame) -> pd.DataFrame:
  df = df_in.copy()
  # TODO: If using soft deltes, please be aware you need to delete row with the deleted_at is not null
  return df

def give_recommendation(idx:int, num_recs:int, df_in:pd.DataFrame) -> np.ndarray:
  df = df_in.copy()
  
  # Drop if id feature exist in df
  if "id" in df.columns:
    df.drop(columns=["id"], inplace=True)
  
  # Get Feature of Pivoted Hotel
  pivoted = df.iloc[idx].to_list()
  
  # Get similarity values
  similarity = cosine_similarity(df.values.tolist(), np.asarray(pivoted).reshape(1,-1)).reshape((1,-1))[0]
  
  # Sort the index and give bac
  sorted = np.argsort(similarity)[::-1][:num_recs+1]
  sorted_wo_first = sorted[1:]
  return sorted_wo_first