import traceback

# Get Cached Database
from database_cache import db

# For API stuff
from fastapi import APIRouter, Response, status

# Hotel similarity function
from modules.near_you.function import *

near_you_router = APIRouter()

@near_you_router.post("/near_you/{coordinate}")
async def sentiment_similarity(coordinate: tuple, response: Response):
    """
    An API for giving recommendation with weighted sentiment 
    """
    try:        
        df_hotels = db.get_dataframe("hotels").copy()
        user_coor = (-8.685924978406074, 115.16562524113574)
        return near_you(user_coor,df_hotels)
    except Exception as e:
        traceback.print_exc()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return "Internal server error"