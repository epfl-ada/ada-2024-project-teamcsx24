# Scripts for international career of actors

# importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from itertools import combinations

# importing df
data_folder = '../../data/cleanData/'
df_characters = pd.read_csv(data_folder + 'characters_cleaned.csv')
df_movies = movies_df = pd.read_csv(data_folder + 'movies_cleaned.csv')


#function that counts the number of countries associated with a single movie
def numberMovieCount(countries):
    list_countries = countries.split(',')
    return len(list_countries)


# Creating df containing only the single prods
merged_df = pd.merge(df_characters, df_movies[['freebase_id','countries_freebase_id']], on='freebase_id')
#removing the movies in which there is no actor ID
merged_df = merged_df.dropna(subset=('actor_freebase_id', 'countries_freebase_id'))
# removing the countries that have '[]' as id
merged_df = merged_df[merged_df['countries_freebase_id'] != '[]']
#creating a column in the df that contains the number of production countries
merged_df['number_production_countries'] = merged_df['countries_freebase_id'].apply(numberMovieCount)
single_prod_df = merged_df[merged_df['number_production_countries'] == 1]

def createSingleProdDf() :
    return single_prod_df


# function to plot the number of countries per actor
single_prod_grouped = single_prod_df.groupby(single_prod_df.actor_freebase_id)
number_countries_per_actor = single_prod_grouped['countries_freebase_id'].nunique()
def numberCountriesPerActor():
    # for each actor, counts the number of different countries in which they played
    return number_countries_per_actor 


# comparisons between single and co prod
def comparisonSingleCoProd():
    single_prod = single_prod_df['countries_freebase_id'].nunique()
    total_movies = merged_df['countries_freebase_id'].nunique()
    return ((f'Number of single-production movies : {single_prod}'), (f'Total number of movies : {total_movies}'))

def comparisonActors() :
    single_prod = single_prod_df['actor_freebase_id'].nunique()
    total_movies = merged_df['actor_freebase_id'].nunique()
    return ((f'Number of actors single production : {single_prod}'), (f'Total number of actors : {total_movies}'))

# create international actor dataframe
international_actors = number_countries_per_actor[number_countries_per_actor > 1]
international_actors_df = pd.merge(single_prod_df, international_actors, on = 'actor_freebase_id')
def createInternationalActorDf() :
    return international_actors_df

# number of nodes
def numberCountries():
    number_countries = international_actors_df['countries_freebase_id_x'].nunique()
    number_countries_total = merged_df['countries_freebase_id'].nunique()
    return (f'{number_countries} countries will be represented in our graph, {number_countries_total} were initially present in the data')


# graph

# Creating a graph and adding one node for each country
G = nx.Graph()
G.add_nodes_from(international_actors_df['countries_freebase_id_x'].unique())

#associating each actor with the countries they played in
international_actors_df_grouped = international_actors_df.groupby(international_actors_df.actor_freebase_id)
countries_for_actor = international_actors_df_grouped['countries_freebase_id_x'].unique()

# Creating a function that create edges between countries in which an actor played
def createEdges(actor) :
    countries = countries_for_actor[actor]
    #countries_cleaned = [(country.strip("[]'\"")) for country in countries]
    #creates a list with all possible pairs of countries
    pairs = tuple(combinations(countries, 2))
    return pairs

# Adding the edges to the graph
for actor in international_actors_df['actor_freebase_id'].unique() :
    edge = createEdges(actor)
    G.add_edges_from(edge)
G.number_of_edges()

def getGraph():
    return G


# ethnicity

#dataframe and statistics

characters_modified = df_characters.dropna(subset=('ethnicity_freebase_id', 'release_date'))

def getReleaseYear(release_date):
    date = pd.to_datetime(release_date, format = "%Y-%m-%d")
    return date.year

characters_modified['release_year'] = characters_modified['release_date'].apply(getReleaseYear)

def createEthicitiesDf():
    return characters_modified

#computing the average number of ethnicities in movie per year
characters_grouped = characters_modified.groupby(['release_year', 'freebase_id'])

number_ethnicities = pd.DataFrame(characters_grouped['ethnicity_freebase_id'].nunique())
number_ethnicities.reset_index(inplace=True)

number_ethnicities_grouped = number_ethnicities.groupby(number_ethnicities.release_year)
average_ethnicity_per_year = number_ethnicities_grouped['ethnicity_freebase_id'].mean()

def averageEthnicityPerYear():
    return average_ethnicity_per_year

