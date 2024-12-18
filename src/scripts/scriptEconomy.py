import pandas as pd
import ast
import numpy as np
from itertools import combinations
import json

# Function to transform countries names to geopandas names using the freebase id

def transformCountryNameGpd(countries_freebase_id):
    # Load countries dictionnary
    with open('././data/freebaseIdDictionnaries/countries_geo', 'r') as file:
        countries_dict = json.load(file)
    
    # Transform countries names to geopandas names using the freebase id
    countries_name = []
    n = len(countries_freebase_id)
    for i in range(n):
        country_freebase_id = countries_freebase_id[i]
        country_name = countries_dict[country_freebase_id]
        countries_name.append(country_name)
    
    return countries_name


# Function to process the data related to the economy part
def process_data_economy():

    # -- Load the data -- #

    df_movies = pd.read_csv('./data/cleanData/movies_cleaned.csv') # Load the movies dataset cleaned

    df_inflation_additional_annual = pd.read_csv('./data/cleanData/Kaggle_US_CPI_annual_cleaned.csv')

    # -- Process the data -- #

    df_movies = df_movies[["wiki_id", "freebase_id", "original_title", "release_date", "revenue", "countries", "countries_freebase_id"]] # Keep only the relevant columns for the Economy part

    columns_to_convert = ['countries', 'countries_freebase_id']
    
    df_movies[columns_to_convert] = df_movies[columns_to_convert].applymap(eval) # Convert the columns with list of strings to list of strings

    df_movies['release_date'] = pd.to_datetime(df_movies['release_date']) # Convert the 'release_date' column to datetime format

    # -- Filter the data for Economy part -- #

    df_movies_eco = df_movies[df_movies['revenue'].notna()] # Drop the rows with missing values in the 'revenue' column

    df_movies_eco['year'] = df_movies_eco['release_date'].dt.year # Extract the year from the 'release_date' column

    df_movies_eco = df_movies_eco.dropna(subset=['year']) # Drop the rows with missing values in the 'year' column

    df_movies_eco = df_movies_eco[df_movies_eco['year'] != 1897] # Drop the rows with the year 1897

    df_movies_eco['countries'] = df_movies_eco['countries_freebase_id'].apply(transformCountryNameGpd) # we transform countries names to geopandas names using the freebase id

    # -- New features -- #

    reference_year = 1963 # Reference year for the inflation adjustment

    cpi_reference = df_inflation_additional_annual[df_inflation_additional_annual['year'] == reference_year]['CPI'].values[0] # CPI value for the reference year

    df_movies_eco['revenue_adj'] = df_movies_eco.apply(lambda x: x['revenue'] * cpi_reference / df_inflation_additional_annual[df_inflation_additional_annual['year'] == x['year']]['CPI'].values[0], axis=1) # Adjust the revenue for inflation

    # -- Return processed data -- #

    return df_movies_eco

# Function to attach a world region to each country

def attachWorldRegion(country):
    # Load countries dictionnary
    with open('././data/freebaseIdDictionnaries/regions', 'r') as file:
        countries_regions = json.load(file)
    
    # Convert country to string
    country = str(country)
    
    # Attach a world region to each country
    world_region = countries_regions[country]
    
    return world_region


# Function to explode on countries and process the data related to the economy part
def process_data_exploded_economy():

    df_movies_eco = process_data_economy() # Process the data related to the economy part

    # -- Explode on countries -- #

    df_movies_eco_exploded_countries = df_movies_eco.explode('countries') # we create duplicates of the rows with multiple production countries

    # -- Process the data -- #

    df_movies_eco_exploded_countries = df_movies_eco_exploded_countries[df_movies_eco_exploded_countries['countries'].notna()] # we remove the rows with no countries

    # -- New features -- #

    df_movies_eco_exploded_countries['region'] = df_movies_eco_exploded_countries['countries'].apply(attachWorldRegion) # we attach a world region to each country

    # -- Return processed data -- #
    
    return df_movies_eco_exploded_countries

# Function to create a dataframe with the market share of each country

def calculate_market_share_economy():

    df_movies_eco_exploded_countries = process_data_exploded_economy() # Process the data related to the economy part

    # -- Calculate the market share of each country -- #

    df_movies_eco_exploded_countries_agg = df_movies_eco_exploded_countries.groupby(["year", "countries"])["revenue"].sum().reset_index() # Group by Year and Country, sum revenue

    df_movies_eco_exploded_countries_agg["total_revenue_year"] = df_movies_eco_exploded_countries_agg.groupby("year")["revenue"].transform("sum") # Calculate total revenue per year

    df_movies_eco_exploded_countries_agg["market_share"] = df_movies_eco_exploded_countries_agg["revenue"] / df_movies_eco_exploded_countries_agg["total_revenue_year"] *100  # Calculate market share as a percentage

    df_movies_eco_exploded_countries_agg['log_revenue'] = df_movies_eco_exploded_countries_agg["revenue"].apply(lambda x: np.log(x)) # Calculate the log of the revenue

    df_movies_eco_exploded_countries_agg["log_market_share"] = df_movies_eco_exploded_countries_agg["market_share"].apply(lambda x: np.log(x)) # Calculate the log of the percentage of market share

    df_movies_eco_exploded_countries_agg['year'] = df_movies_eco_exploded_countries_agg['year'].astype(int)


    # -- Return processed data -- #
    
    return df_movies_eco_exploded_countries_agg

# Function to create a dataframe with the co-productions movies

def movies_co_productions():

    df_movies_eco_exploded_countries = process_data_exploded_economy() # Process the data related to the economy part

    # -- Process the data -- #

    df_movies_eco_coprod = df_movies_eco_exploded_countries.groupby(["wiki_id"])["countries"].count().reset_index() # Count the number of countries for each movie

    df_movies_eco_coprod = df_movies_eco_coprod[df_movies_eco_coprod["countries"] > 1] # Keep only the movies with more than 1 country

    # -- Filter the data for co-productions movies -- #

    df_movies_eco_exploded_countries_coprod = df_movies_eco_exploded_countries[df_movies_eco_exploded_countries["wiki_id"].isin(df_movies_eco_coprod["wiki_id"])] # Keep only the rows with movies with more than 1 country

    # -- Return processed data -- #

    return df_movies_eco_exploded_countries_coprod

# Function to create a dataframe with the number of co-productions yearly per country

def coprod_countries_yearly():

    df_movies_eco_exploded_countries_coprod = movies_co_productions() # Create a dataframe with the co-productions movies

    df_movies_eco_coprod_countries_count = (df_movies_eco_exploded_countries_coprod.groupby(["year", "countries"])["wiki_id"].nunique().reset_index(name="co_production_count")) # Count the number of co-productions movies per year and per country
    
    df_movies_eco_coprod_countries_count['year'] = df_movies_eco_coprod_countries_count['year'].astype(int) # Convert the 'year' column to integer format

    # -- Return processed data -- #

    return df_movies_eco_coprod_countries_count

# Function to generate all the combinations of countries per movies

def generate_country_combinations(row):
        return pd.DataFrame(list(combinations(sorted(row["countries"]), 2)), columns=["country_1", "country_2"]).assign(year=row["year"])

#Function to create a dataframe with couple of countries and the number of co-productions between them yearly

def coprod_couple_countries_yearly():

    df_movies_eco_exploded_countries_coprod = movies_co_productions() # Create a dataframe with the co-productions movies

    # -- Step 1 : Group countries and co-productions per movies and years -- #
    
    df_movies_eco_coprod_countries = df_movies_eco_exploded_countries_coprod.groupby(["wiki_id", "year"])["countries"].apply(list).reset_index() # Group countries per movies and years

    # -- Step 2 : Generate all the combinations of countries per movies -- #
    
    combinations_df = pd.concat([generate_country_combinations(row) for _, row in df_movies_eco_coprod_countries.iterrows()], ignore_index=True) # Generate all the combinations of countries per movies

    # -- Step 3 : Count the co-productions per year and per couple of countries -- #
    df_movies_eco_coprod_country_country = (combinations_df.groupby(["year", "country_1", "country_2"]).size().reset_index(name="co_production_count")) # Count the number of co-productions per year and per couple of countries

    df_movies_eco_coprod_country_country['year'] = df_movies_eco_coprod_country_country['year'].astype(int) # Convert the 'year' column to integer format

    # -- Return processed data -- #
    
    return df_movies_eco_coprod_country_country


#Function to create a dataframe with couple of countries and the number of co-productions between them per period of 10 years

def coprod_couple_countries_period():

    df_movies_eco_coprod_country_country = coprod_couple_countries_yearly() # Create a dataframe with couple of countries and the number of co-productions between them yearly
    
    df_movies_eco_coprod_country_country_10 = df_movies_eco_coprod_country_country # Copy the dataframe

    # -- Process the data -- #

    df_movies_eco_coprod_country_country_10["period"] = (df_movies_eco_coprod_country_country_10["year"] // 10) * 10 # Add the period of 10 years

    df_movies_eco_coprod_country_country_10 = df_movies_eco_coprod_country_country_10.groupby(["period", "country_1", "country_2"])["co_production_count"].sum().reset_index() # Count the number of co-productions per period of 10 years and per couple of countries

    # -- Return processed data -- #

    return df_movies_eco_coprod_country_country_10    

#Function to create a dataframe with the revenue of movies per period of 10 years

def revenue_period():

    df_movies_eco_exploded_countries = process_data_exploded_economy() # Process the data related to the economy part

    # -- Process the data -- #

    # Create period based on 10-year intervals
    df_movies_eco_exploded_countries['period'] = (df_movies_eco_exploded_countries['year'] // 10) * 10 # Add the period of 10 years

    # Group by Year and Country, sum revenue
    df_movies_eco_exploded_countries_agg_10 = df_movies_eco_exploded_countries.groupby(["period", "countries"])["revenue"].sum().reset_index() # Group by period and country, sum revenue

    # Calculate log of revenue over the period
    df_movies_eco_exploded_countries_agg_10['log_revenue_period'] = df_movies_eco_exploded_countries_agg_10["revenue"].apply(lambda x: np.log(x) if x > 0 else 0) # Calculate the log of the revenue

    # Convert year to integer
    df_movies_eco_exploded_countries_agg_10['period'] = df_movies_eco_exploded_countries_agg_10['period'].astype(int)

    # -- Data Cleaning for the plot -- #

    df_movies_eco_exploded_countries_agg_10 = df_movies_eco_exploded_countries_agg_10[df_movies_eco_exploded_countries_agg_10.countries != "Republic of Serbia"]

    df_movies_eco_exploded_countries_agg_10 = df_movies_eco_exploded_countries_agg_10[df_movies_eco_exploded_countries_agg_10.countries != "The Bahamas"]

    df_movies_eco_exploded_countries_agg_10 = df_movies_eco_exploded_countries_agg_10[df_movies_eco_exploded_countries_agg_10.countries != "Bosnia and Herzegovina"]

    # -- Return processed data -- #

    return df_movies_eco_exploded_countries_agg_10