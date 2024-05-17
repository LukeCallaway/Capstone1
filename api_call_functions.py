import requests
from my_secrets import MY_API_KEY

base_url =  'https://api.watchmode.com/v1/'

def get_basic_info(search_value, search_type = None, search_field='name'):
    """get basic info of movie searching by actor name or movie title"""

    params = {'search_field': search_field, 'search_value': search_value, 'apiKey':  MY_API_KEY}
    full_url = base_url

    if search_type != None:
        full_url += search_type

    res = requests.get(full_url, params=params)

    return res.json()


    # for result in data['title_results']:
    #     print(result['name'], result['year'], result['type'], 'end of result')

    # data['title_results'][0] <- data['title_results'] gives arrary of results
    # title details page will be most request


# can only search api by id
def get_all_info(id):
    params = {'apiKey':  MY_API_KEY}
    full_url = base_url + f'title/{id}/details/'

    res = requests.get(full_url, params=params)
    return res.json()
