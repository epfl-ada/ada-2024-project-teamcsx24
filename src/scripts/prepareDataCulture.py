# Script to prepare the data for the culture analysis (topic and genre)

import sys
import pandas as pd
import os
import json

# Path to add
base_path = os.path.dirname(os.path.abspath(__file__))
utils_path = os.path.join(base_path, '..', 'utils')
sys.path.append(utils_path)

# Load the data
base_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, '..', '..', 'data', 'cleanData', 'movies_cleaned.csv')
df_movies = pd.read_csv(file_path)

# Process the data
df_movies['release_date'] = pd.to_datetime(df_movies['release_date'])

columns_to_convert = ['genres','languages','countries', 'countries_freebase_id', 'languages_freebase_id', 'genres_freebase_id']
df_movies[columns_to_convert] = df_movies[columns_to_convert].applymap(eval)

# ------------------- Prepare the data for the genre analysis -------------------
print('Preparing the data for the genre analysis...')

# Transform the country names
print('Transforming the country names...')

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

df_movies['countries'] = df_movies['countries_freebase_id'].apply(transformCountryNameGpd)

# Explode the genres and countries
print('Exploding the genres and countries...')
df_genres_countries_exploded = df_movies.explode('genres').explode('countries')

# Print number of movies
print('Number of movies before and after dropping movies without countries, release date and genres:')
nb_movies = df_genres_countries_exploded['wiki_id'].nunique()
print(f'Total number of movies: {nb_movies}')

df_genres_countries_exploded.dropna(subset=['countries','release_date','genres'], inplace=True)

nb_movies_after_dropna = df_genres_countries_exploded['wiki_id'].nunique()
print(f'Total number of movies with countries, release date and genres: {nb_movies_after_dropna}')

print(f'Pourcentage of dropped movies: {100*(1-nb_movies_after_dropna/nb_movies):.2f}%')

# Attach the world region to the countries
print('Attaching the world region to the countries...')

def attachWorldRegion(country):
    # Load countries dictionnary
    with open('././data/freebaseIdDictionnaries/regions', 'r') as file:
        countries_regions = json.load(file)
    
    # Convert country to string
    country = str(country)
    
    # Attach a world region to each country
    world_region = countries_regions[country]
    
    return world_region

df_genres_countries_exploded['region'] = df_genres_countries_exploded['countries'].apply(attachWorldRegion)

df_genres_countries_exploded['year'] = pd.to_datetime(df_genres_countries_exploded['release_date']).dt.year

df_genres_countries_exploded.drop(columns=['runtime','revenue','languages','countries_freebase_id','languages_freebase_id','genres_freebase_id'], inplace=True)

# Save the data
df_genres_countries_exploded.to_csv('././data/cultureData/df_genres_countries_exploded.csv', index=False)

# Genre dataframes
df1 = df_genres_countries_exploded.groupby(['region','year','genres']).size().reset_index(name='count')
df2 = df_genres_countries_exploded.groupby(['countries','year','genres']).size().reset_index(name='count')

# Save data
print('Saving the data...')
df1.to_csv('././data/cultureData/df1.csv', index=False)
df2.to_csv('././data/cultureData/df2.csv', index=False)

print('\033[1m' + 'Genre analysis data ready!' + '\033[0m')

# ------------------- Prepare the data for the topic analysis -------------------
print('Preparing the data for the topic analysis...')

df = pd.read_csv('././data/cultureData/topicModelData/summaries_with_topics.csv')
df = df[df['topic'] != -1]

df = df.merge(df_genres_countries_exploded, on='wiki_id')

df = df[['wiki_id','topic_name','release_date','countries','region']]

# Save data
print('Saving the data...')
df.to_csv('././data/cultureData/df_movies_with_topics.csv', index=False)

print('\033[1m' + 'Topic analysis data ready!' + '\033[0m')
