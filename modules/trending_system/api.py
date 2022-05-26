# Get Cached Database
from database_cache import db
import traceback
# For API stuff
from fastapi import APIRouter, Response, status

# Hotel similarity function
from modules.trending_system.trend_functions import *

trending_system_router = APIRouter()

@trending_system_router.post("/trending_system/")
async def trending_system(response: Response):
    """
    An API for calculating similarity between hotel of interest and the other
    hotel using cosine similarity. 
    """
    try:
        df_hotels = db.get_dataframe("hotels").copy()
        df_reviews = db.get_dataframe("reviews").copy()

        # Preprocess Dataframes
        df_hotel_trend_id = preprocess_trend_reviews(df_hotels,df_reviews)
        return df_hotel_trend_id
    except Exception as e:
        traceback.print_exc()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return "Internal server error"