# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from hashlib import md5


class BaseStorage(object):

    __metaclass__ = ABCMeta

    def get_key(self, path, geometry, filters, options, timestamp):
        seed = u' '.join([
            str(path),
            str(geometry),
            str(filters),
            str(options),
            str(timestamp),
        ]).encode('utf8')
        return md5(seed).hexdigest()

    @abstractmethod
    def get_source(self, path):
        """Returns the opened source image file descriptor.
        """
        pass

    @abstractmethod
    def get_thumb(self, path, key, format):
        """Get the stored thumbnail if exists.
        """
        pass

    @abstractmethod
    def save(self, path, key, format, data, w=None, h=None):
        """Save a newly generated thumbnail.
        """
        pass
