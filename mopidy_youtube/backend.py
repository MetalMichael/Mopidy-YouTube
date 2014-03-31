from __future__ import unicode_literals

import logging
import pykka

from mopidy import backend

from mopidy_youtube.library import YoutubeLibraryProvider

logger = logging.getLogger(__name__)


class YoutubeBackend(pykka.ThreadingActor, backend.Backend):
    def __init__(self, config, audio):
        super(YoutubeBackend, self).__init__()

        self.config = config
        
        self.library = YoutubeLibraryProvider(backend=self)
        self.playback = backend.PlaybackProvider(audio=audio, backend=self)

        self.uri_schemes = ['http']