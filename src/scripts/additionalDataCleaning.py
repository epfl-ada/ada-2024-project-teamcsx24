import pandas as pd
import ast

# --- Data loading ---

# Additional movie data from Kaggle

df_movies_additional = pd.read_csv('data/additionalData/Kaggle_movie_data_tmdb_filtered.csv')
print('Additional Movies successfully loaded')

df_inflation_additional_monthly = pd.read_csv('data/additionalData/Kaggle_US_CPI.csv')
print('Monthly inflation data successfully loaded')

# --- Data preprocessing ---

# -- Additional movie data from Kaggle --

# Convert budget to pd.to_numeric format

df_movies_additional['budget'] = pd.to_numeric(df_movies_additional['budget'], errors='coerce')
print('Budget successfully converted')

# Additional movie data from Kaggle where budget is not null

df_movies_additional_filtered = df_movies_additional.loc[df_movies_additional['budget'] != 0]
print('Filtered additional movie data successfully created')

# -- Inflation data --

df_inflation_additional_monthly['Yearmon'] = pd.to_datetime(df_inflation_additional_monthly['Yearmon'])
df_inflation_additional_monthly['year'] = df_inflation_additional_monthly['Yearmon'].dt.year
df_inflation_additional_annual = df_inflation_additional_monthly.groupby('year')['CPI'].mean().reset_index()
print('Inflation data successfully processed')

# --- Data saving ---

def save_dataset(df, filename):
    file_path = f'data/cleanData/{filename}.csv'
    df.to_csv(file_path, index=False)
    print(f"Saved {filename} to {file_path}")

# Save cleaned dataset
save_dataset(df_inflation_additional_monthly, 'Kaggle_US_CPI_monthly_cleaned')
print('Saved monthly inflation data to Kaggle_US_CPI_monthly_cleaned.csv')

save_dataset(df_inflation_additional_annual, 'Kaggle_US_CPI_annual_cleaned')
print('Saved annual inflation data to Kaggle_US_CPI_annual_cleaned.csv')

save_dataset(df_movies_additional, 'Kaggle_movie_data_tmdb_cleaned')
print('Saved additional movie data to Kaggle_movie_data_tmdb_cleaned.csv')

save_dataset(df_movies_additional_filtered, 'Kaggle_movie_data_tmdb_filtered_cleaned')
print('Saved filtered additional movie data to Kaggle_movie_data_tmdb_filtered_cleaned.csv')
