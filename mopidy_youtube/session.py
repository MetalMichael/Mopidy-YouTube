from __future__ import unicode_literals

import logging
import time
import urllib
import requests
import pykka
import json

logger = logging.getLogger('mopidy.backends.youtube')

YOUTUBE_API_URL = "http://gdata.youtube.com/feeds/api/videos"

def search(query, callback, track_count):
    tracks = make_request(YOUTUBE_API_URL,
                  {'alt': 'json', 'q': query, 'max-results': track_count, 'category': 'music'})
    videos = []
    try:
        tracks = json.loads(tracks.text)
    except ValueError:
        logger.error('YoutubeBackend Error: ' + tracks.text)
        return false
    if "entry" in tracks["feed"]:
        for track in tracks["feed"]["entry"]:
            videos.append({'title': track["title"]["$t"],
                        'id': track["id"]["$t"],
                        'date': track["published"]["$t"],
                        'length': track["media$group"]["yt$duration"]["seconds"],
                        'uploader': track["author"][0]
            })
    callback(videos)

#def lookup(query, callback):
def lookup(query):   
    track = make_request(query, {'alt': 'json'})
    try:
        track = json.loads(track.text)
    except ValueError:
        logger.error('YoutubeBackend Error: ' + track.text)
        return False
    trackInfo = track["entry"]
    
    return {'title': trackInfo ["title"]["$t"],
        'id': trackInfo["id"]["$t"],
        'date': trackInfo["published"]["$t"],
        'length': trackInfo["media$group"]["yt$duration"]["seconds"],
        'uploader': {'name': trackInfo["author"][0]["name"]["$t"], 'uri': trackInfo["author"][0]["uri"]["$t"]}
    }

def make_request(url, parameters):
    try:
         r = requests.get(url, params = parameters)
    except (ConnectionError, Timeout):
        logger.error('YoutubeBackend Error: Cannot connect to ' + url)
        return false
    except HTTPError:
        logger.error('YoutubeBackend Error: HTTP error')
        return false
    return r