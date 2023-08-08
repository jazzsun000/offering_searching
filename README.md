# offering-search API

## Description
This is an offering recommendation system API developed by FastAPI which gives you recommended Fetch Reward offerings based on user input.
  

## Summary
This documentation will show you how to use the API and how we develop it, including:
- how to retrieve the data
- how to perform data preprocessing
- how to start the API
- how to send requests 
- required parameters
- recommendation response format
- How we develop the API



# Initialization 
  
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
  
## Using the API  
 1. Send the request to your_server_name/recommend as a json object in the following format:
```json
{
  "query": "string"
}
```

Request Parameters

**query**: (string) The offering you want to retrieve information for.



We will use curl and post method to call the API in the documentation, but you can use whatever service you like.

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

{"OFFER":{"1165":"Dove Hand Wash, select varieties at Target",
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
{"1165":0.661,"9621":0.661,"562":0.661,
"183":0.661,"182":0.653,"561":0.652,"9620":0.652,
"1164":0.652,"985":0.647,"986":0.645}}
……

```  

Example recommendation response in the terminal
![alt text](https://github.com/blueboard/offering-search/blob/main/sample_response.png)

