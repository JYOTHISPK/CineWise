from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from scipy.spatial.distance import jensenshannon
import streamlit as st
import json


PROJECT_ROOT = Path.cwd()

while not (PROJECT_ROOT / "data").exists() :
    PROJECT_ROOT = PROJECT_ROOT.parent

df=pd.read_csv(PROJECT_ROOT / "data" / "more cleaned movies.csv")

df = df.reset_index(drop=True)

df["movie_id"] = df.index


@st.cache_resource
def load_vectorizer():

    cv = CountVectorizer()

    count_matrix = cv.fit_transform(
        df["Combined_Features"]
    )

    return cv, count_matrix

cv, count_matrix = load_vectorizer()


# ---------------- LOAD USER DATA ---------------- #

def load_user_data():

    with open(
        "data/user_data.json",
        "r"
    ) as f:

        data = json.load(f)

    return (
        data["liked"],
        data["disliked"],
        data["watched"]
    )


# ---------------- SAVE FUNCTION ---------------- #

def save_user_data(
    liked,
    disliked,
    watched
):

    with open(
        "data/user_data.json",
        "r"
    ) as f:

        data = json.load(f)

    data["liked"] = liked
    data["disliked"] = disliked
    data["watched"] = watched

    with open(
        "data/user_data.json",
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )



def generate_content_scores():

    liked, disliked, watched = load_user_data()

    watched_all = set(liked + disliked  + watched)

    movies = df['Movie Name']

    unwatched = []
    for i,j in enumerate(movies) :
        if i not in watched_all :
            unwatched.append(i)


    unwatched_matrix = count_matrix[unwatched]

    liked_score = np.zeros(len(unwatched))
    disliked_score = np.zeros(len(unwatched))
    watched_score = np.zeros(len(unwatched))

    if liked:
        liked_score = cosine_similarity(
            unwatched_matrix,
            count_matrix[liked]
        ).mean(axis=1)

    if disliked:
        disliked_score = cosine_similarity(
            unwatched_matrix,
            count_matrix[disliked]
        ).mean(axis=1)

    if watched:
        watched_score = cosine_similarity(
            unwatched_matrix,
            count_matrix[watched]
        ).mean(axis=1)


    #WEIGHTAGE

    length = len(watched)

    if length :

        weightage_second = max(0.1,1-(length*0.1))

        weightage_first = 1 - weightage_second

    else :

        weightage_second = 1
        weightage_first  = 0

    #PENALTY

    if liked and disliked :

        liked_matrix = count_matrix[liked]
        disliked_matrix = count_matrix[disliked]

        p = liked_matrix.sum(axis=0).A1
        q = disliked_matrix.sum(axis=0).A1

        P = p / p.sum()
        Q = q / q.sum()

        distance = jensenshannon( P , Q )
        divergence = distance ** 2

        if divergence < 0.4 and liked:
            divergence = 0.4
            if len(disliked) >= 2 * len(liked):
                divergence *= 2

    else :

        divergence = 1


    final_scores = (
        (
        1.5 * liked_score
        - 3 * disliked_score * divergence
        + watched_score * 0.5
        )
    )

    max_score = max(final_scores)
    min_score = min(final_scores)

    denominator = max_score - min_score

    if denominator == 0:
        normalised_score = np.zeros(len(final_scores))
    else:
        normalised_score = (
            final_scores - min_score
        ) / denominator

    content_score = dict(zip(unwatched, normalised_score))

    return (
        content_score,
        unwatched,
        weightage_first,
        weightage_second
    )