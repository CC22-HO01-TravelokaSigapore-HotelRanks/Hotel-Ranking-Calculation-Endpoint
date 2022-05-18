# Get Cached Database
from database_cache import db

# For API stuff
from fastapi import APIRouter, Response, status
import pandas as pd
import numpy as np

# Hotel Similarity
import modules.hotel_similarity as similarity_mods

router = APIRouter()

@router.get("/")
async def hello_world():
    return "Hello from hotel ranking calculation endpoint"

@router.post("/re-cached/")
async def re_cached_db(response: Response):
    try:
        db.update_df()
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return "Cannot re-cached the server"

@router.get("/rows-cached/")
async def hotel_ranking(response: Response):
    try:
        dfs_rows = {}
        for i in db.df:
            dfs_rows[i] = len(db.get_dataframe(i))
        return dfs_rows
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return "Internal server error"

@router.post("/hotel-similarity/{hotel_id}")
async def hotel_similar(hotel_id: int, response: Response):
    """
    An API for calculating similarity between hotel of interest and the other
    hotel using cosine similarity. 
    """
    try:
        df = db.get_dataframe("hotels").copy()
        
        # # Check if hotel of interest is in the dataframes
        # # WARNING NO ID CHECKING
        # if not similarity_mods.id_is_available(hotel_id, df):
        #     response.status_code = status.HTTP_400_BAD_REQUEST
        #     return "Hotel ID is not found/cached yet in ML. Please do recached on POST /re-cached/"
        
        # Calculate cosine similarity and give recommendation
        # TODO: Convert ids to idx
        idx_recommendation = similarity_mods.hotel_similarity(hotel_id, 10, df)
        # TODO: Convert idx recommendation to ids
        return idx_recommendation.tolist()
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return "Internal server error"