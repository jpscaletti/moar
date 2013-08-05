# -*- coding: utf-8 -*-
"""
Local file system storage.

"""
import errno
import io
import os
from os.path import join, dirname, isfile, isdir

from moar.thumb import Thumb


def make_dirs(path):
    try:
        os.makedirs(dirname(path))
    except (OSError) as e:
        if e.errno != errno.EEXIST:
            raise
    return path


class FileStorage(object):

    def __init__(self, base_path, base_url='', thumbsdir='t'):
        self.base_path = base_path.rstrip('/')
        self.base_url = base_url.rstrip('/') or '/'
        self.thumbsdir = thumbsdir

    def get_thumb(self, path, key, format):
        name = '%s.%s' % (key, format)
        thumbpath = self.get_thumbpath(path, name)
        fullpath = join(self.base_path, thumbpath)
        if isfile(fullpath):
            url = self.get_url(thumbpath)
            return Thumb(url, key, fullpath=fullpath)
        return None

    def save(self, path, key, format, data, w=None, h=None):
        name = '%s.%s' % (key, format)
        thumbpath = self.get_thumbpath(path, name)
        fullpath = join(self.base_path, thumbpath)
        self.save_thumb(fullpath, data)
        url = self.get_url(thumbpath)
        thumb = Thumb(url, key, width=w, height=h, fullpath=fullpath)
        return thumb

    def save_thumb(self, fullpath, data):
        make_dirs(fullpath)
        with io.open(fullpath, 'wb') as f:
            f.write(data)

    def get_thumbpath(self, path, name):
        relpath = dirname(path)
        thumbsdir = self.get_thumbsdir(name)
        return join(relpath, thumbsdir, name)

    def get_thumbsdir(self, name):
        # Thumbsdir could be a callable
        # In that case, the path is built on the fly, based on the thumbs name
        thumbsdir = self.thumbsdir
        if callable(self.thumbsdir):
            thumbsdir = self.thumbsdir(name)
        return thumbsdir

    def get_url(self, thumbpath):
        return '/'.join([self.base_url, thumbpath.strip('/')])

