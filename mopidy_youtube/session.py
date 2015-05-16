from __future__ import unicode_literals

import logging
import time
import urllib
import pykka
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

from . import translator

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
def lookup(context, uri, url):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=context.config['youtube']['apikey'])
    
    youtubeId = translator.uriToId(uri)
    
    search_response = youtube.videos().list(
        id=youtubeId,
        part="snippet,contentDetails"
      ).execute()
    
    return translator.to_mopidy_track(search_response['items'][0], url);