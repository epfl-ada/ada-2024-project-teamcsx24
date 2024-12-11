import pandas as pd
import ast
import numpy as np
import generalUtils
import sys

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
    df_movies['countries'] = df_movies['countries'].apply(lambda x: ast.literal_eval(x))
    df_movies['countries_freebase_id'] = df_movies['countries_freebase_id'].apply(lambda x: ast.literal_eval(x))
    from generalUtils import transformCountryNameGpd
    df_movies['countries'] = df_movies['countries_freebase_id'].apply(transformCountryNameGpd)

    df_characters = pd.read_csv('data/cleanData/characters_cleaned.csv')
    df_summary = pd.read_csv('data/cleanData/summaries_cleaned.csv')
    df_cluster = pd.read_csv('data/cleanData/character_clusters_cleaned.csv')
    df_us_influence_nlp = process_data_us_influence_nlp()
    
    # Merge DataFrames movies and summaries
    df_movies_merge = pd.merge(df_summary, df_movies, how='inner')

    # Convert country data to a list

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
    country_us_influence_df['Naïve_Influence_score'] = country_us_influence_df['US_Term_Count'] / country_us_influence_df['Number of movies']
    country_us_influence_df['log Number of movies'] = np.log(country_us_influence_df['Number of movies'])

    # Add a 'World_region' column with the geographical region

    country_us_influence_df['World_region'] = country_us_influence_df['Country'].apply(assign_geographical_region)

    country_us_influence_df = pd.merge(country_us_influence_df, df_us_influence_nlp, on='Country', how='inner')

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
    df_first_appearance_tot['number_countries_score'] = df_first_appearance_tot['all_countries'].apply(lambda x: len(x))
    
    return df_first_appearance_tot

def process_data_us_influence_nlp():      #Process the data and return the DataFrame useful for studying the influence of US on other countries.
    
    df_us_influence_nlp = pd.read_csv('data/cleanData/scores.csv')

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
    df_us_influence_nlp['NLP US Influence Score'] = df_us_influence_nlp['Sum_us_score'] / df_us_influence_nlp['Number of movies']
    df_us_influence_nlp.drop(columns=['Number of movies','Sum_us_score'], inplace=True)
    # Return the processed DataFrame
    return df_us_influence_nlp
   

def process_character_nlp():  #Process the data and return the DataFrame useful for studying the influence of countries on each other considering characters (influence get by NLP methods)
    
    # Here, we load the data and we make a few transformations    
    df_movies = pd.read_csv('data/cleanData/movies_cleaned.csv')
    df_characters = pd.read_csv('data/cleanData/characters_cleaned.csv')
    df_summary = pd.read_csv('data/cleanData/summaries_cleaned.csv')  
    df_cluster = pd.read_csv('data/cleanData/character_clusters_cleaned.csv')
    df_character_nlp = pd.read_csv('data/cleanData/character_countries.csv')
    
    # We get a dataframe with the NLP score and best country for each character
    df_character_influence_nlp = pd.merge(process_data_character(), df_character_nlp, on='Character', how='inner')

    # We get another dataframe to get some columns of interest (all the release years of the movies for eg, which will be useful for our analysis)
    df_character_cluster = pd.merge(df_cluster, df_characters, on='character_actor_freebase_id', how='inner')
    
    df_character_influence = pd.merge(df_character_cluster, df_movies, on='wiki_id', how='inner')
    
    df_character_influence['countries'] = df_character_influence['countries'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else x
    )
    
    # We convert the release date to datetime and extract the release year
    df_character_influence['release_date_x'] = pd.to_datetime(df_character_influence['release_date_x'])
    df_character_influence['release_year'] = df_character_influence['release_date_x'].dt.year
    
    # Select the relevant columns
    df_character_influence = df_character_influence[['cluster', 'release_year', 'original_title', 'countries']]
    
    # Merge the two dataframes
    df_character_test = pd.merge(
        df_character_influence_nlp, 
        df_character_influence, 
        left_on='Character', 
        right_on='cluster', 
        how='inner'
    )
    
    # Select the relevant columns
    df_character_test = df_character_test[['original_title', 'Character', 'Best_Country', 'number_countries_score', 'release_year', 'countries']]

    df_character_test = df_character_test.sort_values(by=['Character', 'release_year'])
    
    #Here, we create a function that allows us to track the appearance of characters in different countries

    # Initialize a column for new countries that will contain the cumulate number of counties in which the character appears
    df_character_test['new_countries'] = 0
    
    # Dictionary to track already visited countries by character
    visited_countries = {}
    
    # Iterate over each row to compute new countries
    for idx, row in df_character_test.iterrows():
        character = row['Character']
        countries = set(row['countries'])  
        best_country = row['Best_Country']
        
        # Remove Best_Country from the countries list, we want influence poitn so we don't want to count the influence of a country on itself
        if best_country in countries:
            countries.remove(best_country)     
        
        # Initialize the character in the dictionary if not present
        if character not in visited_countries:
            visited_countries[character] = set()
        
        # Compute the new countries for this character
        new_countries = countries - visited_countries[character]   # Get only the countries in which the character didn't already appeared
        df_character_test.at[idx, 'new_countries'] = len(new_countries)  # Store the count of new countries
        
        # Update the visited countries for this character
        visited_countries[character].update(countries)
    
    return df_character_test

def process_top_characters():      #Process the data and return a dataframe useful to study the most influential characters
    df_character_nlp = pd.read_csv('data/cleanData/character_countries.csv')
    df_character_influence = process_data_character()

    df_top_characters = pd.merge(df_character_influence, df_character_nlp, on='Character', how='inner')
    df_top_characters = df_top_characters[['Character','first_movie_name','Best_Country','number_countries_score','all_countries','first_apperance_date']]
    return df_top_characters


def create_cumulative_df_2(df):     #Create a temporal cumulative DataFrame for the number of new countries in which characters appear, that is the one will use to plot the number of character points of influence over time.
    
    # Create a list of all years from 1910 to 2010
    years = list(range(1910, 2011))

    # Create an empty list to store the new rows for the cumulative DataFrame
    rows = []

    # Loop through each unique country in the 'Best_Country' column
    for country in df['Best_Country'].unique():
        # Filter the data for each country
        country_data = df[df['Best_Country'] == country]
        
        # Initialize a cumulative total to 0
        cumulative_total = 0
        
        # Loop through each year from 1910 to 2010
        for year in years:
            # If the year exists for this country, add the number of new countries produced that year
            if year in country_data['release_year'].values:
                cumulative_total += country_data[country_data['release_year'] == year]['new_countries'].sum()
            
            # Append the row to the list with the year, country, and cumulative total
            rows.append({'release_year': year, 'Best_Country': country, 'tot': cumulative_total})
    
    # Convert the list of rows into a DataFrame
    cumulative_df = pd.DataFrame(rows)
    
    return cumulative_df