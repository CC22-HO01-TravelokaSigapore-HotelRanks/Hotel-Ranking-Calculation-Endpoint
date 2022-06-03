import traceback

# Get Cached Database
from database_cache import db

# For API stuff
from fastapi import APIRouter, Response, status, Request

# Hotel similarity function
from modules.near_you.function import *

near_you_router = APIRouter()
@near_you_router.post("/near_you/")
async def sentiment_similarity(request: Request, response: Response):
    """
    An API for giving recommendation with weighted sentiment 
    """
    try:        
        df_hotels = db.get_dataframe("hotels").copy()
        json_req = await request.json()
        latitude = json_req["latitude"]
        longitude = json_req["longitude"]

        if not (type(latitude) == float and type(longitude) == float):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return "Position is not found/cached yet in ML. Please do recached on POST /re-cached/"

        user_coor = (latitude, longitude)
        return near_you(user_coor,df_hotels)
    except Exception as e:
        traceback.print_exc()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return "Internal server error"