# -*- coding: utf-8 -*-
from __future__ import absolute_import
"""
# moar.engines.mwand

Wand (a ctypes-based simple MagickWand API) engine.

"""
from __future__ import absolute_import

available = True
try:
    from wand.image import Image
except ImportError:
    available = False

from .base import BaseEngine


class Engine(BaseEngine):

    name = 'wand'

    def load_image(self, path):
        return Image(filename=path)
    
    def close_image(self, im):
        im.close()
    
    def get_data(self, im, options):
        format = options['format']
        im.format = format
        im.quality = options['quality']
        if format == 'JPEG' and options['progressive']:
            im.progressive = True
        return im.make_blob()
    
    def _set_orientation(self, im):
        ### Sadly, not implemented yet ###
        return im
        orientation = im.orientation()
        if orientation == OrientationType.TopRightOrientation:
            im.flop()
        elif orientation == OrientationType.BottomRightOrientation:
            im.rotate(180)
        elif orientation == OrientationType.BottomLeftOrientation:
            im.flip()
        elif orientation == OrientationType.LeftTopOrientation:
            im.rotate(90)
            im.flop()
        elif orientation == OrientationType.RightTopOrientation:
            im.rotate(90)
        elif orientation == OrientationType.RightBottomOrientation:
            im.rotate(-90)
            im.flop()
        elif orientation == OrientationType.LeftBottomOrientation:
            im.rotate(-90)
        im.orientation(OrientationType.TopLeftOrientation)
        return im

    def _get_image_size(self, im):
        return im.size
    
    def _scale(self, im, width, height):
        im.resize(width, height)
        return im

