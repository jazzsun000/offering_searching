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

# Run the API  
  
Note: If you want to skip the preprocessing step a [df_processed_df.bz2](offering_search_API/df_processed_df.bz2) file has been provided. 

## Retrieving offering information
To retrieve recommendations offering information, send a POST request to your_server_name/recommend.  

Detailed instructions on how the offering search is performed can be found by reading the comments in the recommendation.offering_search() class method in the [recommendation_model.py](FastAPI_model/recommendation_model.py#L683) file. 

## Starting the API

1.  Place the [main.py](FastAPI_model/main.py) and [recommendation_model.py](FastAPI_model/recommendation_model.py) files located in the [FastAPI_model](FastAPI_model/) folder in the same directory on your machine along with the __.bz2__ you created earlier in the preprocessing section (this file must be named **processed_offering_search.bz2** for the app to correctly load it).  
  
2.  From the command line, install the [requirements.txt](FastAPI_model/requirements.txt) and launch the local server in your directory FastAPI_model

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
  "query": "string",
  "price": 0,
  "weights": [
    0,0,0,0
  ]
}
```

Request Parameters

**query**: (string) The offering you want to retrieve information for.

**price**: (int) The offering price you want to retrieve, you can only choose from [150, 250, 500, 1000, 2500, 5000, 10000, 15000, 20000, 25000]

**weights**: (list [float]) Represents vector weights [location score weight, search query relevancy score weight, offering feedback rating score weight, provider score weight]

We will use curl and post method to call the API in the documentation, but you can use whatever service you like.

Example request

```console 
curl -X 'POST'   'http://localhost:8000/recommend/'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "query": "I want to see a basketball at Seattle",
  "price": 250,
  "weights": [
    0.6,0.2,0.1,0.1
  ]
}'

```  

 2. Get the corresponding response. 
 
Response Parameters

**Name**: The top 25 offering names we recommend.

**Experience Location**: The corresponding offering location name.

**Category Name**: The corresponding offering category name.

**Bucket Price**: The corresponding offering price we will retrieve, they will range from [150, 250, 500, 1000, 2500, 5000, 10000, 15000, 20000, 25000]

**Subdescription Text**: The corresponding description text of the offering.

**Provider Name Combined**: The corresponding provider name of the offering.

**Rating Score**: The corresponding feedback rating score of the offering.

**Provider Score**: The corresponding provider rating score of the offering.

**Location Score**: The corresponding Location score of the offering.
 
 Location Score Formula:  
 Using median distance of all to minus target distance then divided by median of distance


**Relevancy Score**: The corresponding search query relevancy score of the offering, we built in tfidf model.

**Weighted Score**: The corresponding weight score of offering

Weight score= Location_weight x Location_score +search query relevancy score weight x Relevancy Score + offering feedback rating score weight x Rating Score+ Provider score weight x Provider score

Response Format

If the request is successful, the API will return a JSON object containing top 25 weight score offering information in the following json format:

```console 
{
   "NAME": {
       "2": "Cook Like a Chef",
       "4": "Rock Out at a Concert",
       "8": "Tickets to a NBA Game",
       "1": "Cheer on the Seattle Storm",
       "33": "Marvel at the Theater",
       "40": "Seattle Brewery Tour",
       "38": "All About the Vino",
       "27": "Kick It at a Sounders Game",
       "55": "See Seattle from a Chopper",
       "42": "Ultimate Seattle Skytour",
       "28": "Cheer on the Trailblazers",
       "44": "Food Tour with Friends",
       "59": "Animal Hour",
       "63": "Segway Seattle",
……

```  

Example recommendation response in the terminal
![alt text](https://github.com/blueboard/offering-search/blob/main/sample_response.png)

