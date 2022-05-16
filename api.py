# Get Database Caching
from database_cache import db

# For API stuff
from fastapi import APIRouter
from hotel_ranking import hotel_similarities

router = APIRouter()

@router.get("/")
async def hello_world():
    return "Hello from hotel ranking calculation endpoint"

@router.post("/hotel-ranking/")
async def hotel_ranking():
    df = db.get_dataframe("hotel")
    return hotel_similarities(0, df)