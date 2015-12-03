from __future__ import unicode_literals

import re
from setuptools import setup, find_packages


def get_version(filename):
    content = open(filename).read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", content))
    return metadata['version']


setup(
    name='Mopidy-YouTube',
    version=get_version('mopidy_youtube/__init__.py'),
    url='https://github.com/MetalMichael/Mopidy-YouTube',
    license='Apache License, Version 2.0',
    author='Michael Fiford',
    author_email='michaelfiford@gmail.com',
    description='Mopidy extension that serves songs from YouTube',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'apiclient',
        'urllib3',
        'google-api-python-client',
        'iso8601',
        'isodate',
        'Mopidy >= 0.18',
        'Pykka >= 1.1',
        'python-dateutil',
        'httplib2 >= 0.9.1',
        'youtube-dl'
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'mock >= 1.0',
    ],
    entry_points={
        'mopidy.ext': [
            'youtube = mopidy_youtube:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
