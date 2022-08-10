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

class ContentBasedClass:

    def __init__(self):
        self.data = pickle.load(open('.\ContentBased\movies_2003.pkl', 'rb'))
        self.sim = pickle.load(open('.\ContentBased\similarity_2003.pkl', 'rb'))
        self.titles = self.data['title']
        self.ids = self.data['id']
        self.indices = pd.Series(self.data.index, index=self.data['title'])
        self.getidfromtitle = pd.Series(self.data['id'].values.tolist(), index=self.data['title'])
        self.gettitlefromid = pd.Series(self.data['title'].values.tolist(), index=self.data['id'])
        self.tmdb = TMDb()
        self.tmdb.api_key = '3deeb4c3065471557db144f8f3f78056'
        self.api_key = '3deeb4c3065471557db144f8f3f78056'

    def get_recommendations(self, title):

        idx = self.indices[title]

        # It will get the title with its index
        sim_scores = list(enumerate(self.sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]

        # [2502, 7535, 4702, 889, 437]
        movie_indices = [i[0] for i in sim_scores]

        recommended_movies_id = self.ids.iloc[movie_indices].values.tolist()

        return recommended_movies_id
    

    def content_based_function(self, movie):
        rid = classContentBased.get_recommendations(movie)  # List of movie id
        rmovie = [self.gettitlefromid[movieid] for movieid in rid]  # List of movie name

        movieUpper = movie.upper()
        tmdb_movie = Movie()
        result = tmdb_movie.search(movieUpper)

        # we are fetching movie id from its title
        original_movie_id = self.getidfromtitle[movie]

        # making API Call for Video
        responseVideo = requests.get('https://api.themoviedb.org/3/movie/{}/videos?api_key={}'.format(original_movie_id, self.api_key))
        data_json_video = responseVideo.json()
        for data in data_json_video['results']:
            officialvalue = data['official']
            typevalue = data['type']
            if(officialvalue == True and typevalue == 'Trailer'):
                keyvalue = data['key']
                # print(keyvalue)
                break
        
        #making API Call for Cast
        responseCast = requests.get('https://api.themoviedb.org/3/movie/{}/credits?api_key={}&language=en-US'.format(original_movie_id, self.api_key))
        data_json_cast = responseCast.json()

        cast_name = []
        cast_image = []
        for data in data_json_cast['cast'][:4]:
            name = data['original_name']
            image = data['profile_path']
            cast_name.append(name)
            cast_image.append('https://image.tmdb.org/t/p/original{}'.format(image))
        cast_cards = {cast_image[i]: cast_name[i] for i in range(len(cast_name))}

        # making API call for image
        responseImage = requests.get('https://api.themoviedb.org/3/movie/{}/images?api_key={}'.format(original_movie_id, self.api_key))
        data_json_image = responseImage.json()

        backdrop_image = data_json_image['backdrops']
        if(backdrop_image == []):
            path = data_json_image['posters'][0]['file_path']
        else:
            lang = []
            for data in data_json_image['backdrops']:
                iso = data['iso_639_1']
                lang.append(iso)

            eng = 'en'
            if eng not in lang:
                for data in data_json_image['backdrops']:
                    language = data['iso_639_1']
                    if(language == None):
                        path = data['file_path']
                        break
            else:
                for data in data_json_image['backdrops']:
                    language = data['iso_639_1']
                    if(language == 'en'):
                        path = data['file_path']
                        break

            # path = data_json_image['backdrops'][0]['file_path']
        img_path = 'https://image.tmdb.org/t/p/original{}'.format(path)

        # making API call for genre, runtime
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(original_movie_id, self.api_key))
        data_json = response.json()

        # getting list of genres form json (API)
        genreList = objectCommonFunction.ListOfGenres(data_json['genres'])
        genre = genreList.split(", ")

        # getting votes with comma as thousands separators
        vote_count = "{:,}".format(result[0].vote_count)

        # convert date to readable format (eg. 10-06-2019 to June 10 2019)
        rd = objectCommonFunction.date_convert(result[0].release_date)

        # convert minutes to hours minutes (eg. 148 minutes to 2 hours 28 mins)
        runtime = objectCommonFunction.MinsToHours(data_json['runtime'])


        # getting the posters for the recommended movies
        backdrop = []
        genres = []
        time = []
        for movie_id in rid:
            # making API call for image
            responseImageinLoop = requests.get('https://api.themoviedb.org/3/movie/{}/images?api_key={}'.format(movie_id, self.api_key))
            data_json_image_in_loop = responseImageinLoop.json()
            # print(data_json_image_in_loop)

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

        return (movie_cards, cast_cards, result[0], keyvalue, img_path, genre, vote_count, rd, runtime)

classContentBased = ContentBasedClass()


        


