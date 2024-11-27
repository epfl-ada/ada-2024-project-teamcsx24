import pandas as pd
import ast
import numpy as np

def count_us_terms(summary):       #Example of US related terms
    us_terms = [
        "America", "United States", "US", "U.S.", "American", "New York",
        "Los Angeles", "California", "Washington D.C.", "Hollywood", 
        "East Coast", "West Coast", "Midwest", "Southern", "American Dream",
        "FBI", "CIA", "White House", "Capitol Hill", "Congress", "President",
        "Independence", "Patriot", "Yankee", "Route 66"
    ]
    
    words = summary.split()
    return sum(1 for word in words if word in us_terms)



def assign_geographical_region(country):         #Geographical clusterisation
     # Europe
    europe = {
        'France', 'Germany', 'Czech Republic', 'United Kingdom', 'Italy', 'Spain', 'Switzerland', 'Belgium',
        'Denmark', 'Bulgaria', 'Ireland', 'Slovakia', 'Norway', 'Sweden', 'Greece', 'Portugal', 'Austria',
        'Poland', 'Hungary', 'Slovenia', 'Croatia', 'Romania', 'Luxembourg', 'Netherlands', 'Estonia',
        'Lithuania', 'Ukraine', 'Latvia', 'Montenegro', 'Albania', 'Serbia', 'Bosnia and Herzegovina',
        'Macedonia', 'Georgia', 'Armenia', 'Moldova', 'Finland', 'Iceland', 'Belarus', 'Malta',
        'Weimar Republic', 'Nazi Germany', 'German Democratic Republic', 'Czechoslovakia', 
        'Kingdom of Great Britain', 'Kingdom of Italy'
    }
    
    # North America
    north_america = {
        'United States of America', 'Canada', 'Mexico', 'Puerto Rico', 'Bahamas', 'Jamaica',
        'Panama', 'Cuba', 'Haiti', 'Bermuda', 'Aruba'
    }
    
    # South America
    south_america = {
        'Brazil', 'Argentina', 'Chile', 'Peru', 'Venezuela', 'Colombia', 'Uruguay', 'Bolivia',
        'Ecuador', 'Paraguay'
    }
    
    # Africa
    africa = {
        'South Africa', 'Morocco', 'Algeria', 'Egypt', 'Nigeria', 'Kenya', 'Zimbabwe', 'Libya',
        'Tunisia', 'Cameroon', 'Senegal', 'Mali', 'Guinea', 'Burkina Faso', 'Ethiopia',
        'Democratic Republic of the Congo', 'Ivory Coast', 'Zambia', 'Angola'
    }
    
    # East and Southeast Asia
    east_asia = {
        'China', 'Japan', 'South Korea', 'North Korea', 'Taiwan', 'Vietnam', 'Thailand', 'Philippines',
        'Indonesia', 'Malaysia', 'Singapore', 'Cambodia', 'Myanmar (Burma)', 'Hong Kong', 'Macau'
    }
    
    # South Asia
    south_asia = {
        'India', 'Pakistan', 'Bangladesh', 'Sri Lanka', 'Nepal', 'Bhutan', 'Maldives'
    }
    
    # Middle East
    middle_east = {
        'Israel', 'Turkey', 'Iran', 'Iraq', 'Saudi Arabia', 'United Arab Emirates', 'Qatar', 'Jordan',
        'Lebanon', 'Kuwait', 'Syria', 'Palestinian territories', 'Mandatory Palestine'
    }
    
    # Eastern Europe and Central Asia
    eastern_europe_central_asia = {
        'Russia', 'Ukraine', 'Kazakhstan', 'Uzbekistan', 'Turkmenistan', 'Georgia', 'Armenia',
        'Azerbaijan', 'Moldova', 'Kyrgyzstan', 'Tajikistan', 'Belarus', 'Soviet Union',
        'Soviet occupation zone', 'Georgian SSR', 'Ukrainian SSR', 'Uzbek SSR'
    }
    
    # Oceania
    oceania = {
        'Australia', 'New Zealand', 'Papua New Guinea', 'Fiji', 'Samoa', 'Tonga'
    }
    
    # Caribbean
    caribbean = {
        'Cuba', 'Jamaica', 'Haiti', 'Dominican Republic', 'Bahamas', 'Barbados'
    }
    
    # Check and assign region
    if country in europe:
        return 'Europe'
    elif country in north_america:
        return 'North America'
    elif country in south_america:
        return 'South America'
    elif country in africa:
        return 'Africa'
    elif country in east_asia:
        return 'East and Southeast Asia'
    elif country in south_asia:
        return 'South Asia'
    elif country in middle_east:
        return 'Middle East'
    elif country in eastern_europe_central_asia:
        return 'Eastern Europe and Central Asia'
    elif country in oceania:
        return 'Oceania'
    elif country in caribbean:
        return 'Caribbean'
    else:
        return 'Other'
    


def process_data_us_influence():            #Process the data and return the DataFrame useful for studying the influence of countries on each other.
    # Charger les données
    df_movies = pd.read_csv('data/cleanData/movies_cleaned.csv')
    df_characters = pd.read_csv('data/cleanData/characters_cleaned.csv')
    df_summary = pd.read_csv('data/cleanData/summaries_cleaned.csv')
    df_cluster = pd.read_csv('data/cleanData/character_clusters_cleaned.csv')
    
    # Merge DataFrames movies and summaries
    df_movies_merge = pd.merge(df_summary, df_movies, how='inner')

    # Convert country data to a list
    df_movies_merge['countries'] = df_movies_merge['countries'].apply(lambda x: ast.literal_eval(x))

    # Create a 'word_list' column containing words from the summary
    df_movies_merge['word_list'] = df_movies_merge['summary'].apply(lambda x: x.split())

    # Add a 'us_terms_count' column with the count of US-related terms found
    df_movies_merge['us_terms_count'] = df_movies_merge['summary'].apply(lambda x: count_us_terms(x))

    # Count the us terms for each country

    country_term_counts = {}

    for index, row in df_movies_merge.iterrows():
        count = row['us_terms_count']
        countries = row['countries']
        for country in countries:
            if country not in country_term_counts:
                country_term_counts[country] = 0
            country_term_counts[country] += count

    country_terms_count_df = pd.DataFrame(list(country_term_counts.items()), columns=['Country', 'US_Term_Count'])

    # Count the number of movies for each country
    country_movie_count = {}

    for index, row in df_movies_merge.iterrows():
        countries = row['countries']
        for country in countries:
            if country not in country_movie_count:
                country_movie_count[country] = 1
            country_movie_count[country] += 1

    country_movie_count_df = pd.DataFrame(list(country_movie_count.items()), columns=['Country', 'Number of movies'])

    # Merge the DataFrames with the number of US terms and the number of movies
    country_us_influence_df = pd.merge(country_terms_count_df, country_movie_count_df)

    # Calculate a ratio of us term and log transformation
    country_us_influence_df['Influence_score'] = country_us_influence_df['US_Term_Count'] / country_us_influence_df['Number of movies']
    country_us_influence_df['log_number_of_movies'] = np.log(country_us_influence_df['Number of movies'])

    # Add a 'World_region' column with the geographical region

    country_us_influence_df['World_region'] = country_us_influence_df['Country'].apply(assign_geographical_region)

    # Return the processed DataFrame
    return country_us_influence_df


def process_data_character():
    # Load the datasets
    df_movies = pd.read_csv('data/cleanData/movies_cleaned.csv')
    df_characters = pd.read_csv('data/cleanData/characters_cleaned.csv')
    df_summary = pd.read_csv('data/cleanData/summaries_cleaned.csv')
    df_cluster = pd.read_csv('data/cleanData/character_clusters_cleaned.csv')
    
    # Merge the DataFrames df_cluster and df_characters on 'character_actor_freebase_id'
    df_character_cluster = pd.merge(df_cluster, df_characters, on='character_actor_freebase_id', how='inner')
    
    # Merge the previous DataFrame with df_movies
    df_character_influence = pd.merge(df_character_cluster, df_movies, on='wiki_id', how='inner')
    
    # Convert the 'countries' column to a list
    df_character_influence['countries'] = df_character_influence['countries'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else x)

    # Sort the data by cluster and release date to get the first appearance of each character
    df_sorted_character = df_character_influence.sort_values(by=['cluster', 'release_date_x'])
    df_first_appearance = df_sorted_character.groupby('cluster').first().reset_index()
    
    # Select the relevant columns
    df_first_appearance = df_first_appearance[['cluster', 'character_actor_freebase_id', 'name', 'original_title', 'release_date_x', 'countries']]
    
    # Extract all the countries where the characters appeared
    all_countries = df_character_influence.groupby('cluster')['countries'].apply(lambda x: list({country for countries_list in x for country in countries_list if isinstance(country, str)})).reset_index()
    
    df_first_appearance_tot = pd.merge(df_first_appearance, all_countries, on='cluster', how='left')

    df_first_appearance_tot.columns = ['Character', 'character_actor_freebase_id', 'actor_name', 'first_movie_name', 'first_apperance_date', 'origin_country', 'all_countries']
    
    # Add a column with the number of countries in which the character appeared
    df_first_appearance_tot['number_countries'] = df_first_appearance_tot['all_countries'].apply(lambda x: len(x))
    
    return df_first_appearance_tot

def process_data_us_influence_nlp():      #Process the score of each country tha twe get from transformers' NLP method and return the DataFrame useful for studying the influence of countries on each other.
    # Charger les données
    df_us_influence_nlp = pd.read_csv('scores.csv')

    df_us_influence_nlp['countries'] = df_us_influence_nlp['countries'].apply(lambda x: ast.literal_eval(x))

    country_sum_score = {}

    for index, row in df_us_influence_nlp.iterrows():
        count = row['score']
        countries = row['countries']
        for country in countries:
            if country not in country_sum_score :
                country_sum_score [country] = 0
            country_sum_score [country] += count

    country_terms_count_df = pd.DataFrame(list(country_sum_score .items()), columns=['Country', 'Sum_us_score'])

    country_movie_count = {}

    for index, row in df_us_influence_nlp.iterrows():
        countries = row['countries']
        for country in countries:
            if country not in country_movie_count:
                country_movie_count[country] = 1
            country_movie_count[country] += 1

    country_movie_count_df = pd.DataFrame(list(country_movie_count.items()), columns=['Country', 'Number of movies'])

    # Merge the DataFrames with the number of US terms and the number of movies
    df_us_influence_nlp = pd.merge(country_terms_count_df, country_movie_count_df)

    # Calculate a ratio of us term and log transformation
    df_us_influence_nlp['nlp_score'] = df_us_influence_nlp['Sum_us_score'] / df_us_influence_nlp['Number of movies']
    # Return the processed DataFrame
    return df_us_influence_nlp
   