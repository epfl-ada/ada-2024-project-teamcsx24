# From Local Production to Global Screens: How the Film Industry Reflects Globalization

Website URL : https://blaisedepauw.github.io/teamCSX/datastory

## Abstract

Our project, "From local production to global screens: How the film industry reflects globalization", seeks to reveal how cinema mirrors the broader process of globalization across three key dimensions: economic, cultural, and population. Motivated by a desire to make globalization more engaging, we position ourselves as a history teacher passionate about cinema. This passion-driven approach aims to transform the often dry topic of globalization into a captivating dialogue between a teacher and their class, featuring a particularly challenging student and an intelligent, insightful one. Economically, our project examines how co-productions and box office trends reflect global trade in the film industry. Culturally, we explore how film genres and iconic characters transcend borders, revealing cultural exchanges. In terms of population, we analyze actor diversity to highlight increased global mobility. Our motivation is to tell the story of cinema's role in fostering a more interconnected and culturally blended world.

---

## Research Questions

1. **Economic Globalization**
   - Is the movie industry representative of the economic aspect of globalization? For example, how did the number of movie co-productions between countries evolve? 
   - What is the impact of an international co-production on the budget allocated to each movie?  

2. **Cultural Globalization**
   - Can we see a uniformization of the culture through the evolution of the genres and topics of the movies that are produced?
   - Can we see the cultural influence that some regions of the world have on others? 
   - Are there some movie characters that originate from a country and are also present in foreign movies?  
   - Are there topics treated in movies which travelled over time and space ?

3. **Population Mobility**
   - Does the diversity of actors' ethnicity in each movie increase over time? 
   - Can we see an increasing number of actors that take part in movies produced by different countries?  
   - Considering the number of translations available, where do the films that reach the largest audiences originate from?

4. **Correlation**
   - Overall, is there a correlation between the globalization of the cinema industry and an existing globalization index?

---

## Proposed Additional Datasets

- We need a premade world map to plot with geopandas: [Natural Earth Data](https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-0-countries/)
- We need to consider inflation to adjust the revenue: [Kaggle Inflation Dataset](https://www.kaggle.com/datasets/varpit94/us-inflation-data-updated-till-may-2021)
- We consider additional movies to add consistency to the results of the Economics part: [TMDB Data](https://www.kaggle.com/datasets/kakarlaramcharan/tmdb-data-0920)
- We downloaded the data on the KOF index from the website https://kof.ethz.ch/en/forecasts-and-indicators/indicators/kof-globalisation-index.html 
---

## Project Plans & Methods

### Part I: Data and Processing
For each segment of economy, culture, and population, we extract a new processed dataset from the cleaned dataset containing only the features relevant to that segment. This approach enables more efficient use of each dataset for the subsequent analysis. We also built different dictionaries to link each FreebaseID to the corresponding feature. 

### Part II: Economy
Our goal in this section is to show how the film industry's market bears witness to economic globalization.

1. To address the free trade in goods and services, we will examine the box office revenue of films over time globally and by country.
2. Focus on co-productions to estimate the influence of cross-country productions on the revenue as a witness to globalization.
3. Tackle the evolution of the number of co-productions over time to highlight the free trade in goods and services.

### Part III: Culture
Our goal in this section is to study the cultural influences that countries have on each other’s films.

1. **Genres:** Genre Analysis involves studying the evolution and distribution of movie genres over time and across different regions. This method typically includes identifying the most common genres, examining their progression by year and country, and exploring regional trends. By analyzing the frequency and appearance of genres over time, researchers can observe shifts in movie preferences and genre diversity.
2. **Topics:** Topic Modeling is a technique used to identify hidden themes in text data. In this case, it is applied to movie data to uncover topics like "Martial Arts" or "Love and Family". The process involves preprocessing the text (removing stopwords, tokenizing, and lemmatizing), applying the BERTopic algorithm to identify topics, and preparing the data by linking movies to their respective topics. The results are visualized on a world map to show the global distribution of these topics, with statistical analysis revealing the spread across countries and regions. This helps to understand how topics evolve over time and across geographies.
3. **US Cultural Influence:** Analyze US cultural influences through themes by examining the impact of the United States on the themes of films produced in other countries. This involves clustering countries using geographic clustering and centroid-based techniques. NLP methods, such as Hugging Face’s Transformers for zero-shot classification are used.
4. **Characters:** Focus on characters and their appearances in productions from various countries. Deduce character origins through story settings analyzed with Hugging Face Transformers to enhance cultural influence assessments.

### Part IV: Population
The goal in this section is to see whether the movements and globalization of populations are visible in the movie industry.

1. Visualize actor mobility by plotting an interactive map linking countries where actors worked.
2. Analyze the average proportion of each ethnicity in movies over time. Steps include:
   - Match Freebase_IDs to ethnicity names via Wikidata.
   - Cluster or reduce the number of ethnicities for better visualization.
3. Explore insights from the number of translations available for each country's films.

### Part V: Data Story
For each part of our analysis, we want to compare our results to actual information about globalization to make the teacher’s course interesting and pedagogic. We will need to find a globalization index that is relevant to our topic.

---

## Proposed Timeline

| Date         | Milestone                                                              |
|--------------|------------------------------------------------------------------------|
| 15.11.2024   | Primary analysis on all parts                                         |
| 22.11.2024   | Homework 2                                                            |
| 29.11.2024   | Implementation of specific methods and adaptation based on feedback   |
| 06.12.2024   | Final analysis and visualization of results                           |
| 13.12.2024   | Website creation                                                      |
| 20.12.2024   | Final review of the Data story and repository cleaning                |

Along the different steps of the project, we managed to follow this proposed timeline. 

---

## Organization Within the Team

- **Pauline:** Part IV
- **Arnaud:** Part I (Data processing) & Part III (Genres & Topics) 
- **Aurélien:** Part I (Additional Dataset) & Part II
- **Blaise:** Part V (Website creation)
- **Oscar:** Part III  (US cultural influence & characters)

Each member has done the data analysis of its part and the associated data story.

---


## Quickstart

```bash
# clone project
git clone <project link>
cd <project repo>

# [OPTIONAL] create conda environment
conda create -n <env_name> python=3.11
conda activate <env_name>


# install requirements  (Proposed at the beginning of the result notebook)
pip install -r pip_requirements.txt
```





## Project Structure

The directory structure of new project looks like this:

```
├── data                        <- Project data files
│   ├── additionalData          <- Contains all the additional Dataset
│   ├── cleanData               <- Processed data used in the analysis
│   ├── cultureData             <- Prepares dataframes for cultural analysis
│   ├── freebaseIdDictionnaries     <- Contains dictionnaries (freebaseId, world region, actors...)
│   ├── map                     <- Contains geopanda data
│   ├── MovieSummaries          <- Raw data
│
├── src                         <- Source code
│   ├── data                            <- Contains the work on data processing
│   ├── models                          <- Model directory (Models used in the topic modeling analysis and the NLP models)
│   ├── utils                           <- Utility directory
│   ├── scripts                         <- Shell scripts
│
│
├── results.ipynb               <- a well-structured notebook showing the results
│
├── .gitignore                  <- List of files ignored by git
├── pip_requirements.txt        <- File for installing python dependencies
└── README.md
```

