import pickle

import pandas as pd
import numpy as np

import json
import urllib.request
import requests

from tmdbv3api import Movie
from tmdbv3api import TMDb

# Import class
import CommonFunction

# Creating Object
objectCommonFunction = CommonFunction.CommonFunctionClass

class CollaborativeBasedClass:

    def __init__(self):
        self.user_item_matrix = pickle.load(open(r'.\CollaborativeBased\user_item_m.pkl', 'rb'))
        self.user_similarity = pickle.load(open(r'.\CollaborativeBased\user_similarity.pkl', 'rb'))
        self.item_similarity = pickle.load(open('.\CollaborativeBased\item_similarity.pkl', 'rb'))
        self.movies = pickle.load(open('.\CollaborativeBased\movies.pkl', 'rb'))
        self.tmdb = TMDb()
        self.tmdb.api_key = '3deeb4c3065471557db144f8f3f78056'
        self.api_key = '3deeb4c3065471557db144f8f3f78056'

        self.getidfromtitle = pd.Series(self.movies['movieId'].values.tolist(), index=self.movies['title'])
        self.gettitlefromid = pd.Series(self.movies['title'].values.tolist(), index=self.movies['movieId'])

    def user_based_recommendation(self, user, k=20, top_n=10):
        user_ix = self.user_item_matrix.index.get_loc(user)
        user_similarities = self.user_similarity[user_ix]
        most_similar_users = self.user_item_matrix.index[user_similarities.argpartition(-k)[-k:]]
        rec_movies = self.user_item_matrix.loc[most_similar_users].mean(0).sort_values(ascending=False)

        # Discard already seen movies
        m_seen_movies = self.user_item_matrix.loc[user].gt(0)
        seen_movies = m_seen_movies.index[m_seen_movies].tolist()
        rec_movies = rec_movies.drop(seen_movies).head(top_n)

        return rec_movies.index.to_frame().reset_index(drop=True).merge(self.movies, left_on='movieId', right_on='movieId')

    def item_based_recommendation(self, item, k=10, top_n=10):
        # get index of movie
        item_ix = self.user_item_matrix.columns.get_loc(item)
        # Use it to index the User similarity matrix
        item_sim = self.item_similarity[item_ix]
        # obtain the indices of the top k most similar users
        most_similar = self.user_item_matrix.columns[item_sim.argpartition(-(k+1))[-(k+1):]]
        return (most_similar.to_frame().reset_index(drop=True).merge(self.movies).head(top_n))

    def item_based_function(self, movie):

        interested_movie_id = self.getidfromtitle[movie]

        itemRec = classCollaborativeBased.item_based_recommendation(interested_movie_id) # Dataframe with Id and title
        rid = itemRec['movieId'].values # List of Movie Id
        rmovie = [self.gettitlefromid[movieid] for movieid in rid]  # List of movie name

        # getting the posters for the recommended movies
        backdrop = []
        genres = []
        time = []
        for movie_id in rid:
            # making API call for image
            responseImageinLoop = requests.get('https://api.themoviedb.org/3/movie/{}/images?api_key={}'.format(movie_id, self.api_key))
            data_json_image_in_loop = responseImageinLoop.json()
            print(data_json_image_in_loop)

            backdrop_image = data_json_image_in_loop['backdrops']
            if(backdrop_image == []):
                # print("EMPTY BACKDROP")
                isolang = []
                for data in data_json_image_in_loop['posters']:
                    iso = data['iso_639_1']
                    isolang.append(iso)
                # print(isolang)

                eng = 'en'
                if eng not in isolang:
                    #   print('POSTER NONE')
                    for data in data_json_image_in_loop['posters']:
                        language = data['iso_639_1']
                        if(language == None):
                            back_path = data['file_path']
                            break
                else:
                    #   print('POSTER EN')
                    for data in data_json_image_in_loop['posters']:
                        language = data['iso_639_1']
                        if(language == 'en'):
                            back_path = data['file_path']
                            break
                # path = data_json_image['posters'][0]['file_path']
            else:
                # print('NON EMPTY BACKDROP')
                isolang = []
                for data in data_json_image_in_loop['backdrops']:
                    iso = data['iso_639_1']
                    isolang.append(iso)
                # print(isolang)
                eng = 'en'
                if eng not in isolang:
                    #   print('BACKDROP NONE')
                    for data in data_json_image_in_loop['backdrops']:
                        language = data['iso_639_1']
                        if(language == None):
                            back_path = data['file_path']
                            break
                else:
                    #   print('BACKDROP EN')
                    for data in data_json_image_in_loop['backdrops']:
                        language = data['iso_639_1']
                        if(language == 'en'):
                            back_path = data['file_path']
                            break
                    # print(path)

            backdrop.append('https://image.tmdb.org/t/p/original{}'.format(back_path))

            response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, self.api_key))
            data_json = response.json()

            
            genreList = objectCommonFunction.ListOfGenres(data_json['genres'])
            genre = genreList.split(", ")
            genres.append(genre)

            
            runtime = objectCommonFunction.MinsToHours(data_json['runtime'])
            time.append(runtime)

        movie_cards = {backdrop[i]: [rmovie[i], genres[i], time[i]] for i in range(len(rmovie))}

        return (movie_cards)


    def user_based_function(self, userid):

        userRec = classCollaborativeBased.user_based_recommendation(userid) # Dataframe with Id and title
        rid = userRec['movieId'].values # List of Movie Id
        rmovie = [self.gettitlefromid[movieid] for movieid in rid]  # List of movie name

        # getting the posters for the recommended movies
        backdrop = []
        genres = []
        time = []
        for movie_id in rid:
            # making API call for image
            responseImageinLoop = requests.get('https://api.themoviedb.org/3/movie/{}/images?api_key={}'.format(movie_id, self.api_key))
            data_json_image_in_loop = responseImageinLoop.json()
            print(data_json_image_in_loop)

            backdrop_image = data_json_image_in_loop['backdrops']
            if(backdrop_image == []):
                # print("EMPTY BACKDROP")
                isolang = []
                for data in data_json_image_in_loop['posters']:
                    iso = data['iso_639_1']
                    isolang.append(iso)
                # print(isolang)

                eng = 'en'
                if eng not in isolang:
                    #   print('POSTER NONE')
                    for data in data_json_image_in_loop['posters']:
                        language = data['iso_639_1']
                        if(language == None):
                            back_path = data['file_path']
                            break
                else:
                    #   print('POSTER EN')
                    for data in data_json_image_in_loop['posters']:
                        language = data['iso_639_1']
                        if(language == 'en'):
                            back_path = data['file_path']
                            break
                # path = data_json_image['posters'][0]['file_path']
            else:
                # print('NON EMPTY BACKDROP')
                isolang = []
                for data in data_json_image_in_loop['backdrops']:
                    iso = data['iso_639_1']
                    isolang.append(iso)
                # print(isolang)
                eng = 'en'
                if eng not in isolang:
                    #   print('BACKDROP NONE')
                    for data in data_json_image_in_loop['backdrops']:
                        language = data['iso_639_1']
                        if(language == None):
                            back_path = data['file_path']
                            break
                else:
                    #   print('BACKDROP EN')
                    for data in data_json_image_in_loop['backdrops']:
                        language = data['iso_639_1']
                        if(language == 'en'):
                            back_path = data['file_path']
                            break
                    # print(path)

            backdrop.append('https://image.tmdb.org/t/p/original{}'.format(back_path))

            response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, self.api_key))
            data_json = response.json()

            
            genreList = objectCommonFunction.ListOfGenres(data_json['genres'])
            genre = genreList.split(", ")
            genres.append(genre)

            
            runtime = objectCommonFunction.MinsToHours(data_json['runtime'])
            time.append(runtime)

        movie_cards = {backdrop[i]: [rmovie[i], genres[i], time[i]] for i in range(len(rmovie))}

        return (movie_cards)


classCollaborativeBased = CollaborativeBasedClass()
