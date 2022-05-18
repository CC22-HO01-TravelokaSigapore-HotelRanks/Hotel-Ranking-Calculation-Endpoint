import pandas as pd
import sqlalchemy as sql_a
import os

class DatabaseCache:
    engine = None
    database_query = {
        "review_sentiment" : "SELECT user_id, review_id, sentiment FROM Review" 
    }
    df = {}
    
    def __init__(self, con_str: str) -> None:
        # Create SQL Alchemy Connection to the Database
        self.engine = sql_a.create_engine(con_str, connect_args={'connect_timeout': 5})
        self.engine.connect()
        print("INFO: Database Connected")        
    
    def update_df(self) -> None:
        for i in self.database_query:
            self.df[i] = pd.read_sql(self.database_query[i])
                
    def get_dataframe(self, name:str) -> pd.DataFrame:
        return self.df[name]
    
# Instantiate Database Cache
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database_name = os.getenv("DB_NAME")
db = DatabaseCache(f"mysql://{username}:{password}@{host}:{port}/{database_name}")