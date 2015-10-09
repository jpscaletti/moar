# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from hashlib import md5
from os.path import getmtime


class BaseStorage(object):

    __metaclass__ = ABCMeta

    def __init__(self, base_path):
        self.base_path = base_path.rstrip('/')

    def get_key(self, path, geometry, filters, options, timestamp=None):
        timestamp = timestamp or self.get_timestamp(path)
        seed = u' '.join([
            str(path),
            str(geometry),
            str(filters),
            str(options),
            str(timestamp),
        ]).encode('utf8')
        return md5(seed).hexdigest()

    def get_timestamp(self, path):
        fullpath = self.get_source_path(path)
        try:
            return getmtime(fullpath)
        except OSError:
            return 0

    @abstractmethod
    def get_source_path(self, path):
        """Returns the absolute path of the source image.
        Overwrite this to load the image from a place different than the
        filesystem into a temporal file.
        """
        pass

    @abstractmethod
    def get_thumb(self, path, key, format):
        pass

    @abstractmethod
    def save(self, path, key, format, data, w=None, h=None):
        pass
