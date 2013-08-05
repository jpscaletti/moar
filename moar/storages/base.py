# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class BaseStorage(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_thumb(self, path, key, format):
        pass

    @abstractmethod
    def save(self, path, key, format, data, w=None, h=None):
        pass
