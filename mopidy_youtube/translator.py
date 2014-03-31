from __future__ import unicode_literals

import dateutil.parser
import subprocess
import sys
import re
import logging

from mopidy.models import Track, Artist, Album

logger = logging.getLogger(__name__)

track_cache = {}
artist_cache = {}

def to_mopidy_track(youtube_track):
    if youtube_track is None:
        return
    uri = str(youtube_track['id'])
    if uri in track_cache:
        return track_cache[uri]
    date = youtube_track['date']
    artist = to_mopidy_artist(youtube_track['uploader'])
    track_cache[uri] = Track(
        uri=uri,
        name=youtube_track['title'],
        artists=[artist],
        album=dummy_mopidy_album(artist, date),
        track_no=0,
        date=dateutil.parser.parse(youtube_track['date']),
        length=int(youtube_track['length'])*1000,
        bitrate=320)
    return track_cache[uri]

def to_mopidy_artist(artist):
    if artist is None:
        return
    uri = str(artist['uri']['$t'])
    if uri in artist_cache:
        return artist_cache[uri]
    artist_cache[uri] = Artist(uri=uri, name=artist['name']['$t'])
    return artist_cache[uri]

def dummy_mopidy_album(artist, date):
    return Album(
        uri='',
        name='n/a',
        artists=[artist],
        date=date)

def uriToVideo(uri):
    # http://gdata.youtube.com/feeds/api/videos/Nh2xYpwe4ws
    idgroup = re.search("videos\/(.+)", uri)
    if idgroup is None:
        print "Couldn't match Regex: " + uri
        return []
    id = idgroup.group(1)
    url = subprocess.Popen(["/home/soc_lsucs/Documents/youtube-dl/youtube-dl", "-g", "http://www.youtube.com/watch?v=" + id], stdout=subprocess.PIPE)
    flvlocation = url.communicate()[0].strip()

    logger.info("Youtube-dl returned location of VideoID: " + id)
    logger.debug("Youtube-dl returned location of VideoID: " + id + " URL: " + flvlocation)

    return flvlocation
