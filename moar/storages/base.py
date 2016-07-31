# coding=utf-8
from abc import ABCMeta, abstractmethod
from hashlib import md5


class BaseStorage(object):

    __metaclass__ = ABCMeta

    def get_key(self, path, geometry, filters, options):
        """Generates the thumbnail's key from it's arguments.
        If the arguments doesn't change the key will not change
        """
        seed = u' '.join([
            str(path),
            str(geometry),
            str(filters),
            str(options),
        ]).encode('utf8')
        return md5(seed).hexdigest()

    @abstractmethod
    def get_source(self, path):
        """Returns the source image file descriptor.

        path:
            Path to the source image
        """

    @abstractmethod
    def get_thumb(self, path, key, format):
        """Get the stored thumbnail if exists.

        path:
            path of the source image
        key:
            key of the thumbnail
        format:
            thumbnail's file extension
        """

    @abstractmethod
    def save(self, path, key, format, data):
        """Save a newly generated thumbnail.

        path:
            path of the source image
        key:
            key of the thumbnail
        format:
            thumbnail's file extension
        data:
            thumbnail's binary data
        """
