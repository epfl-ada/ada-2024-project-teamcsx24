# --------------------------------------------------------------------
# General functions utils for the project
# --------------------------------------------------------------------

# Importing libraries
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import json

# Function to compare the intersection between two DataFrames
def intersectionId(df1, df2, name1, name2, id_column='id'):
    # Ids extraction from each DataFrame
    ids1 = set(df1[id_column].unique())
    ids2 = set(df2[id_column].unique())
    
    # Compute intersection and differences
    intersection = ids1 & ids2
    only_df1 = ids1 - ids2
    only_df2 = ids2 - ids1
    
    # Count elements
    count_intersection = len(intersection)
    count_only_df1 = len(only_df1)
    count_only_df2 = len(only_df2)
    total = count_intersection + count_only_df1 + count_only_df2

    # Venn diagram
    venn = venn2(subsets=(1, 1, 1), set_labels=(name1, name2))
    
    # Add counts
    venn.get_label_by_id('10').set_text(f'{count_only_df1}')
    venn.get_label_by_id('01').set_text(f'{count_only_df2}')
    venn.get_label_by_id('11').set_text(f'{count_intersection}')
    
    plt.title("Intersection between " + name1 + " and " + name2)
    plt.show()

# Function to transform country names to geopandas names
def transformCountryNameGpd(countries_freebase_id):
    # Load countries dictionnary
    with open('../../data/freebaseIdDictionnaries/countries_geo', 'r') as file:
        countries_dict = json.load(file)
    
    # Transform countries names to geopandas names using the freebase id
    countries_name = []
    n = len(countries_freebase_id)
    for i in range(n):
        country_freebase_id = countries_freebase_id[i]
        country_name = countries_dict[country_freebase_id]
        countries_name.append(country_name)
    
    return countries_name

# Attach a world region to each country
def attachWorldRegion(country):
    # Load countries dictionnary
    with open('../../data/freebaseIdDictionnaries/regions', 'r') as file:
        countries_regions = json.load(file)
    
    # Attach a world region to each country
    world_region = countries_regions[country]
    
    return world_region

