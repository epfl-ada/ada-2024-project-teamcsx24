import pandas as pd

# Function to load dataframes and preprocess the additional data

def loadAdditionalDataframe(name, path_to_directory):
    if name == 'inflation_monthly':
        df = pd.read_csv(path_to_directory + 'Kaggle_US_CPI_monthly_cleaned.csv')
        
        df['Yearmon'] = pd.to_datetime(df['Yearmon'])
        df['year'] = df['Yearmon'].dt.year
        
        return df
    
    elif name == 'inflation_annual':
        df = pd.read_csv(path_to_directory + 'Kaggle_US_CPI_annual_cleaned.csv')
                
        return df
    
    elif name == 'movies_additional':
        df = pd.read_csv(path_to_directory + 'Kaggle_movie_data_tmdb_cleaned.csv')

        return df
    
    elif name == 'movies_additional_filtered':
        df = pd.read_csv(path_to_directory + 'Kaggle_movie_data_tmdb_filtered_cleaned.csv')

        return df
    
    else:
        print('Invalid dataframe name')
        return None