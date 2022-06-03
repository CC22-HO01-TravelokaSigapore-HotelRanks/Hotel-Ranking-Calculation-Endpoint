import traceback

# Get Cached Database
from database_cache import db

# For API stuff
from fastapi import APIRouter, Response, status

# Hotel similarity function
from modules.sentiment_colaborative.function import *

sentiment_similarity_router = APIRouter()

@sentiment_similarity_router.post("/sentiment-similarity/{user_id}")
async def sentiment_similarity(user_id: int, response: Response):
    """
    An API for giving recommendation with weighted sentiment 
    """
    try:
        df_users = db.get_dataframe("users_id")
        if user_id not in df_users["id"].to_list():
            print("Masuk")
            response.status_code = status.HTTP_400_BAD_REQUEST
            return "User ID is not found/cached yet in ML. Please do recached on POST /re-cached/"
        
        df_reviews = db.get_dataframe("reviews_sentiment")
        df_hotels = db.get_dataframe("hotels_id")
        
        matrix = create_matrix(df_reviews, df_users, df_hotels)
        similarity = get_user_similarity(matrix, user_id)
        not_reviewed = get_hotel_not_reviewed(matrix, user_id)
        return give_recommendation(10, matrix, not_reviewed, similarity)
    except Exception as e:
        traceback.print_exc()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return "Internal server error"