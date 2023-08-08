# Dynamic Offer Retrieval Based on Search Queries

## Problem Overview

In the e-commerce space, providing relevant offers to users based on their search intent is paramount. However, this intent can vary widely:

Category-based: Users might search for broad categories such as "diapers".

Brand-focused: Users might have brand preferences, for instance, "Huggies".

Retailer-centric: Users might show loyalty towards certain retailers, for example, "Target".

Our challenge is to devise a system that dynamically gauges user intent based on their search query, filters through a vast database of offers, and delivers the most relevant results. Importantly, transparency is key; we should also reveal the similarity scores which power our recommendations.


# Solution:offering-search API

## Description
This is an offering recommendation system API developed by FastAPI which gives you recommended Fetch Reward offerings based on user input.
  

## Summary
This documentation will show you how to use the API and how we develop it, including:

- Key approachs to the problem
- how to retrieve the data
- how to perform data preprocessing
- how to start the API
- how to send requests 
- required parameters
- recommendation response format

# Approach

We utilize a combination of text processing techniques and similarity computations to retrieve the most pertinent offers:

## 1. Text Preprocessing:

To ensure the accuracy of our similarity calculations, the first step is to standardize the text. This involves:

Stemming: 

Truncating words to their root form to treat words like 'running', 'runner', and 'ran' as the same entity.

TF-IDF Vectorization: 

Transforming text into numerical vectors while emphasizing the importance of terms that are unique to specific documents.

## 2. Similarity Computation:

We employ the cosine similarity metric to measure the similarity between the user's search query and our database of offers. For every category (i.e., offers, brands, and retailers), we compute a similarity score, showcasing how aligned a given offer is to the user's search intent.

## 3. Dynamic Retrieval:
The actual retrieval of offers is done in stages:

a. Direct Matches: 

First, we check for direct matches in categories. If a user searches for a category, brand, or retailer that is directly present in our database, we prioritize those offers.

b. Weighted Averages: 

For a more generic search, we rely on averaged similarity scores across categories. We identify the category with the highest mean similarity score and provide offers from that category.

c. Final Compilation: 

Offers are then sorted based on their similarity scores, ensuring users see the most relevant offers first.

Key Functions:

calculate_similarity: 
Calculates cosine similarity between the user's search query and the provided columns.

top_offers_average: 
Determines the top offers based on direct matches or averaged similarity scores, depending on the nature of the search query.

offering_search: 
This is the primary function that integrates the above components to provide a list of top offers for a given search query, complete with similarity scores.


# Process
  
## Retrieve the data from csv files then get offers data

Introduction
This step consists of reading the data from various CSV files and joining certain DataFrames to get the relevant data pertaining to offers.

Steps


1. Begin by importing the required functions and loading the datasets:.

Load the data from three CSV files: offer_retailer.csv, brand_category.csv, and categories.csv.

```console 
from recommendation import *

offer_retailer_df = pd.read_csv('offer_retailer.csv')
brand_category_df = pd.read_csv('brand_category.csv')
categories_df = pd.read_csv('categories.csv')

```  

2. Join DataFrames:

Now, join the offer_retailer.csv DataFrame with brand_category.csv DataFrame using the 'BRAND' key. The right join ensures that all rows from the brand_category.csv DataFrame are retained and only matching rows from the offer_retailer.csv DataFrame are considered.

```console 
df = pd.merge(offer_retailer_df, brand_category_df, how='right', on='BRAND')

``` 

After executing the above steps, df will hold the merged data based on the 'BRAND' key. 
  
## Data Preprocessing

Before we dive deep into recommendation, it is crucial to preprocess the data to make it suitable for analysis. Below are the steps and methods we employ for data preprocessing:

1.  Fill Missing Offer Data:

In cases where the OFFER column has missing values, we fill in a default message to inform users about the brand's availability, even if there aren't any active offers currently. This ensures that every brand in our database provides valuable feedback to the users.

```console 
df = recommendation.fill_offer_column(df)

``` 

The message format is:
"We currently carry the brand [BRAND_NAME], but we do not have any active offers. Please stay tuned for future updates, as we'll continually strive to bring you exciting deals."


2. Text Preprocessing:

For optimal recommendation performance, the textual data should be standardized. 

This involves a series of steps:

a. Lowercasing: 

All the text is transformed to lowercase to maintain uniformity.

b. Stemming: 

Words are stemmed, which means they are reduced to their root form. This helps in grouping similar words together. For example, 'running', 'runner', and 'ran' will all be reduced to the root 'run'.

c. Handling Missing Values: 

Any NaN values are replaced with empty strings for smoother processing.



### Method Descriptions:

fill_offer_column: 

This method iterates through the OFFER column, and if a value is missing, fills it with the default message mentioned above.

stem_lower_text: 

This method handles the stemming and lowercasing of the text. It uses the PorterStemmer from the nltk library to achieve this. 

preprocess_text: 

This is a comprehensive method that uses the above methods to preprocess specified columns in the dataframe.

## DataFrame Compression for Optimized API Loading

In the evolving world of data science and web services, speed and efficiency play a pivotal role. A primary concern for many APIs is the time taken to read data, especially when the dataset is voluminous. To address this, we present a method to store our preprocessed data in a compressed format, specifically the .bz2 format. This enables faster reads when the API loads the data, optimizing overall performance.

### Compression using bz2

bz2 is a data compression format known for its good compression ratios and fast decompression times. By storing the dataframe in this format, we drastically reduce the time taken to load data when initializing our API, enhancing the user experience.

Import the necessary module and save the preprocessed DataFrame as a compressed bz2 file

```console
import bz2
with bz2.BZ2File('df_processed_df.bz2', 'w') as f:
    df.to_csv(f, index=False, compression='bz2')
``` 

# Run the API using FastAPI
  
Note: If you want to skip the preprocessing step a [df_processed_df.bz2](offering_search_API/df_processed_df.bz2) file has been provided. 

## Retrieving offering information
To retrieve recommendations offering information, send a POST request to your_server_name/recommend.  

Detailed instructions on how the offering search is performed can be found by reading the comments in the recommendation() class method in the [recommendation.py](offering_search_API/recommendation.py) file. 

## Starting the API

1.  Place the [main.py](offering_search_API/main.py) and [recommendation.py](offering_search_API/recommendation.py) files located in the [offering_search_API](offering_search_API/) folder in the same directory on your machine along with the __.bz2__ you created earlier in the preprocessing section (this file must be named **df_processed_df.bz2** for the app to correctly load it).  
  
2.  From the command line, install the [requirements.txt](offering_search_API/requirements.txt) and launch the local server in your directory offering_search_API

Install required libraries

```console 
pip install -r requirements.txt
```  

Launch the API to the local server

```console 
uvicorn main:app --reload
```
![alt text](https://github.com/jazzsun000/offering_searching/blob/main/offering_search_API/server_launched.png)
  
## Using the API  
 1. Send the request to your_server_name/recommend as a json object in the following format:
```json
{
  "query": "string"
}
```

Request Parameters

**query**: (string) The offering you want to retrieve information for.



Launched another terminal under the offering_search_API
folder, we will use curl and post method to call the API in the documentation, but you can use whatever service you like.

Example request

```console 
curl -X 'POST'   'http://localhost:8000/recommend/'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "query": "target"
}'

```  

 2. Get the corresponding response. 
 
Response Parameters

**OFFER**: The top 10 offer description we recommend.

**weight_similarity_score**: The corresponding weight score of offering

Weight score= Offer_weight:0.4 x Offering_similarity_score + (Retailer score weight:0.5 x Retailer score or Brand score weight:0.5 x Brand score or Category score weight:0.5 x Category score) + Receipt_weight:0.1 x Receipt_normalized_score

Response Format

If the request is successful, the API will return a JSON object containing top 25 weight score offering information in the following json format:

```console

{"OFFER":
{"1165":"Dove Hand Wash, select varieties at Target",
"9621":"Dove Hand Wash,select varieties at Target",
"562":"Dove Hand Wash,select varieties at Target",
"183":"Dove Hand Wash,select varieties at Target",
"182":"Dove Hand Wash, select varieties, buy 2 at Target",
"561":"Dove Hand Wash, select varieties, buy 2 at Target",
"9620":"Dove Hand Wash, select varieties, buy 2 at Target",
"1164":"Dove Hand Wash, select varieties, buy 2 at Target",
"985":"L'Oréal Paris Makeup, spend $35 at Target",
"986":"L'Oréal Paris Makeup, spend $30 at Target"},
"weight_similarity_score_retailer":
{"1165":0.661,
"9621":0.661,
"562":0.661,
"183":0.661,
"182":0.653,
"561":0.652,
"9620":0.652,
"1164":0.652,
"985":0.647,
"986":0.645}}
……

```

Result for search query = diapers

```console

{"OFFER":
{"5500":"We currently carry the brand HELLO BELLO, but we do not have any active offers. Please stay tuned for future updates, as we'll continually strive to bring you exciting deals.","4146":"We currently carry the brand LUVS, but we do not have any active offers. Please stay tuned for future updates, as we'll continually strive to bring you exciting deals.","2080":"We currently carry the brand HONEST, but we do not have any active offers. Please stay tuned for future updates, as we'll continually strive to bring you exciting deals.","1731":"We currently carry the brand HUGGIES, but we do not have any active offers. Please stay tuned for future updates, as we'll continually strive to bring you exciting deals.","8338":"We currently carry the brand NEST, but we do not have any active offers. Please stay tuned for future updates, as we'll continually strive to bring you exciting deals.","643":"We currently carry the brand PAMPERS, but we do not have any active offers. Please stay tuned for future updates, as we'll continually strive to bring you exciting deals.","0":"We currently carry the brand CASEYS GEN STORE, but we do not have any active offers. Please stay tuned for future updates, as we'll continually strive to bring you exciting deals.","1":"We currently carry the brand CASEYS GEN STORE, but we do not have any active offers. Please stay tuned for future updates, as we'll continually strive to bring you exciting deals.","2":"We currently carry the brand EQUATE, but we do not have any active offers. Please stay tuned for future updates, as we'll continually strive to bring you exciting deals.","3":"We currently carry the brand PALMOLIVE, but we do not have any active offers. Please stay tuned for future updates, as we'll continually strive to bring you exciting deals."},
"weight_similarity_score_category":
{"5500":0.5,"4146":0.5,"2080":0.5,"1731":0.5,"8338":0.5,"643":0.5,"0":0.1,"1":0.097,"2":0.03,"3":0.018}}
……

```

Result for search query = Huggies

```console

{"OFFER":
{"457":"We currently carry the brand HUGGIES, but we do not have any active offers. Please stay tuned for future updates, as we'll continually strive to bring you exciting deals.","1548":"We currently carry the brand HUGGIES, but we do not have any active offers. Please stay tuned for future updates, as we'll continually strive to bring you exciting deals.","1731":"We currently carry the brand HUGGIES, but we do not have any active offers. Please stay tuned for future updates, as we'll continually strive to bring you exciting deals.","5763":"We currently carry the brand HUGGIES, but we do not have any active offers. Please stay tuned for future updates, as we'll continually strive to bring you exciting deals."},
"weight_similarity_score_brand":
{"457":0.5,"1548":0.5,"1731":0.5,"5763":0.5}}
……

```


