# Dotenv if available
print("INFO: Loading dotenv if available")
from dotenv import load_dotenv
load_dotenv()

# For Database Caching
print("INFO: Testing Database")
from database_cache import db

# Scheduling for Database Caching
print("INFO: Loading scheduler")
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(db.update_df, 'interval', minutes=1)
scheduler.start()

# For API
import uvicorn
from fastapi import FastAPI
from api import router
# Instantiate API
api = FastAPI()
api.include_router(router)

# Init Endpoint
port = 8001
print(f"Listening to http://0.0.0.0:{port}")
uvicorn.run(api, host='0.0.0.0',port=port)