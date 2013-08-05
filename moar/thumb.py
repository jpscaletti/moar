# -*- coding: utf-8 -*-


class Thumb(object):

    _engine = None

    def __init__(self, url, key, width=None, height=None, fullpath=None):
        self.url = url
        self.key = key
        self.fullpath = fullpath
        self._width = width
        self._height = height

    @property
    def width(self):
        if self._width is None:
            self._set_size()
        return self._width

    @property
    def height(self):
        if self._height is None:
            self._set_size()
        return self._height

    def _set_size(self):
        im = self._engine.open_image(self.fullpath)
        self._width, self._height = self._engine.get_size(im)
        self._engine.close_image(im)

    def as_dict(self):
        return {
            'url': self.url,
            'key': self.key,
            'fullpath': self.fullpath,
            'width': self.width,
            'height': self.height,
        }

    def __repr__(self):
        return self.url
