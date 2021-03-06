# Get Cached Database
from database_cache import db

# For API stuff
from fastapi import APIRouter, Response, status
import pandas as pd
import numpy as np

router = APIRouter()

@router.get("/")
async def hello_world():
    return {"message" : "Hello from hotel ranking calculation endpoint"}

@router.post("/re-cached/")
async def re_cached_db(response: Response):
    try:
        db.update_df()
        return {"message" : "Success"}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message" : "Cannot re-cached database"}

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
        return {"message" : "Internal server error"}
    
# Hotel Similarity endpoint
from modules.hotel_similarity.api import hotel_similarity_router
router.include_router(hotel_similarity_router)

# Sentiment Similarity endpoint
from modules.sentiment_colaborative.api import sentiment_similarity_router
router.include_router(sentiment_similarity_router)

# Trending endpoint
from modules.trending_system.api import trending_system_router
router.include_router(trending_system_router)

# Near You endpoint
from modules.near_you.api import near_you_router
router.include_router(near_you_router)