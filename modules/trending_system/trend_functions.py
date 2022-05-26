from datetime import date
from datetime import timedelta
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def mask(df):
    Today = pd.Timestamp('today').floor('D')
    mask = (df['dates'] > Today - timedelta(days=7)) & (df['dates'] <= Today)
    forecast_mask = df.loc[mask]
    df_list = forecast_mask.groupby('hotel_id').count()['text'] 
    df_list_2 = df.groupby('hotel_id')['rating'].mean()
    return df_list,df_list_2

def hotel_reviews(df_list,df_list_2,df_hotel_reviews):
    df_hotel_reviews['num_of_reviews'] = df_list
    df_hotel_reviews['avg_ratings'] = df_list_2
    df_hotel_reviews = df_hotel_reviews.fillna(0)
    trans = MinMaxScaler()
    df_hotel_reviews[["num_of_reviews","avg_ratings"]] = trans.fit_transform(df_hotel_reviews[["num_of_reviews","avg_ratings"]])
    df_hotel_reviews['score'] = df_hotel_reviews['num_of_reviews']*(df_hotel_reviews['avg_ratings']*1.2)
    df_hotel_reviews = df_hotel_reviews.sort_values(by = 'score',ascending = False)
    # between Column_1 or hotel_id
    list_id_review = df_hotel_reviews['id'].tolist()
    return list_id_review

def preprocess_trend_reviews(df_hotel,df_reviews):
    df_list,df_list_2 = mask(df_reviews)
    df_hotel_trend_id = hotel_reviews(df_list,df_list_2,df_hotel)

    return df_hotel_trend_id