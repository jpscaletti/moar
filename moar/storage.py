# coding=utf-8
"""
Local file system storage.

"""
import errno
from hashlib import md5
import io
import os

from ._compat import urlopen
from .thumb import Thumb


def make_dirs(path):
    try:
        os.makedirs(os.path.dirname(path))
    except (OSError) as e:
        if e.errno != errno.EEXIST:
            raise
    return path


class Storage(object):

    def __init__(self, base_path, base_url='/', thumbsdir='t', out_path=None):
        self.base_path = base_path.rstrip('/')
        self.base_url = base_url.rstrip('/') or '/'
        self.thumbsdir = thumbsdir
        self.out_path = (out_path or self.base_path).rstrip('/')
        super(self.__class__, self).__init__()

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

    def get_source(self, path_or_url):
        """Returns the source image file descriptor.

        path_or_url:
            Path to the source image as an absolute path, a path relative
            to `self.base_path` or a URL beginning with `http[s]`

        """
        if path_or_url.startswith(('http://', 'https://')):
            try:
                return urlopen(path_or_url)
            except IOError:
                return None

        fullpath = path_or_url
        if not os.path.isabs(path_or_url):
            fullpath = os.path.join(self.base_path, path_or_url)
        try:
            return io.open(fullpath, 'rb')
        except IOError:
            return None

    def get_thumb(self, path, key, format):
        """Get the stored thumbnail if exists.

        path:
            path of the source image
        key:
            key of the thumbnail
        format:
            thumbnail's file extension
        """
        thumbpath = self.get_thumbpath(path, key, format)
        fullpath = os.path.join(self.out_path, thumbpath)
        if os.path.isfile(fullpath):
            url = self.get_url(thumbpath)
            return Thumb(url, key)
        return Thumb()

    def get_thumbpath(self, path, key, format):
        """Return the relative path of the thumbnail.

        path:
            path of the source image
        key:
            key of the thumbnail
        format:
            thumbnail file extension
        """
        relpath = os.path.dirname(path)
        thumbsdir = self.get_thumbsdir(path)
        name, _ = os.path.splitext(os.path.basename(path))
        name = '{}.{}.{}'.format(name, key, format.lower())
        return os.path.join(relpath, thumbsdir, name)

    def get_thumbsdir(self, path):
        """
        path:
            path of the source image
        """
        # Thumbsdir could be a callable
        # In that case, the path is built on the fly, based on the source path
        thumbsdir = self.thumbsdir
        if callable(self.thumbsdir):
            thumbsdir = self.thumbsdir(path)
        return thumbsdir

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
        thumbpath = self.get_thumbpath(path, key, format)
        fullpath = os.path.join(self.out_path, thumbpath)
        self.save_thumb(fullpath, data)
        url = self.get_url(thumbpath)
        thumb = Thumb(url, key, fullpath)
        return thumb

    def save_thumb(self, fullpath, data):
        make_dirs(fullpath)
        with io.open(fullpath, 'wb') as f:
            f.write(data)

    def get_url(self, thumbpath):
        return os.path.join(self.base_url, thumbpath.strip('/'))
