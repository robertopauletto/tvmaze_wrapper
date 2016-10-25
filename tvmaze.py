#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

__doc__ = """Python interface to the TV Maze API

This interface returns always JSON objects exept for the convenience method
`get_episodes_short` which retrieves some info only about shows and episodes
such as

- Show Name
- Number of seasons
- Episodes (each episode has)
    - Number
    - Title
    - Season show

"""
__version__ = '0.1'

TVMAZE_API = {
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
    """(str) -> str

    Compose the REST url to request, according to `qtype`, returns None if
    `qtype` is not found
    """
    if qtype not in TVMAZE_API:
        return None
    return "%s%s" % (TVMAZE_API['root'], TVMAZE_API[qtype])


def _set_request(url, parms=None):
    """(str [,dict]) -> JSON string or None

    Execute a REST request with `url` and optionals parameters `parms`
    Returns None or the JSON object from the request
    """
    r = None
    if parms:
        r = requests.get(url, params=parms)
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
    parms = {'q': query}
    return _set_request(url, parms)


def single_search(query):
    """(str) -> JSON string or None

    Performs a search for a show with query as name (forgiving for typos)
    """
    url = _set_query('single_search')
    parms = {'q': query}
    return _set_request(url, parms)


def get_shows(query):
    """(str) -> list of tuples with show id and name

    Discards all the informations and returns a list of show ids and names.
    It's up to the caller to eventually pick a specific entry.

    Returns an empty list if nothing is found
    """
    results = find_shows(query)
    if not results:
        return []
    retval = []
    for result in results:
        retval.append((result['show']['id'], result['show']['name']))
    return retval


def get_show_id(query):
    """(str) -> int

    Returns the show id from a **single_search** query
    """
    show = single_search(query)
    return show['id'] if show else -1


def get_show(show_id):
    """Return info about the show with `show_id`"""
    url = _set_query('show_info') + str(show_id)
    show = _set_request(url)
    return show


def get_show_and_episodes_short(show_id, seasons=()):
    """(int [,seasons) -> (dict, list of dict)

    Returns basic info for the show (name) and episodes with `show_id` such as
    name, season number, episode number.

    `seasons` could be a tuple with the season number for which we want
    episodes.
    If `show_id` does not exists returns an empty list
    """
    show = get_show(show_id)
    if not show:
        return (None, [])
    url = _set_query('show_episode_list') % show_id
    r = _set_request(url)
    if not r:
        return []
    result = []
    for ep in r:
        if seasons and ep['season'] not in seasons:
            continue
        result.append(
            {'name': ep['name'], 'number': ep['number'], 'season': ep['season']}
        )
    return (show['name'], result)


def get_seasons_number(show_id):
    """(int) -> int

    Returns the number of season for the show with id `show_id`
    """
    show_name, eps = get_show_and_episodes_short(show_id)
    if not eps:
        raise TVMazeException("Show id %d not found" % show_id)
    return max([item['season'] for item in eps])


