import pandas as pd
import numpy as np

m_cols = ['anime_id', 'name']
animes = pd.read_csv('..\\data\\anime.csv', usecols = m_cols)

r_cols = ['user_id', 'anime_id', 'rating']
ratings = pd.read_csv('..\\data\\rating.csv',  sep=',', usecols=r_cols)

# Filtramos por ratings válidos (mayores a 0)
ratings_filtrados = ratings[ratings['rating'] >= 0]

anime_counts = ratings_filtrados.groupby('anime_id')['rating'].count()

animes_populares = anime_counts[anime_counts > 100].index

# Filtramos por número mínimo de ratings que tenga un anime
ratings = ratings_filtrados[ratings_filtrados['anime_id'].isin(animes_populares)]


# Eliminamos los duplicados para anime y ratings checkeando previamente si hay alguno en cada uno de los csv
duplicates_ratings = ratings.duplicated(subset=['user_id', 'anime_id']).sum()
if duplicates_ratings > 0:
    dup_mask = ratings.duplicated(subset=['user_id', 'anime_id'], keep=False)

duplicates_animes = animes.duplicated(subset=['anime_id', 'name']).sum()
if duplicates_animes > 0:
    dup_mask = animes.duplicated(subset=['anime_id', 'name'], keep=False)

# Comprovamos que los rating negativos se hayan eliminado
print("Mínimo rating:", ratings['rating'].min())
ratings.head()
# animes.head()

counts_per_anime = ratings['anime_id'].value_counts()
print(counts_per_anime.describe())

for p in [50, 75, 90, 95, 99]:
    print(f"P{p} =", int(counts_per_anime.quantile(p/100)))

counts_per_user = ratings['user_id'].value_counts()
print(counts_per_user.describe())

for p in [50, 75, 90, 95, 99]:
    print(f"P{p} =", int(counts_per_user.quantile(p/100)))

# Comptem usuaris abans del filtre
usuaris_abans = ratings['user_id'].nunique()

# Apliquem filtre d'usuaris
MIN_RATINGS_USER = 5
counts_user = ratings['user_id'].value_counts()
valid_users = counts_user[counts_user >= MIN_RATINGS_USER].index
ratings = ratings[ratings['user_id'].isin(valid_users)].copy()

# Comptem usuaris i files després
usuaris_despres = ratings['user_id'].nunique()
files_despres = len(ratings)

print("Usuaris abans del filtre:", usuaris_abans)
print("Usuaris després del filtre:", usuaris_despres)
print("Files totals després del filtre:", files_despres)

# percetantge de dades que he conservat
percentatge = len(ratings) / len(ratings) * 100
print(f"Percentatge de files conservades: {percentatge:.2f}%")


MAX_RATINGS_USER = counts_user.quantile(0.99)  # ≈ 617
valid_users = counts_user[
    (counts_user >= 5) &
    (counts_user <= MAX_RATINGS_USER)
].index

ratings = ratings[ratings['user_id'].isin(valid_users)].copy()
# Comptem usuaris i files després del filtre superior
usuaris_despres2 = ratings['user_id'].nunique()
files_despres2 = len(ratings)

print("Usuaris després del filtre superior:", usuaris_despres2)
print("Files totals després del filtre superior:", files_despres2)

# Percentatge de files conservades respecte a l'original
percentatge2 = len(ratings) / len(ratings) * 100
print(f"Percentatge de files conservades: {percentatge2:.2f}%")

perdua_usuaris = usuaris_abans - usuaris_despres2
print(f"Usuaris eliminats en total: {perdua_usuaris}")

animeRatings = ratings.pivot_table(index=['user_id'],columns=['anime_id'],values='rating')
# animeRatings.head()

HatsukoiRatings = animeRatings[7669]
HatsukoiRatings = HatsukoiRatings.dropna()
HatsukoiRatings.head()

similarAnimesToHatsukoi = animeRatings.corrwith(HatsukoiRatings)
similarAnimesToHatsukoi = similarAnimesToHatsukoi.dropna()

df = pd.DataFrame(similarAnimesToHatsukoi)
print(df.head(10))

similarAnimesToHatsukoi.sort_values(ascending=False).head(40)

animeStatsNuevo = ratings.groupby('anime_id').agg({'rating': np.size})
print(animeStatsNuevo.head(15))

animeStatsPromedo = ratings.groupby('anime_id').agg({'rating': np.mean})

animeStatsPromedo = animeStatsPromedo.sort_values('rating', ascending=False)
print(animeStatsPromedo.head(10))

corrMatrix = animeRatings.corr(method='pearson', min_periods=100)
# corrMatrix.head()

myRatings = pd.Series({11061: 10, 2476: 1})

simCandidates = pd.Series(dtype='float64')

for anime_id, rating in myRatings.items():
    print(f"Añadiendo animes similares a {anime_id}...")
    
    # Recuperar los animes similares a los calificadas
    sims = corrMatrix[anime_id].dropna()
    
    # Escalar la similaridad multiplicando la correlación por la calificación del usuario
    sims = sims.map(lambda x: x * rating)
    
    # Añadir el puntaje a la lista de candidatos similares
    simCandidates = pd.concat([simCandidates, sims])

# Mirar los resultados
print("Ordenando...")
simCandidates = simCandidates.groupby(simCandidates.index).sum()  # Sumar puntuaciones duplicadas
simCandidates.sort_values(inplace=True, ascending=False)
filteredSims = simCandidates.drop(myRatings.index)
print(filteredSims.head(10))

# Convertir la Series en DataFrame para hacer merge
simCandidates_df = filteredSims.reset_index()
simCandidates_df.columns = ['anime_id', 'score']

# Merge con el DataFrame de animes para obtener los nombres
simCandidates_df = simCandidates_df.merge(animes, on='anime_id')

# Reordenar columnas para legibilidad
simCandidates_df = simCandidates_df[['anime_id', 'name', 'score']]

# Mostrar las 10 recomendaciones principales con nombres
simCandidates_df.head(10)
