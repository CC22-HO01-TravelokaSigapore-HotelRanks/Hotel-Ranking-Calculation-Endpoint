import pandas as pd
import sqlalchemy as sql_a

class DatabaseCache:
    engine = None
    database_query = {
        "review_sentiment" : "SELECT user_id, review_id, sentiment FROM Review" 
    }
    df = {}
    
    def __init__(self, con_str: str) -> None:
        # Create SQL Alchemy Connection to the Database
        # self.engine = sql_a.create_engine(con_str)
        # self.engine.connect()
        pass
    
    def update_df(self) -> None:
        for i in self.database_query:
            self.df[i] = pd.read_sql(self.database_query[i])
                
    def get_dataframe(self, name:str) -> pd.DataFrame:
        return self.df[name]
    
# Instantiate Database Cache
db = DatabaseCache("")