from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import bz2

# Set the option to display maximum columns and maximum column width
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)


class recommendation:
    def __init__(self):
        """ """

    def fill_offer_column(self,df):
        df['OFFER'] = df.apply(
            lambda row: "We currently carry the brand {}, but we do not have any active offers. Please stay tuned for future updates, as we'll continually strive to bring you exciting deals.".format(row['BRAND'])
            if pd.isnull(row['OFFER']) else row['OFFER'],
            axis=1
        )
        return df
    
    def get_weight_score(self,df):

        # Define the text you want to match
        no_offer_text = "We currently carry the brand {}, but we do not have any active offers. Please stay tuned for future updates, as we'll continually strive to bring you exciting deals."

        # Set the 'OFFER_similarity' to 0 if the 'OFFER' column contains the specified text
        df['OFFER_similarity'] = df.apply(
            lambda row: 0 if no_offer_text.format(row['BRAND']) in row['OFFER'] else row['OFFER_similarity'],
            axis=1
        )

        # Normalize the receipt data
        df['normalized_receipts'] = df['RECEIPTS'] / df['RECEIPTS'].max()

        # Calculate the receipt score
        df['receipt_score'] = df['normalized_receipts']

        # Calculate the weight similarity score
        df['weight_similarity_score_retailer']= (df['OFFER_similarity']*0.4+df['RETAILER_similarity']*0.5+df['receipt_score']*0.1).round(3)
        df['weight_similarity_score_brand']= (df['OFFER_similarity']*0.4+df['BRAND_similarity']*0.5+df['receipt_score']*0.1).round(3)
        df['weight_similarity_score_category']= (df['OFFER_similarity']*0.4+df['BRAND_BELONGS_TO_CATEGORY_similarity']*0.5+df['receipt_score']*0.1).round(3)
    
        return df


    def stem_lower_text(self, df, column):
        stemmer = PorterStemmer()
        df[column + '_stemmed'] = df[column].apply(lambda x: str(x).lower() if pd.notnull(x) else '')
        df[column + '_stemmed'] = df[column + '_stemmed'].apply(lambda x: ' '.join([stemmer.stem(word) for word in str(x).split()]))
        return df

    def preprocess_text(self, df, columns):
        for column in columns:
            df[column].fillna("", inplace=True)  # replace nan values with empty strings
            df = self.stem_lower_text(df, column)
        return df

    def stem_query(self, query):
        stemmer = PorterStemmer()
        stemmed_query = ' '.join([stemmer.stem(word) for word in query.lower().split()])
        return stemmed_query

    def calculate_similarity(self, df, search_query, columns):
        # Stem the search_query
        search_query = self.stem_query(search_query)
    
        # Initialize a TF-IDF Vectorizer
        tfidf_vectorizer = TfidfVectorizer()

        # For each specified column
        for column in columns:
            # Fit and transform the dataframe column to a TF-IDF matrix
            tfidf_matrix = tfidf_vectorizer.fit_transform(df[column + '_stemmed'])

            # Transform the search query to its TF-IDF representation
            search_vector = tfidf_vectorizer.transform([search_query])

            # Calculate cosine similarity between the search term and each item in the dataframe
            df[column + '_similarity'] = cosine_similarity(search_vector, tfidf_matrix).flatten()

        return df



    
    
    def top_offers_average(self,df, search_query,n=10):
    
        # Check if search query matches with 'BRAND_BELONGS_TO_CATEGORY'
        match_category = df[df['BRAND_BELONGS_TO_CATEGORY'].str.contains(search_query, na=False, case=False)]
        if not match_category.empty:
            sorted_top_category_offers = match_category.sort_values(by='weight_similarity_score_category' , ascending=False).head(n)
            return sorted_top_category_offers[['OFFER','weight_similarity_score_category']]
    
        # Check if search query matches with 'RETAILER'
        match_retailer = df[df['RETAILER'].str.contains(search_query, na=False, case=False)]
        if not match_retailer.empty:
            sorted_top_retailer_offers = match_retailer.sort_values(by='weight_similarity_score_retailer' , ascending=False).head(n)
            return sorted_top_retailer_offers[['OFFER', 'weight_similarity_score_retailer']]
    
        # Check if search query matches with 'BRAND'
        match_brand = df[df['BRAND'].str.contains(search_query, na=False, case=False)]
        if not match_brand.empty:
            # match_brand.loc[:, 'weight_similarity_score_brand'] = 1 # Setting similarity score to 1
            sorted_top_brand_offers = match_brand.sort_values(by='weight_similarity_score_brand' , ascending=False).head(n)
            return sorted_top_brand_offers[['OFFER', 'weight_similarity_score_brand']]

        # Sort the DataFrame by weight_similarity_score for each category and take the top 10
        top_retailer_offers = df.sort_values(by='weight_similarity_score_retailer', ascending=False).head(10)
        top_brand_offers = df.sort_values(by='weight_similarity_score_brand', ascending=False).head(10)
        top_category_offers = df.sort_values(by='weight_similarity_score_category', ascending=False).head(10)

        # Calculate the mean weight_similarity_score for the top 10 offers in each category
        retailer_avg = top_retailer_offers['weight_similarity_score_retailer'].mean()
        brand_avg = top_brand_offers['weight_similarity_score_brand'].mean()
        category_avg = top_category_offers['weight_similarity_score_category'].mean()

        # Combine the averages into a single DataFrame
        averages = {
            'retailer': retailer_avg,
            'brand': brand_avg,
            'category': category_avg
        }

        # Get the category with the highest average
        max_category = max(averages, key=averages.get)

        # Get the corresponding offers and final similarity score
        if max_category == 'retailer':
            top_offers = top_retailer_offers
            final_score = retailer_avg
        elif max_category == 'brand':
            top_offers = top_brand_offers
            final_score = brand_avg
        else:
            top_offers = top_category_offers
            final_score = category_avg
    
        # Sort by the 'weight_similarity_score_' column of the max category and get the top n offers
        sorted_top_offers = top_offers.sort_values(by='weight_similarity_score_' + max_category, ascending=False).head(n)


        # Return the top offers and the final similarity score
        return sorted_top_offers[['OFFER', 'weight_similarity_score_' + max_category]]

    def offering_search(self, search_query, df):
        columns = ['OFFER', 'RETAILER', 'BRAND', 'BRAND_BELONGS_TO_CATEGORY']
        
        df.fillna("", inplace=True)  # replacing nan values with empty strings
        
        df = self.calculate_similarity(df, search_query, columns)
        
        df = self.get_weight_score(df)
        
        final_df=self.top_offers_average(df, search_query)
        
        return final_df
