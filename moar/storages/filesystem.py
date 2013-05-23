# -*- coding: utf-8 -*-
"""
# moar.storages.filesystem

Local file system store.

"""
import errno
import io
import os
from os.path import join, dirname, isfile, isdir


def make_dirs(path):
    try:
        os.makedirs(dirname(path))
    except (OSError) as e:
        if e.errno != errno.EEXIST:
            raise
    return path


class Storage(object):

    def __init__(self, base_path, base_url='', thumbsdir='t'):
        self.base_path = base_path.rstrip('/')
        self.base_url = base_url.rstrip('/')
        self.thumbsdir = thumbsdir

    def get(self, thumb):
        """"""
        name = self.get_name(thumb.key, thumb.options)
        fullpath = self.get_fullpath(thumb.source, name)
        if isfile(fullpath):
            return self.get_url(thumb.source, name)
        return None

    def save(self, thumb, raw_data):
        name = self.get_name(thumb.key, thumb.options)
        fullpath = self.get_fullpath(thumb.source, name)
        make_dirs(fullpath)
        with io.open(fullpath, 'wb') as f:
            f.write(raw_data)
        return self.get_url(thumb.source, name)

    def get_name(self, key, options):
        format = options['format'].lower()
        if format == 'jpeg':
            format = 'jpg'
        return '%s.%s' % (key, format)

    def get_thumbsdir(self, name):
        # Thumbsdir could be a callable
        # In that case, the path is built on the fly, based on the thumbs name
        thumbsdir = self.thumbsdir
        if callable(self.thumbsdir):
            thumbsdir = self.thumbsdir(name)
        return thumbsdir

    def get_fullpath(self, source, name):
        path = dirname(source.fullpath)
        thumbsdir = self.get_thumbsdir(name)
        return join(path, thumbsdir, name)

    def get_url(self, source, name):
        path = dirname(source.path).lstrip('/')
        thumbsdir = self.get_thumbsdir(name)
        return '/'.join([self.base_url, path, thumbsdir, name])
