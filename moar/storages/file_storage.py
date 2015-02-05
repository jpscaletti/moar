# -*- coding: utf-8 -*-
"""
Local file system storage.

"""
import errno
import io
import os
from os.path import join, dirname, isfile, basename, splitext

from moar.thumb import Thumb
from moar.storages.base import BaseStorage


def make_dirs(path):
    try:
        os.makedirs(dirname(path))
    except (OSError) as e:
        if e.errno != errno.EEXIST:
            raise
    return path


class FileStorage(BaseStorage):

    def __init__(self, base_path, base_url='/', thumbsdir='t', out_path=None):
        self.base_path = base_path.rstrip('/')
        self.base_url = base_url.rstrip('/') or '/'
        self.thumbsdir = thumbsdir
        self.out_path = (out_path or self.base_path).rstrip('/')

    def get_source_path(self, path):
        """Returns the absolute path of the source image.
        Overwrite this to load the image from a place different than the
        filesystem into a temporal file.
        """
        return join(self.base_path, path)

    def get_thumb(self, path, key, format):
        thumbpath = self.get_thumbpath(path, key, format)
        fullpath = join(self.out_path, thumbpath)
        if isfile(fullpath):
            url = self.get_url(thumbpath)
            return Thumb(url, key, fullpath=fullpath)
        return None

    def save(self, path, key, format, data, w=None, h=None):
        thumbpath = self.get_thumbpath(path, key, format)
        fullpath = join(self.out_path, thumbpath)
        self.save_thumb(fullpath, data)
        url = self.get_url(thumbpath)
        thumb = Thumb(url, key, width=w, height=h, fullpath=fullpath)
        return thumb

    def save_thumb(self, fullpath, data):
        make_dirs(fullpath)
        with io.open(fullpath, 'wb') as f:
            f.write(data)

    def get_thumbpath(self, path, key, format):
        thumbsdir = self.get_thumbsdir(path)
        relpath = dirname(path)
        name, _ = splitext(basename(path))
        name = '%s.%s' % (name, format.lower())
        return join(relpath, thumbsdir, key, name)

    def get_thumbsdir(self, path):
        # Thumbsdir could be a callable
        # In that case, the path is built on the fly, based on the source path
        thumbsdir = self.thumbsdir
        if callable(self.thumbsdir):
            thumbsdir = self.thumbsdir(path)
        return thumbsdir

    def get_url(self, thumbpath):
        return join(self.base_url, thumbpath.strip('/'))
