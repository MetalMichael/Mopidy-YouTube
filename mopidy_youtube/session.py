from __future__ import unicode_literals

import logging
import time
import urllib
import pykka
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

logger = logging.getLogger('mopidy.backends.youtube')

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def search(context, query, callback, track_count):

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=context.config['youtube']['apikey'])
        
    search_response = youtube.search().list(
        q=query,
        part="snippet,id",
        maxResults=track_count,
        videoCategoryId="music",
        type="video"
      ).execute()
   
    videos = []
    videoIds = []
    
    for search_result in search_response.get("items", []):
        videoIds.append(search_result['id']['videoId'])

    video_response = youtube.videos().list(
        id = ",".join(videoIds),
        part='snippet,contentDetails'
    ).execute()
    
    for video_result in video_response.get("items", []):
        videos.append(video_result)
            
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