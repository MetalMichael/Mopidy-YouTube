from __future__ import unicode_literals

import logging
import pykka

from mopidy import backend

from . import translator
from . import session

import dateutil
from mopidy.models import Track, Artist, Album, SearchResult

logger = logging.getLogger(__name__)

class YoutubeLibraryProvider(backend.LibraryProvider):
    def __init__(self, config, *args, **kwargs):
        self.config = config;
        super(YoutubeLibraryProvider, self).__init__(*args, **kwargs)

    def lookup(self, uri):
        logger.info("Looking Up Youtube Video: " + uri)

        #Most important part. Location of the FLV
        url = translator.uriToVideo(uri)

        #Get the track info
        output = [session.lookup(self, uri, url)]
        
        return output
        
    def find_exact(self, query=None, uris=None):
        return self.search(query, uris)
        
    def search(self, query=None, uris=None, exact=False):
        if query is None:
            return SearchResult(uri='youtube:search')
    
        youtube_query = self._translate_search_query(query)
        logger.info('Youtube search query: %s' % youtube_query)

        future = pykka.ThreadingFuture()

        def callback(results, userdata=None):
            search_result = SearchResult(
                uri='youtube:search',
                tracks=[translator.to_mopidy_track(t, False, None) for t in results])
            future.set(search_result)

        session.search(self,
            youtube_query, callback,
            track_count=50)

        try:
            return future.get(timeout=self.backend.config['youtube']['timeout'])
        except pykka.Timeout:
            logger.info(
                'Timeout: YouTube search did not return in %ds',
                self.backend.config['youtube']['timeout'])
            return SearchResult(uri='youtube:search')

    def _get_all_tracks(self):
        return SearchResult(uri='youtube:search')

    def _translate_search_query(self, query):
        youtube_query = []
        fields = ''
        for (fields, values) in query.iteritems():
            if not values:
                raise LookupError('Missing query')
            for value in values:
                if not value:
                    raise LookupError('Missing query')
                youtube_query.append(value)
            break
        youtube_query = ' '.join(youtube_query)
        return youtube_query