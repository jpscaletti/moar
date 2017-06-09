# coding=utf-8


class Thumb(object):

    _engine = None

    def __init__(self, url='', key=None, fullpath=None):
        self.url = url
        self.key = key
        self.fullpath = fullpath

    def __nonzero__(self):
        return bool(self.url)

    def __bool__(self):
        return bool(self.url)

    def as_dict(self):
        return {
            'url': self.url,
            'key': self.key,
        }

    def __repr__(self):
        return self.url
