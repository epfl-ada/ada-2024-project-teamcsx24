# Scripts for international career of actors

# importing libraries
import pandas as pd
import plotly.graph_objects as go
from importlib import reload
import sys
from itertools import combinations
import json
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# Paths to add
paths = ['./src/data']
for path in paths:
    sys.path.append(path)
    
# Data loader
from dataLoader import loadDataframe


# ethnicity


#Preparing the dataframe

# loading the dictionnaries
with open('./data/freebaseIdDictionnaries/ethnicities', 'r') as file:
        ethnicities_dict = json.load(file)

with open('./data/freebaseIdDictionnaries/ethnicity_to_country', 'r') as file:
        ethnicities_to_country = json.load(file)

# functions
def getEthnicity(id):
    try :
        return ethnicities_dict[id]
    except :
        return None

def getReleaseYear(release_date): 
    date = pd.to_datetime(release_date, format = "%Y-%m-%d")
    return date.year

def getCountry(ethnicity):
    try :
        return  ethnicities_to_country[ethnicity]
        
    except :
        return ethnicity


def createEthicitiesDf():
    df_ethnicities = loadDataframe('characters', path_to_directory)
    df_ethnicities = df_ethnicities.dropna(subset=('ethnicity_freebase_id', 'release_date'))
    df_ethnicities['release_year'] = df_ethnicities['release_date'].apply(getReleaseYear)

    #translate the ethnicity-id into names using the dictionnary
    df_ethnicities['ethnicity_name'] = df_ethnicities['ethnicity_freebase_id'].apply(lambda x: getEthnicity(x))
    df_ethnicities = df_ethnicities.dropna(subset='ethnicity_name')
    df_ethnicities['ethnicity_name'] = df_ethnicities['ethnicity_name'].astype(str).apply(lambda x: x.strip("['']"))

    #associating each ethnicity with a country
    df_ethnicities['actor_country'] = df_ethnicities['ethnicity_name'].apply(lambda x: getCountry(x))
    df_ethnicities = df_ethnicities[df_ethnicities['actor_country'] != 'Unknown']

    #selecting the appropriate years
    df_ethnicities = df_ethnicities[(df_ethnicities['release_year'] > 1908)&(df_ethnicities['release_year'] <=2010)]
    return df_ethnicities








#plotting the repartition of ethnicities in the df
def plotEthnicityRepartition(df):
    ethnicity_representation = df['ethnicity_name'].value_counts()[:100]
    fig = px.bar(x= ethnicity_representation.index, y=ethnicity_representation.values)
    fig.update_xaxes(showticklabels=False)
    fig.update_layout(title_text='Repartition of the ethnicities',title_x=0.5, showlegend=False, legend_title=None, xaxis_title = 'ethnicity', yaxis_title = 'count')
    fig.show()

#plotting the repartition of actor's country in the df
def plotCountryRepartition(df):
    country_representation = df['actor_country'].value_counts()[:100]
    fig = px.bar(x= country_representation.index, y=country_representation.values)
    fig.update_xaxes(showticklabels=False)
    fig.update_layout(title_text="Repartition of the actors' countries",title_x=0.5, showlegend=False, legend_title=None, xaxis_title = 'country', yaxis_title = 'count')
    fig.show()
 





# plotting the stacked barchart

def createMainEthnicitiesDf(df):
#There still are too many categories : we will also keep the 15 major ones
# list of the 15 most represented ethnicities
    list_main_ethnicities = df['actor_country'].value_counts()[:15].index

    # selecting the most represented ethnicities
    main_ethnicities = df[df['actor_country'].isin(list_main_ethnicities)]

    #Adding a row representing all the other ethnicities grouped together
    other_df = df[~df['actor_country'].isin(list_main_ethnicities)]
    other_df['actor_country'] = 'others'
    main_ethnicities = pd.concat([main_ethnicities, other_df])

    # Normalizing the data
    main_ethnicities_grouped = main_ethnicities.groupby(['release_year', 'actor_country']).size().reset_index(name='count')
    main_ethnicities_grouped['proportion'] = main_ethnicities_grouped.groupby('release_year')['count'].transform(lambda x: x / x.sum())

    return main_ethnicities_grouped

#plotting the normalized graph
def plotNormalizedGraph(df):
    custom_colors = px.colors.qualitative.Light24

    fig_normalized = px.histogram(
        df,
        x='release_year',
        y='proportion',
        color='actor_country',
        barmode='stack',
        title='Proportion of Ethnicities per Year',
        labels={'release_year': 'Year', 'proportion': 'Proportion'},
        nbins=220,
        color_discrete_sequence=custom_colors
    )

    fig_normalized.update_layout(
        xaxis=dict(title="Year", dtick=5),  # Set tick interval to 1 year
        yaxis=dict(title="Proportion"),
        template="plotly_white",
        legend_title_text="Ethnicity",
    )

    fig_normalized.update_traces(xbins=dict( # bins used for histogram
            size=0.5
        ))
    return fig_normalized


# plotting non-normalized version
def plotOriginalGraph(df):
    custom_colors = px.colors.qualitative.Light24
    fig_original = px.histogram(
        df,
        x='release_year',
        y='count',
        color='actor_country',
        barmode='stack',
        title='Proportion of Ethnicities per Year',
        labels={'release_year': 'Year', 'count': 'Count'},
        nbins=220,
        color_discrete_sequence=custom_colors
    )

    fig_original.update_layout(
        xaxis=dict(title="Year", dtick=5),  # Set tick interval to 1 year
        yaxis=dict(title="Count"),
        template="plotly_white",
        legend_title_text="Ethnicity",
        width = 1000,
        height = 600,
    )

    fig_original.update_traces(xbins=dict( # bins used for histogram
            size=0.5
        ))
    return fig_original





# average nb of ethnicities per movie
def averageEthnicityPerYear(df):
    characters_grouped = df.groupby(['release_year', 'freebase_id'])
    number_ethnicities = pd.DataFrame(characters_grouped['ethnicity_freebase_id'].nunique())
    number_ethnicities.reset_index(inplace=True)
    number_ethnicities_grouped = number_ethnicities.groupby(number_ethnicities.release_year)
    average_ethnicity_per_year = number_ethnicities_grouped['ethnicity_freebase_id'].mean()
    deviation = number_ethnicities_grouped['ethnicity_freebase_id'].std()
    years = average_ethnicity_per_year.index
    values = average_ethnicity_per_year.values
    errors = deviation  

    
    fig = go.Figure()

    
    fig.add_trace(go.Scatter(
        x=years,
        y=values,
        error_y=dict(
            type='data',   
            array=errors,  
            color='lightskyblue'  
        ),
        mode='lines+markers',
        line=dict(color='royalblue'),
        name='Average number of ethnicities'
    ))

   
    fig.update_layout(
        title="Evolution of the number of ethnicities per movie",
        xaxis_title="Years",
        yaxis_title="Average number of ethnicities",
        width=700, 
        height=400,  
    )
    return fig











# map of international actors


#creating the dataframe

#function that counts the number of countries associated with a single movie
def numberMovieCount(countries):
    list_countries = countries.split(',')
    return len(list_countries)


def createInternationalActorDf() :
    # Load data
    path_to_directory = './data/cleanData/'
    df_movies = loadDataframe('movies', path_to_directory)
    df_characters = loadDataframe('characters', path_to_directory)
    merged_df = pd.merge(df_characters, df_movies[['freebase_id','countries_freebase_id']], on='freebase_id')

    #removing the movies in which there is no actor ID
    merged_df = merged_df.dropna(subset=('actor_freebase_id', 'countries_freebase_id', 'release_date'))

    # removing the countries that have '[]' as id
    merged_df['countries_freebase_id'] = merged_df['countries_freebase_id'].astype(str)
    merged_df = merged_df[merged_df['countries_freebase_id'] != '[]']

    #creating a column in the df that contains the number of production countries
    merged_df['number_production_countries'] = merged_df['countries_freebase_id'].apply(numberMovieCount)
    single_prod_df = merged_df[merged_df['number_production_countries'] == 1]

    single_prod_grouped = single_prod_df.groupby(single_prod_df.actor_freebase_id)
    number_countries_per_actor = single_prod_grouped['countries_freebase_id'].nunique()
    international_actors = number_countries_per_actor[number_countries_per_actor > 1]
    international_actors_df = pd.merge(single_prod_df, international_actors, on='actor_freebase_id')
    international_actors_df = international_actors_df.drop('countries_freebase_id_y', axis=1)
    # creating a line with the release year
    international_actors_df['release_year'] = international_actors_df['release_date'].apply(getReleaseYear) 
    return international_actors_df
  
   

#function that returns a dataframe of pairs for all countries in which the actor played 
def createLinks(actor) :
    countries = countries_for_actor[actor]
    #creates a list with all possible pairs of countries
    pairs = list(combinations(countries, 2))
    return pd.DataFrame(pairs)


#modifying the function createLinks so that it returns the id of the actor as well 
def createLinksYear(actor, df) :
    countries = df[actor]
    #creates a list with all possible pairs of countries
    pairs = list(combinations(countries, 2))
    pairs = pd.DataFrame(pairs)
    pairs['actor'] = actor
    return pairs

#creating a function that takes an actor and a country and 
#gives the earliest date in which the actor played in this country

def findEarliestDate(actor, country, df) : 
    new_df = df[(df['actor_freebase_id'] == actor) & (df['countries_freebase_id_x'] == country)]
    if new_df.empty:
        return None
    years = new_df['release_year'].unique()
    earliest_date = min(years)
    return earliest_date


def createLinkDf(df):
    df_links = pd.DataFrame({
    'country1': [],
    'country2': [],
    'actor': []
    })
    #associating each actor with the countries they played in
    international_actors_df_grouped = df.groupby(df.actor_freebase_id)
    countries_for_actor = international_actors_df_grouped['countries_freebase_id_x'].unique()
    for actor in df['actor_freebase_id'].unique() :
        df_actor = createLinksYear(actor, countries_for_actor)
        df_actor.columns = ('country1', 'country2', 'actor')
        df_links = pd.concat([df_links, df_actor])
    return df_links

