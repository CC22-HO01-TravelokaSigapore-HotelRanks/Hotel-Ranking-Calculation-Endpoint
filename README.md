# Hotel Ranking Calculation API

This is an endpoint for api for all our hotel ranking scripts.

# Environment Variables
| Variables   | Description                      |
|-------------|----------------------------------|
| DB_USER     | Database Username                |
| DB_PASSWORD | Database Password                |
| DB_HOST     | Database IP Address or Host name |
| DB_PORT     | Database Port                    |
| DB_NAME     | Database Name                    |

# APIs
## Hotel Similarity API
Hotel similarity endpoint based on almost all columns except `"name", "neighborhood", "type_nearby_destination", "image_links", "id"`.    
| Endpoint                     | Input                      | Output                                                           |
|------------------------------|----------------------------|------------------------------------------------------------------|
| POST `/hotel-similarity/{hotel_id}` | - | List of Hotel ID (Currently hardcoded to give 10 recommendation) |

Example:
If Success:  
![image](https://user-images.githubusercontent.com/61568092/169243556-4432b73c-e812-4c8c-b45e-101a009da98f.png)

If Hotel Ids is not cached in ML Endpoint or Cannot be Processed for Hotel Similarity:  
![image](https://user-images.githubusercontent.com/61568092/169243726-0f346f09-d498-4e53-815f-b13664c1b880.png)

## Collaborative Sentiment Filtering API
A recommendation system based on weighted similarity sentiment reivews
| Endpoint                               | Input | Output                                         |
|----------------------------------------|-------|------------------------------------------------|
| POST `/sentiment-similarity/{user_id}` | -     | List of Hotel ID with number hotel recommendation ranged from 0 to 10 |

**Please Be Aware** that the recommendation is not always give 10 ids of hotels.  
Example:  
If Success:  
![image](https://user-images.githubusercontent.com/61568092/169698056-96480a98-ca74-4ab2-8639-c48797d996d1.png)  

If Success but No Recommendation Because of all hotels is been reviewed by the user:  
![image](https://user-images.githubusercontent.com/61568092/169698126-55871840-9cf4-4a9d-ac0d-f01ad12c9d22.png)

IF User IDs not Found:  
![image](https://user-images.githubusercontent.com/61568092/169698039-9f596f8f-895e-48b8-8a6a-3f0c0e123476.png)

## Trending Recommendation API
Trending Recommendation endpoint is based on the number of reviews and its average rating with the formulation of then end score: number of reviews * (average rating * 1.2), the output would be a list of Hotel ID sorted from having the best to the worst score    

| Endpoint                     | Input                      | Output                                                           |
|------------------------------|----------------------------|------------------------------------------------------------------|
| POST `/trending_system/` | - | - | List of Hotel ID sorted from having the best to the worst score

Example:
If Success:  
![image](![Uploading 1222344221123.JPG…]()

## Force Caching API
If you want to force caching in the ML endpoint, just hit this method.
| Endpoint           | Input | Output |
|--------------------|-------|--------|
| POST `/re-cached/` | -     | Text   |

Example:   
![image](https://user-images.githubusercontent.com/58240454/170513139-8e011a8d-4f73-4f97-865c-1f02b00e601a.JPG)

## Check Rows Cached
If you want to check how many rows cached
| Endpoint            | Input | Output     |
|---------------------|-------|------------|
| GET `/rows-cached/` | -     | Dictionary |

Example:  
![image](https://user-images.githubusercontent.com/61568092/169244820-3696ad2a-fb41-4359-806b-2b8c552768d1.png)


# Notes
All system error on ML sides will give you a `500: Internal Server Error` status.


CC22-HO01 ML Teams.
