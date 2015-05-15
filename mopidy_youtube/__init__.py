from __future__ import unicode_literals

import os

from mopidy import config, ext

__version__ = '0.0.2'
__url__ = 'https://github.com/MetalMichael/Mopidy-YouTube'

class Extension(ext.Extension):

    dist_name = 'Mopidy-YouTube'
    ext_name = 'youtube'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['bitrate'] = config.Integer()
        schema['timeout'] = config.Integer()
        schema['apikey'] = config.Secret()
        
        return schema

    def setup(self, registry):
        from .backend import YoutubeBackend
        registry.add('backend', YoutubeBackend)
