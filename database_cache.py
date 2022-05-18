import pandas as pd
import sqlalchemy as sql_a
import os

class DatabaseCache:
    engine = None
    database_query = {
        "hotels" : "SELECT * FROM hotel_dummy_photos" 
    }
    df = {}
    
    def __init__(self, con_str: str) -> None:
        # Create SQL Alchemy Connection to the Database
        self.engine = sql_a.create_engine(con_str, connect_args={'connect_timeout': 5})
        self.engine.connect()
        print("INFO: Database Connected")
        self.update_df()
    
    def update_df(self) -> None:
        print("INFO: Updating Database Cache")
        for i in self.database_query:
            self.df[i] = pd.read_sql(self.database_query[i], self.engine)
        print("INFO: Database Cached")
                
    def get_dataframe(self, name:str) -> pd.DataFrame:
        return self.df[name]
    
# Instantiate Database Cache
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database_name = os.getenv("DB_NAME")
db = DatabaseCache(f"mysql://{username}:{password}@{host}:{port}/{database_name}")