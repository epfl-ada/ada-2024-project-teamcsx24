# From Local Production to Global Screens: How the Film Industry Reflects Globalization

## Abstract

Our project, "From local production to global screens: How the film industry reflects globalization", seeks to reveal how cinema mirrors the broader process of globalization across three key dimensions: economic, cultural, and population. Motivated by a desire to make globalization more engaging, we position ourselves as a history teacher passionate about cinema. This passion-driven approach aims to transform the often dry topic of globalization into a captivating dialogue between a teacher and their class, featuring a particularly challenging student and an intelligent, insightful one. Economically, our project examines how co-productions and box office trends reflect global trade in the film industry. Culturally, we explore how film genres and iconic characters transcend borders, revealing cultural exchanges. In terms of population, we analyze actor diversity to highlight increased global mobility. Our motivation is to tell the story of cinema's role in fostering a more interconnected and culturally blended world.

---

## Research Questions

1. **Economic Globalization**
   - Is the movie industry representative of the economic aspect of globalization? For example, how did the number of movie co-productions between countries evolve? 
   - What is the impact of an international co-production on the budget allocated to each movie? 
   - How does the movie industry highlight the globalization of culture?  

2. **Cultural Globalization**
   - Can we see a uniformization of the culture through the evolution of the genres and topics of the movies that are produced?
   - Can we see the cultural influence that some regions of the world have on others? 
   - Are there some movie characters that originate from a country and are also present in foreign movies?  
   - Are there movie summaries that mention foreign countries or regions and how did it evolve over time?

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

---

## Project Plans & Methods

### Data and Processing
For each segment of economy, culture, and population, we extract a new processed dataset from the cleaned dataset containing only the features relevant to that segment. This approach enables more efficient use of each dataset for the subsequent analysis. We also built different dictionaries to link each FreebaseID to the corresponding feature. 

### Part I: Economy
Our goal in this section is to show how the film industry's market bears witness to economic globalization.

1. To address the free trade in goods and services, we will examine the box office revenue of films over time globally and by country.
2. Focus on co-productions to estimate the influence of cross-country productions on the revenue as a witness to globalization.
3. Tackle the evolution of the number of co-productions over time to highlight the free trade in goods and services.

### Part II: Culture
Our goal in this section is to study the cultural influences that countries have on each other’s films.

1. **Themes:** Analyze cultural influences through themes by examining the impact of the United States on the themes of films produced in other countries. This involves clustering countries using geographic clustering and centroid-based techniques. NLP methods, such as SpaCy for Named Entity Recognition (NER), Hugging Face’s Transformers for zero-shot classification, and BERTopic for theme extraction, are used.
2. **Characters:** Focus on characters and their appearances in productions from various countries. Deduce character origins through story settings analyzed with Hugging Face Transformers to enhance cultural influence assessments.

### Part III: Population
The goal in this section is to see whether the movements and globalization of populations are visible in the movie industry.

1. Visualize actor mobility by plotting an interactive map linking countries where actors worked.
2. Analyze the average proportion of each ethnicity in movies over time. Steps include:
   - Match Freebase_IDs to ethnicity names via Wikidata.
   - Cluster or reduce the number of ethnicities for better visualization.
3. Explore insights from the number of translations available for each country's films.

### Part IV: Data Story
For each part of our analysis, we want to compare our results to actual information about globalization to make the teacher’s course interesting and pedagogic. We will need to find a globalization index that is relevant to our topic.

---

## Proposed Timeline

| Date         | Milestone                                                              |
|--------------|------------------------------------------------------------------------|
| 15.11.2024   | Primary analysis on all parts                                         |
| 22.11.2024   | Homework 2                                                            |
| 29.11.2024   | Implementation of specific methods and adaptation based on feedback   |
| 06.12.2024   | Final analysis and visualization of results                           |
| 13.12.2024   | Website creation                                                     |
| 20.12.2024   | Final review of the Data story and repository cleaning                |

---

## Organization Within the Team

- **Pauline:** Part III
- **Arnaud:** Part II and overall support  
- **Aurélien:** Part I  
- **Blaise:** Part IV and Website creation  
- **Oscar:** Part II  

---

## Questions for TAs

1. Would it be interesting to concretely demonstrate the correlation between the film industry and globalization using a homemade globalization index created for each part (economic, cultural, population), or only one for the final conclusion? Considering that our created index might not be entirely representative.
2. Is our data story based on the history teacher passionate about cinema interesting enough? Considering that globalization class is often disliked by students, our goal is to make it interactive with a challenging student to whom we need to explain the very base of the course, and an insightful one who dives deeper into the information to give the class interesting anecdotes.


## Quickstart

```bash
# clone project
git clone <project link>
cd <project repo>

# [OPTIONAL] create conda environment
conda create -n <env_name> python=3.11 or ...
conda activate <env_name>


# install requirements
pip install -r pip_requirements.txt
```



### How to use the library
Tell us how the code is arranged, any explanations goes here.



## Project Structure

The directory structure of new project looks like this:

```
├── data                        <- Project data files
│
├── src                         <- Source code
│   ├── data                            <- Data directory
│   ├── models                          <- Model directory
│   ├── utils                           <- Utility directory
│   ├── scripts                         <- Shell scripts
│
├── tests                       <- Tests of any kind
│
├── results.ipynb               <- a well-structured notebook showing the results
│
├── .gitignore                  <- List of files ignored by git
├── pip_requirements.txt        <- File for installing python dependencies
└── README.md
```

