import pandas as pd
import ast

# --- Data loading ---

# Movie dataset
df_movies = pd.read_csv('data/MovieSummaries/movie.metadata.tsv', sep='\t', header=None)
df_movies.columns = ['wiki_id','freebase_id','original_title','release_date','revenue','runtime','languages','countries','genres']
print('Movies successfully loaded')

# Character dataset
df_characters = pd.read_csv('data/MovieSummaries/character.metadata.tsv', sep='\t', header=None)
df_characters.columns = ['wiki_id','freebase_id','release_date','character','birth_date','gender','height','ethnicity_freebase_id','name','age','character_actor_freebase_id','character_freebase_id','actor_freebase_id']
print('Characters successfully loaded')

# Character cluster dataset
df_cluster = pd.read_csv('data/MovieSummaries/name.clusters.txt', sep='	', header=None)
df_cluster.columns = ['cluster','character_actor_freebase_id']
print('Clusters successfully loaded')

# Summaries dataset
df_summary = pd.read_csv('data/MovieSummaries/plot_summaries.txt', sep='	', header=None)
df_summary.columns = ['wiki_id','summary']
print('Summaries successfully loaded')

# --- Data preprocessing ---

# Convert date to pd.datetime format
def correctDate(date):
    if '-' in date:
        if len(date) >= 10:
            return date
        else:
            return date + '-01'
    else:
        return date + '-01-01'
    
def convertDate(df, columns):
    for col in columns:
        df[col] = df[col].astype(str)
        df[col] = df[col].apply(correctDate)
        df[col] = pd.to_datetime(df[col], errors='coerce')
    return df
    
# Correction of an error
df_movies.loc[62836, 'release_date'] = '2010-12-02'

# Apply date conversion
df_movies = convertDate(df_movies, ['release_date'])
df_characters = convertDate(df_characters, ['release_date', 'birth_date'])
print('Dates successfully converted')

# Create dictionary of freebase id
def buildFreebaseDict(df, column_name):
    freebase_dict = {}
    
    for entry in df[column_name].dropna():
        id_data = ast.literal_eval(entry) if isinstance(entry, str) else entry
        for freebase_id, id_name in id_data.items():
            if freebase_id not in freebase_dict:
                freebase_dict[freebase_id] = id_name

    return freebase_dict

print('Build of countries dictionnary...')
dict_countries = buildFreebaseDict(df_movies, 'countries')
print('Build of languages dictionnary...')
dict_languages = buildFreebaseDict(df_movies, 'languages')
print('Build of genres dictionnary...')
dict_genres = buildFreebaseDict(df_movies, 'genres')

def buildFreebaseDictFromColumns(df, id_column, name_column):
    freebase_dict = {}
    
    # Iterate over the DataFrame rows
    for _, row in df.dropna(subset=[id_column, name_column]).iterrows():
        freebase_id = row[id_column]
        name = row[name_column]
        
        # Add the entry to the dictionary if not already present
        if freebase_id not in freebase_dict:
            freebase_dict[freebase_id] = name
    
    return freebase_dict

print('Build of actors dictionnary...')
dict_actor = buildFreebaseDictFromColumns(df_characters, 'actor_freebase_id', 'name')
print('Build of character dictionnary...')
dict_character = buildFreebaseDictFromColumns(df_characters, 'character_freebase_id', 'character')
print('Build of movies dictionnary...')
dict_movie = buildFreebaseDictFromColumns(df_movies, 'freebase_id', 'original_title')

# Save dictionnaries
import json

def saveDictionnary(dict, name):
    with open('data/freebaseIdDictionnaries/' + name, 'w') as fp:
        json.dump(dict, fp, indent=4)

saveDictionnary(dict_countries,'countries')
saveDictionnary(dict_genres, 'genres')
saveDictionnary(dict_languages,'languages')
saveDictionnary(dict_actor, 'actors')
saveDictionnary(dict_character, 'characters')
saveDictionnary(dict_movie, 'movies')
print('Dictionnaries successfully saved')

# Split freebase_id and content in two different columns
import re

def split_freebase_column(df, column_name):
    # Extract the Freebase IDs and associated names as lists
    df[f"{column_name}_freebase_id"] = df[column_name].apply(
        lambda x: re.findall(r'(/m/[^"]+)"', str(x)) if pd.notnull(x) else []
    )
    df[f"{column_name}"] = df[column_name].apply(
        lambda x: re.findall(r'":\s*"([^"]+)"', str(x)) if pd.notnull(x) else []
    )
    
    return df

# Apply the function to the columns
columns_to_transform = ['countries','languages','genres']
for col in columns_to_transform:
    df_movies = split_freebase_column(df_movies, col)
    
# Save cleaned datasets
def save_dataset(df, filename):
    file_path = f'data/cleanData/{filename}.csv'
    df.to_csv(file_path, index=False)
    print(f"Saved {filename} to {file_path}")

# Save each cleaned dataset
save_dataset(df_movies, 'movies_cleaned')
save_dataset(df_characters, 'characters_cleaned')
save_dataset(df_cluster, 'character_clusters_cleaned')
save_dataset(df_summary, 'summaries_cleaned')
print('Datasets successfully saved')

print('Data cleaning successfully done')