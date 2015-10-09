# -*- coding: utf-8 -*-
"""
Rackspace's CloudFiles storage.

"""
import errno
from io import BytesIO
import mimetypes
import os

from moar._compat import urlparse, url_quote
from moar.thumb import Thumb
from moar.storages.base import BaseStorage


def make_dirs(path):
    try:
        os.makedirs(os.path.dirname(path))
    except (OSError) as e:
        if e.errno != errno.EEXIST:
            raise
    return path


class RackspaceStorage(BaseStorage):

    def __init__(self, base_path, container):
        self.base_path = base_path.rstrip('/')
        self.container = container

    def get_source_path(self, path):
        """Returns the absolute path of the source image.
        Overwrite this to load the image from a place different than the
        filesystem into a temporal file.
        """
        fullpath = os.path.join(self.base_path, path)
        if not os.path.exists(fullpath):
            try:
                obj = self.container.get_object(path)
            except Exception:
                return None
            make_dirs(fullpath)
            obj.download(self.base_path, structure=True)
        return fullpath

    def get_thumb(self, path, key, format):
        thumbpath = self._get_thumbpath(path, key)
        try:
            obj = self.container.get_object(thumbpath)
        except Exception:
            return None
        fullpath = os.path.join(self.base_path, path)
        encoded_name = url_quote(obj.name)
        url = urlparse.urljoin(self.container.cdn_uri, encoded_name)
        return Thumb(url, key, fullpath=fullpath)

    def _get_thumbpath(self, path, key):
        head, tail = os.path.split(path)
        return os.path.join(head, key, tail)

    def save(self, path, key, format, data, w=None, h=None):
        thumbpath = self._get_thumbpath(path, key)
        content_type = mimetypes.guess_type(path)
        if content_type and content_type[0] and content_type[1]:
            content_type = '/'.join(content_type)
        else:
            content_type = None
        obj = self.container.upload_file(
            BytesIO(data),
            obj_name=thumbpath,
            content_type=content_type,
        )
        fullpath = os.path.join(self.base_path, path)
        encoded_name = url_quote(obj.name)
        url = urlparse.urljoin(self.container.cdn_uri, encoded_name)
        return Thumb(url, key, fullpath=fullpath)
