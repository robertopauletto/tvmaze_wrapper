#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """Wrapper interface to the TV Maze API
"""

import requests
import json


TVMAZE_API = {
    'root': r'http://api.tvmaze.com/',
    'single_search': r'singlesearch/shows',
    'show_info': r'shows',
    'show_episode_list': 'shows/%d/episodes'
}

class TVMazeException(Exception):
    pass

def _set_query(qtype):
    """(str) -> str

    Return the type of REST url to request
    """
    if qtype not in TVMAZE_API:
        return None
    return "%s%s" % (TVMAZE_API['root'], TVMAZE_API[qtype])

def _set_request(url, parms=None):
    """(str [,dict]

    Execute a REST request with `url` and optionals parameters `parms`
    Returns None or the JSON object from the request
    """
    r = None
    if parms:
        r = requests.get(url, params=parms)
    else:
        r = requests.get(url)
    return r.json() if r else None

def single_search(query):
    """(str) -> json or None

    Performs a search for a show with query as name (forgiving for typos)
    """
    url = _set_query('single_search')
    parms = {'q': query}
    return _set_request(url, parms)

def get_show_id(query):
    """(str) -> id

    Returns the show id from a **single_search** query
    """
    show = single_search(query)
    return show['id'] if show else -1

def get_episodes(show_id, seasons=()):
    """(int [,seasons) -> list of dict

    Returns basic episode info for the show with `show_id` such as name,
    season number, episode number.
    `seasons` could be a tuple with the season number for which we want
    episodes.
    If `show_id` does not exists returns an empty list
    """
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
    return result

def get_total_seasons(show_id):
    eps = get_episodes(show_id)
    if not eps:
        raise TVMazeException("Show id %d not found" % show_id)
    x = max([item['season'] for item in eps])
    return x
