
# implementing web application for movie recommender using fastAPI

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import os
from fastapi import FastAPI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import uvicorn
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware


def clean_title(title):
    return re.sub("[^a-zA-Z0-9 ]","",title)



# create a function 'Search_movie'which returns top n(not necessarily in order) most relevant search results
def search_movie(title_query,n=1):
    print("searching movie titles...")
    title_query = clean_title(title_query)
    title_query_vector = tfidf_vectorizer.transform([title_query])
    similarity = cosine_similarity(titles_vector,title_query_vector).flatten()
    similarity_series = pd.Series(similarity)
    indices = similarity_series.nlargest(n).sort_values(ascending = False).index
    #indices = np.argpartition(similarity,-n)[-n:] #fetches indices of coresponding top 5 highest valued elements
    results = movies_df.iloc[indices][["movieId","title","genres"]]
    return results


def get_movie_recs(movieId,confidence=0.1,lift=2,top_n = 10):

    print("gettting movie recommendations...")

    # identify similar users liked your movie (M1)
    similar_users = ratings_df[(ratings_df.movieId == movieId) & (ratings_df.rating >= 4)]["userId"].unique()

    # Identifying movies liked by similar people(recommended movies list)
    similar_user_recs = ratings_df[(ratings_df.rating >=4)&(ratings_df.userId.isin(similar_users))]["movieId"]

    # calculating the Confidence(percentage of like minded people also liked other recommended movies(M2)) i.e. confidence(m1->m2)
    confidence_movie_recs = similar_user_recs.value_counts()/len(similar_users)

    # tune the confidence(m1 ->m2) = 10% ~ 30% and filter out best relevant movie m2 results.
    confidence_movie_recs = confidence_movie_recs[(confidence_movie_recs > confidence)] 
    
    # identifying support of each movie recs()
    all_users = ratings_df[(ratings_df.movieId.isin(confidence_movie_recs.index)&(ratings_df.rating >= 4))]["movieId"]
    support_movie_recs = all_users.value_counts()/len(ratings_df.userId.unique())

    # calculating lift for each movie recommendation
    lift_movie_recs = confidence_movie_recs/support_movie_recs

    # filtering out best recommendation by tuning lift threshold value greater than 1
    best_movie_recs = lift_movie_recs[lift_movie_recs >= lift]

    # sort the list by descinding order lift value
    best_movie_recs = best_movie_recs.sort_values(ascending=False)[:top_n]

    # return the recommended movies details
    return movies_df[movies_df.movieId.isin(best_movie_recs.index)][["title","genres"]]

def get_title_names(movies_df):
    print("getting search titles to display")
    return movies_df["title"].values

     
if __name__ == '__main__':
    # Get the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create absolute paths for the datasets
    movies_file = os.path.join(script_dir, 'dataset', 'movies.csv')
    ratings_file = os.path.join(script_dir, 'dataset', 'ratings.csv')

    # Read the CSV files
    movies_df = pd.read_csv(movies_file)
    ratings_df = pd.read_csv(ratings_file)
    print("dataset loaded...")

    # implement search engine
    movies_df["title_clean"] = movies_df.title.apply(clean_title)

    # Initialize the TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2))

    # Fit-transform the vectorizer to the title_clean column
    titles_vector = tfidf_vectorizer.fit_transform(movies_df['title_clean'])
    print("data Preprocessing done...")

    # implementing fastapi:
    app = FastAPI()
    # Add CORS middleware
    # CORS setup
    origins = [
    "null",  # Allow requests from the file:// protocol (local files)
    "http://localhost",
    "https://localhost",
    # Add more origins as needed
] # Replace with your actual frontend URL(s) in production

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["POST"],
        allow_headers=["*"],
)


    @app.get('/recommendations/{title:str}')
    def post_movie_titles(title:str):
        movie_id = search_movie(title)['movieId'].values[0]
        movies_df = get_movie_recs(movie_id)
        movies_dict_list = movies_df.to_dict()
        print("recommendations fetched: {}".format(movies_dict_list))
        return jsonable_encoder(movies_dict_list)
    
    uvicorn.run(app,host='127.0.0.1',port=5000)




