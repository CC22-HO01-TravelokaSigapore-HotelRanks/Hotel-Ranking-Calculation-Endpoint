import pandas as pd
import numpy as np
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
import haversine as hs

def distance_from(loc1,loc2): 
    distance = hs.haversine(loc1,loc2)
    return distance

def near_you(user_coor,df_hotel):
    distances_km = []
    df_hotel['coor'] = list(zip(df_hotel.latitude, df_hotel.longitude))
    for row in df_hotel.itertuples(index=False):
        distances_km.append(distance_from(user_coor, row.coor))
    df_hotel['distance_from_user'] = distances_km
    df_near_you = df_hotel.sort_values(['distance_from_user', 'hotel_star'], ascending=[True, False])
    list_id_near_you = df_near_you['id'].tolist()
    
    return list_id_near_you