# Get Cached Database
from database_cache import db

# For API stuff
from fastapi import APIRouter
import pandas as pd
import numpy as np

router = APIRouter()

@router.get("/")
async def hello_world():
    return "Hello from hotel ranking calculation endpoint"

@router.get("/rows-cached/")
async def hotel_ranking():
    dfs_rows = {}
    for i in db.df:
        dfs_rows[i] = len(db.get_dataframe(i))
    return dfs_rows