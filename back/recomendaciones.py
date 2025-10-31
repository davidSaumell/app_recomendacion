import json
import os
import pandas as pd

MIN_RATINGS_FOR_ANIME = 100
MIN_RATINGS_USER = 5
MIN_PERIODS_CORR = 100

def Train_model():
    os.makedirs("models", exist_ok=True)

    # READ MODEL VERSION #
    version_file = "models/current_model.json"
    if os.path.exists(version_file):
        with open(version_file) as f:
            info = json.load(f)
        current_version = float(info["model_version"])
        new_version = round(current_version + 0.1, 1)
    else:
        new_version = 1.0

    # GET DATA #
    m_cols = ['anime_id', 'name']
    animes = pd.read_csv('..\\data\\anime.csv', usecols = m_cols)
    r_cols = ['user_id', 'anime_id', 'rating']
    ratings = pd.read_csv('..\\data\\rating.csv',  sep=',', usecols=r_cols)

    # FILTER #
    ratings_filtrados = ratings[ratings['rating'] >= 0]
    anime_counts = ratings_filtrados.groupby('anime_id')['rating'].count()
    animes_populares = anime_counts[anime_counts > MIN_RATINGS_FOR_ANIME].index
    ratings = ratings_filtrados[ratings_filtrados['anime_id'].isin(animes_populares)]

    duplicates_ratings = ratings.duplicated(subset=['user_id', 'anime_id']).sum()
    if duplicates_ratings > 0:
        ratings = ratings.drop_duplicates(subset=['user_id','anime_id'], keep='last')
    duplicates_animes = animes.duplicated(subset=['anime_id', 'name']).sum()
    if duplicates_animes > 0:
        animes = animes.drop_duplicates(subset=['anime_id','name'], keep='last')

    counts_user = ratings['user_id'].value_counts()
    MAX_RATINGS_USER = counts_user.quantile(0.99)  # 617
    valid_users = counts_user[
        (counts_user >= MIN_RATINGS_USER) &
        (counts_user <= MAX_RATINGS_USER)
    ].index
    ratings = ratings[ratings['user_id'].isin(valid_users)].copy()

    # CREATE CORRELATION #
    animeRatings = ratings.pivot_table(index=['user_id'],columns=['anime_id'],values='rating')
    corrMatrix = animeRatings.corr(method='pearson', min_periods=MIN_PERIODS_CORR)

    # CREATE MODEL #
    model_path = f"models/anime_model_v{new_version:.1f}.pkl"
    corrMatrix.to_pickle(model_path)
    info = {
        "model_version": f"{new_version:.1f}",
        "artifact_path": model_path
    }
    with open(version_file, "w") as f:
        json.dump(info, f, indent=4)

def Load_model():
    with open("models/current_model.json") as f:
        info = json.load(f)
    return pd.read_pickle(info["artifact_path"]) 

def Get_recomendations(user_preferences):
    corrMatrix = Load_model()

    myRatings = pd.Series(user_preferences)
    simCandidates = pd.Series(dtype='float64')

    for anime_id, rating in myRatings.items():
        if anime_id not in corrMatrix.columns:
            continue       
        sims = corrMatrix[anime_id].dropna()
        sims = sims.map(lambda x: x * rating)
        simCandidates = pd.concat([simCandidates, sims])

    if simCandidates.empty:
        return pd.DataFrame(columns=["anime_id", "score"])

    simCandidates = simCandidates.groupby(simCandidates.index).sum()
    simCandidates.sort_values(inplace=True, ascending=False)
    filteredSims = simCandidates.drop(myRatings.index)
    result = pd.DataFrame({"anime_id": filteredSims.index, "score": filteredSims.values})
    return result[["anime_id", "score"]]
