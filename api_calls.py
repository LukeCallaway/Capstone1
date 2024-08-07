import os
import requests
from random import randint
from dotenv import dotenv_values

from db import db, connect_db
from models.favorites import Favorites
from models.users import User

secrets = dotenv_values('.env')

MY_API_KEY = (os.environ.get('MY_API_KEY') or secrets['MY_API_KEY'])

base_url =  'https://api.watchmode.com/v1/'
genre_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 
22, 28, 29, 31, 32, 38, 39]

class Api_calls():

    @classmethod
    def get_basic_info(cls, search_value, search_type = 3, search_field='name'):
        """Get basic info of movie searching by movie title"""

        params = {'search_field': search_field, 'search_value': search_value, 'search_type': search_type,  'apiKey':  MY_API_KEY}

        full_url = base_url + 'autocomplete-search/'

        res = requests.get(full_url, params=params)

        return res.json()

    @classmethod
    def list_titles_by_genre(cls, genre, types = 'movie', sort_by = 'popularity_desc'):
        """API requests for a list of movie by 1 genre"""

        params = {'genres': genre, 'types': types, 'sort_by': sort_by, 'apiKey': MY_API_KEY}

        full_url = base_url + 'list-titles/'

        res = requests.get(full_url, params=params)

        return res.json()

    @classmethod # can only search api by id
    def get_all_info(cls, id): 
        """Gets all info for 1 movie by movie id"""

        params = {'apiKey':  MY_API_KEY}
        full_url = base_url + f'title/{id}/details/'

        res = requests.get(full_url, params=params)
        return res.json()

    @classmethod
    def is_on_list(cls, u_id, m_id, db):
        """Checks if a movie is already on a users list"""
        movie = (db.query.filter(db.user_id == u_id,
                                db.movie_id == m_id)
                                .first())
        if(movie):
            return True
        return False

    @classmethod
    def get_similar_titles(cls, lst):
        """Grabs all movies on a given list of ids"""
        sim_titles_info = {}
        i = 0
        for movie_id in lst:
            m = cls.get_all_info(movie_id)
            # make a dict with movieidx as key and movie info as values
            sim_titles_info[f'movie{i}'] = [m['id'], m['title'], m['year'], m['poster']]
            i += 1
        return sim_titles_info

    @classmethod
    def get_sim_to_favs(cls, lst):
        """Return list of similar movies from a list of ids"""
        fav_idx = randint(0, len(lst) - 1)
        fav = lst[fav_idx].movie_id
        fav = cls.get_all_info(fav)

        sim_list = fav['similar_titles']
        sim = randint(0, len(sim_list) - 1)
        sim = sim_list[sim]
        
        sim_info = cls.get_all_info(sim)

        return sim_info

    @classmethod
    def get_suggestions(cls, user_id):
        """
        Grab 3 similar titles from movies in favorites
        or 3 random titles from a genre
        """
        favorites = Favorites.get_all_favs(user_id)

        if len(favorites) > 2:
            
            return [cls.get_sim_to_favs(favorites) for i in range(3)]
            
        genre_int = randint(0, len(genre_ids) - 1 )
        genre = cls.list_titles_by_genre(genre_ids[genre_int])
        suggestions = []
        for movie in genre['titles'][:3]:
            res = cls.get_all_info(movie['id'])
            suggestions.append(res)

        return suggestions