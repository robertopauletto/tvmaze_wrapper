# tvmaze.py


try:
    import enum
    import requests
    import json
except ImportError as ie:
    print(f"Some modules are missing:\n{ie}")

__doc__ = """Python interface to the TV Maze API

This interface always returns JSON objects except for the convenience method
`get_show_and_episodes_short` which returns some info about shows and
episodes only such as:

- Show Name
- Number of seasons
- Episodes (each episode has)
    - Number
    - Title
    - Season show

Use `single_search()` if you are pretty sure of the name of the show you are
looking for (e.g. `single_search('buffy')`

Use `get_shows()` if you want to retrieve a number of possible 
matches to process to get the show you actually want, for example:

`get_shows('girls')` will gives you

000139 Girls
000525 Gilmore Girls
006771 The Powerpuff Girls
022131 Brown Girls
009136 Funny Girls
000722 The Golden Girls
021949 Kaiju Girls
000911 Some Girls
003418 ANZAC Girls
013826 Soldier Girls

"""
__version__ = '0.3'
__changelog__ = """
october 2018: Porting to Python3 (version 3.6 or above)
              Added methods to check the status of a show and 
              if the show is currently running
              Test cases rewritten
"""


class ImgType(enum.Enum):
    """Image format"""
    medium = 'medium'
    original = 'original'


# Routes
_routes = {
    'root': r'http://api.tvmaze.com/',
    'search': r'search/shows',
    'single_search': r'singlesearch/shows',
    'show_info': r'shows/',
    'show_episode_list': 'shows/%d/episodes'
}


class TVMazeException(Exception):
    """Custon exception"""
    pass


def _set_query(qtype):
    """
    Compose the REST url to request, according to `qtype`, returns None if
    `qtype` is not found

    :param qtype: key of route
    :return: the api url for the search specified by `qtype`
    """
    if qtype not in _routes:
        return None
    return f"{_routes['root']}{_routes[qtype]}"


def _get_data(url, payload=None):
    """
    Execute a REST request with `url` and optionals parameters

    :param url: the API url
    :param payload:
    :return: None or the JSON object from the request
    """
    if payload:
        r = requests.get(url, params=payload)
    else:
        r = requests.get(url)
    return r.json() if r else None


def find_shows(query):
    """(str) -> JSON or none

    From the TVMaze API docs: Search through all the shows in our database
    by the show's name. A fuzzy algorithm is used (with a fuzziness value of 2),
    meaning that shows will be found even if your query contains small typos.
    Results are returned in order of relevancy (best matches on top) and
    contain each show's full information

    """
    url = _set_query('search')
    payload = {'q': query}
    return _get_data(url, payload)


def single_search(query):
    """
    Performs a search for a show with query as name (forgiving typos).
    Use it if you are sure that the search for `query` will return only one
    show

    :param query:
    :return:
    """
    url = _set_query('single_search')
    payload = {'q': query}
    return _get_data(url, payload)


def get_shows(query):
    """
    Discards all the informations and returns a list of show ids and names.
    Useful if you want the user to choose a show in case of multiple
    occurrences

    :param query:
    :return: list of tuples with show id and name, empty list if nothing found
    """
    results = find_shows(query)
    if not results:
        return []
    return [(res['show']['id'], res['show']['name']) for res in results]


def get_show_id(query):
    """(str) -> int

    Returns the show id from a **single_search** query
    """
    show = single_search(query)
    return show['id'] if show else -1


def get_show_by_id(show_id):
    """Return info about the show with `show_id` (none if not found)"""
    url = _set_query('show_info') + str(show_id)
    show = _get_data(url)
    return show


def get_show_image(show_id, imgtype=ImgType.medium):
    """
    Get the image show url

    :param show_id:
    :param <ImgType> imgtype:
    :return: the raw response (just in case), the image url
    """
    show = get_show_by_id(show_id)
    url = show['image'][imgtype.name]
    response = requests.get(url, stream=True)
    return response.raw, url


def get_show_status(show_id):
    """
    Get the status of the show

    :param show_id:
    :return:
    """
    show = get_show_by_id(show_id)
    return show['status'] if show else None


def is_a_running_show(show_id):
    """
    Convenience method to check is the show is currently running
    :param show_id:
    :return: False if show ended or show **not found**
    """
    show = get_show_by_id(show_id)
    if not show:
        return False
    return show['status'].lower() == 'running'


def get_show_and_episodes_short(show_id, seasons=None):
    """
    Gets the episodes of the show with `show_id`

    :param show_id:
    :param seasons: a tuple with the season number for which we want episodes.
                    `None` or empty means we want all seasons
    :return: list of tuple with:
             - serie_id
             - serie name
             - list of dict with basic info for the episodes:
                 - name
                 - season
                 - episode number
             If `show_id` does not exists returns -1, None and an empty list
    """
    show = get_show_by_id(show_id)
    if not show:  # Could not found the show with id received!
        return -1, None, []
    url = _set_query('show_episode_list') % show_id
    req = _get_data(url)
    if not req:  # Something's wrong
        return -1, None, []
    result = []
    for ep in req:
        if seasons and ep['season'] not in seasons:
            continue
        result.append(
            {'name': ep['name'], 'number': ep['number'], 'season': ep['season']}
        )
    return show_id, show['name'], result


def get_number_of_seasons(show_id):
    """(int) -> int

    Returns the number of seasons for the show with id `show_id`
    """
    show_id, show_name, eps = get_show_and_episodes_short(show_id)
    if not eps:
        raise TVMazeException(f"Show id {show_id} not found")
    return max([item['season'] for item in eps])


