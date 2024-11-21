import pandas as pd

# Function to load dataframes and preprocess the data
def loadDataframe(name, path_to_directory):
    if name == 'movies':
        df = pd.read_csv(path_to_directory + 'movies_cleaned.csv')
        df['release_date'] = pd.to_datetime(df['release_date'])
        
        columns_to_convert = ['genres','languages','countries', 'countries_freebase_id', 'languages_freebase_id', 'genres_freebase_id']
        df[columns_to_convert] = df[columns_to_convert].applymap(eval)

        return df
    
    elif name == 'characters':
        df = pd.read_csv(path_to_directory + 'characters_cleaned.csv')
        
        df['birth_date'] = pd.to_datetime(df['birth_date'])
        df['release_date'] = pd.to_datetime(df['release_date'])
        
        return df
        
    elif name == 'clusters':
        df = pd.read_csv(path_to_directory + 'character_clusters_cleaned.csv')
        return df
    
    elif name == 'summaries':
        df = pd.read_csv(path_to_directory + 'summaries_cleaned.csv')
        return df
    
    else:
        print('Invalid dataframe name')
        return None
    