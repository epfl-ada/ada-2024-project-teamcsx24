# geopanda.py
import matplotlib.pyplot as plt
import geopandas as gpd

def plot_world(world, column=None, color=None, title=None):

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot()

    world.plot(
        ax=ax,
        column=column,
        cmap=color,
        legend=True,
        legend_kwds={'label': f"{column} by Country"},
        edgecolor="black",
        alpha=0.5
    )

    ax.set_xticks([])
    ax.set_yticks([])

    plt.title(title or f"World Map: {column}")
    plt.show()


#create the class from film coutries to correspond to geopandas countries

united_states_of_america = ['Puerto Rico']
uzbekistan = ['Uzbek SSR']
democratic_republic_of_the_congo = ['Congo']
russia = ['Soviet Union', 'Crime', 'Ukrainian SSR', 'Ukranian SSR', 'Georgian SSR', 'Soviet occupation zone']
the_bahamas = ['Bahamas','Aruba']
united_kingdom = ['England', 'Northern Ireland', 'Scotland', 'Wales', 'Isle of Man', 'Kingdom of Great Britain']
france = ['Monaco']
israel = ['Mandatory Palestine', 'Palestinian territories', 'Palestinian Territories']
iraq = ['Iraqi Kurdistan']
myanmar = ['Burma']
south_korea = ['Korea']
india = ['Malayalam Language']
germany = ['German Democratic Republic', 'West Germany', 'Nazi Germany', 'Weimar Republic', 'German Language']
china = ['Hong Kong', 'Macau', 'Republic of China']
italy = ['Kingdom of Italy','Malta']
slovenia = ['Yugoslavia', 'Socialist Federal Republic of Yugoslavia', 'Federal Republic of Yugoslavia']
slovakia = ['Slovak Republic']
czechia = ['Czech Republic', 'Czechoslovakia']
north_macedonia = ['Republic of Macedonia']
republic_of_serbia = ['Serbia', 'Serbia and Montenegro']
qatar = ['Bahrain']
malaysia = ['Singapore']

# Function to replace the countries in the dictionary
def replace_countries(countries_dict_copy):
    # Replace every value in the lists above by the list title
    for key, value in countries_dict_copy.items():
        if value in united_states_of_america:
            countries_dict_copy[key] = 'United States of America'
        elif value in uzbekistan:
            countries_dict_copy[key] = 'Uzbekistan'
        elif value in democratic_republic_of_the_congo:
            countries_dict_copy[key] = 'Democratic Republic of the Congo'
        elif value in russia:
            countries_dict_copy[key] = 'Russia'
        elif value in the_bahamas:
            countries_dict_copy[key] = 'The Bahamas'
        elif value in united_kingdom:
            countries_dict_copy[key] = 'United Kingdom'
        elif value in france:
            countries_dict_copy[key] = 'France'
        elif value in israel:
            countries_dict_copy[key] = 'Israel'
        elif value in iraq:
            countries_dict_copy[key] = 'Iraq'
        elif value in myanmar:
            countries_dict_copy[key] = 'Myanmar'
        elif value in south_korea:
            countries_dict_copy[key] = 'South Korea'
        elif value in india:
            countries_dict_copy[key] = 'India'
        elif value in germany:
            countries_dict_copy[key] = 'Germany'
        elif value in china:
            countries_dict_copy[key] = 'China'
        elif value in italy:
            countries_dict_copy[key] = 'Italy'
        elif value in slovenia:
            countries_dict_copy[key] = 'Slovenia'
        elif value in slovakia:
            countries_dict_copy[key] = 'Slovakia'
        elif value in czechia:
            countries_dict_copy[key] = 'Czechia'
        elif value in north_macedonia:
            countries_dict_copy[key] = 'North Macedonia'
        elif value in republic_of_serbia:
            countries_dict_copy[key] = 'Republic of Serbia'
        elif value in qatar:
            countries_dict_copy[key] = 'Qatar'
        elif value in malaysia:
            countries_dict_copy[key] = 'Malaysia'
    return countries_dict_copy