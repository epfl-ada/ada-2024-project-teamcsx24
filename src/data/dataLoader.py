import pandas as pd

# Function to load dataframes and preprocess the data
def loadDataframe(name=('movies','characters','clusters','summaries')):
    if name == 'movies':
        df = pd.read_csv('data/cleanData/movies_cleaned.csv')
        df['release_date'] = pd.to_datetime(df['release_date'])
        
        columns_to_convert = ['genres','languages','countries']
        df[columns_to_convert] = df[columns_to_convert].applymap(eval)

        return df
    
    elif name == 'characters':
        df = pd.read_csv('data/cleanData/characters_cleaned.csv')
        
        df['birth_date'] = pd.to_datetime(df['birth_date'])
        df['release_date'] = pd.to_datetime(df['release_date'])
        
        return df
        
    elif name == 'clusters':
        df = pd.read_csv('data/cleanData/character_clusters_cleaned.csv')
        return df
    
    elif name == 'summaries':
        df = pd.read_csv('data/cleanData/summaries_cleaned.csv')
        return df
    
    else:
        print('Invalid dataframe name')
        return None
    