from fastapi import FastAPI
import json
import ast

import bz2
import nltk


from recommendation import *
from pydantic import BaseModel

# Create the app
app = FastAPI()

# Create a recommender object to be used in the app
recommender = recommendation()

# Read in the compressed bz2 file
with bz2.BZ2File('df_processed_df.bz2', 'r') as f:
    # read the DataFrame from the compressed file
    df_processed = pd.read_csv(f, compression='bz2')
    

# Define non user-specific variables
d1= df_processed


# Define the request body schema
class PredictionRequest(BaseModel):
    query: str


# Create the home page
@app.get("/")
def read_root():
    return {"Fetch": "Offering Search"}

# Create the search method with user-specific query
@app.post("/recommend/")
def search(request: PredictionRequest):
    results = recommender.offering_search(request.query,d1)

    # Convert the returned DataFrame to a json string
    recommendation_json_str = results.to_json()
    # Convert the json string to a dict
    recommendation_dict = json.loads(recommendation_json_str)
    # Return the recommendation in the response
    return recommendation_dict