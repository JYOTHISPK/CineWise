import numpy as np
import json
from src.ContentBased import df,generate_content_scores
from src.mapping import (
    region_map,
    age_map,
    movie_era_map
)


def get_age_group(age) :

    if age < 18 :
        return "teen"
    elif age <=30 :
        return "young_adult"
    elif age <=50 :
        return "adult"
    return "senior"

def get_movie_era(Year) :

    if Year < 1980 :
        return "before_1980"
    elif Year < 1990 :
        return "1980_1990"
    elif Year < 2000 :
        return "1990_2000"
    return "after_2000"

def recommend() :

    with open( "data/user_data.json", "r" ) as f: 
        data = json.load(f) 
        
    region = data["region"] 
    age = data["age"]

    content_score, unwatched, weightage_first, weightage_second =  generate_content_scores() 

    new_df = df.loc[unwatched]

    unwatched_score = np.zeros(len(unwatched))

    age_group = get_age_group(age)

    index = 0

    recommendations = []

    for id , name , rating, year, language , genre in zip(new_df["movie_id"], new_df["Movie Name"], new_df["Rating(10)"], new_df["Year"], new_df["Language"],new_df["Genre"]):

        score=0

        movie_era = get_movie_era(year)

        # region score

        if language in region_map[region] :
            score += 1

        # age score

        for g in age_map[age_group] :
            if g in genre :
                score +=1
                break
        
        # movie era score

        score += movie_era_map[age_group][movie_era]

        unwatched_score[index] = score 
        index += 1

        recommendations.append(
                {
                "id"       : id,
                "name"     : name,
                "year"     : year,
                "language" : language,
                "genre"    : genre,
                "rating"   : rating,
                "score"    : score,
                }
            )
            
    

    max_score = max(unwatched_score)
    min_score = min(unwatched_score)

    denominator = max_score - min_score

    if denominator == 0:
        normalised_score = np.zeros(len(unwatched_score))
    else:
        normalised_score = (
            unwatched_score - min_score
        ) / denominator

    index = 0

    for i, j in zip(content_score.keys(), normalised_score):
        recommendations[index]["score"] = float (content_score[i] *weightage_first + j *weightage_second)
        index += 1

    
    recommendations = sorted(recommendations , key = lambda x:x["score"] , reverse=True)
        
    return recommendations
          
    
