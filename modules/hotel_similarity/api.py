# Get Cached Database
from database_cache import db

# For API stuff
from fastapi import APIRouter, Response, status

# Hotel similarity function
from modules.hotel_similarity.function import *

hotel_similarity_router = APIRouter()

@hotel_similarity_router.post("/hotel-similarity/{hotel_id}")
async def hotel_similar(hotel_id: int, response: Response):
    """
    An API for calculating similarity between hotel of interest and the other
    hotel using cosine similarity. 
    """
    try:
        df = db.get_dataframe("hotels").copy()
        
        # Preprocess Dataframes
        df = preprocess_dataframe(df)
        
        # Check if hotel of interest is in the dataframes
        # WARNING NO ID CHECKING
        if not id_is_available(hotel_id, df):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return "Hotel ID is not found/cached yet in ML. Please do recached on POST /re-cached/"
        
        # Calculate cosine similarity and give recommendation
        hotel_id = id_to_index(hotel_id, df)
        idx_recommendation = give_recommendation(hotel_id, 10, df)
        idx_recommendation = index_to_id(idx_recommendation, df)
        return idx_recommendation.tolist()
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return "Internal server error"