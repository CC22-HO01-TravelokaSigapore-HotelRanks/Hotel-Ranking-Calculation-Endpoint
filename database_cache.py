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
            temp_df = pd.read_sql(self.database_query[i], self.engine)
            temp_df.dropna(inplace=True)
            self.df[i] = self.df_evaluate_object(temp_df)
        print("INFO: Database Cached")
                
    def get_dataframe(self, name:str) -> pd.DataFrame:
        return self.df[name]
    
    @staticmethod
    def df_evaluate_object(df_in: pd.DataFrame) -> pd.DataFrame:
        df = df_in.copy()
        cols = df.columns.to_list()
        dtypes = df.dtypes
        for i in cols:
            if dtypes[i] == "O":
                try:
                    df[i] = df[i].map(pd.eval)
                except:
                    pass
        return df
    
# Instantiate Database Cache
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database_name = os.getenv("DB_NAME")
db = DatabaseCache(f"mysql://{username}:{password}@{host}:{port}/{database_name}")