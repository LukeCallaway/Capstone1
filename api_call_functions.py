import requests
from my_secrets import MY_API_KEY

base_url =  'https://api.watchmode.com/v1/'

def get_basic_info(search_value, search_type = 3, search_field='name'):
    """get basic info of movie searching by actor name or movie title"""

    params = {'search_field': search_field, 'search_value': search_value, 'search_type': search_type,  'apiKey':  MY_API_KEY}

    full_url = base_url + 'autocomplete-search/'

    res = requests.get(full_url, params=params)

    return res.json()

# can only search api by id
def get_all_info(id):
    params = {'apiKey':  MY_API_KEY}
    full_url = base_url + f'title/{id}/details/'

    res = requests.get(full_url, params=params)
    return res.json()

def is_on_list(u_id, m_id, db):
    movie = (db.query.filter(db.user_id == u_id,
                                            db.movie_id == m_id)
                                            .all())
    if(len(movie) > 0):
        return True
    return False
