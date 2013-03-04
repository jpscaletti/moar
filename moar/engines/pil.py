# -*- coding: utf-8 -*-
from __future__ import absolute_import
"""
# moar.engines.pil

PIL engine.

"""
from os.path import dirname, join
from StringIO import StringIO

available = True
try:
    from PIL import Image, ImageFile
except ImportError:
    available = False

from .base import BaseEngine


class Engine(BaseEngine):

    name = 'pil'
    
    def load_image(self, path):
        try:
            im = Image.open(path)
        except IOError:
            return None
        return im
    
    def get_data(self, im, options):
        ImageFile.MAXBLOCK = 1024 * 1024
        buf = StringIO()
        format = options['format']
        params = {
            'format': format,
            'quality': options['quality'],
        }
        if format == 'JPG' and options['progressive']:
            params['progressive'] = True

        palletized = im.mode == 'P' and format != 'PNG'
        cmyk_jpeg = im.mode == 'CMYK' and format == 'JPEG'
        if palletized or cmyk_jpeg:
            im = im.convert('RGB')
        
        im.save(buf, **params)
        raw_data = buf.getvalue()
        buf.close()
        return raw_data
    
    def _set_orientation(self, im):
        """Orientate the resulting thumbnail with respect to the orientation
        EXIF tags (if available)."""
        try:
            exif = im._getexif()
        except AttributeError:
            exif = None
        if exif:
            orientation = exif.get(0x0112)
            if orientation == 2:
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                im = im.rotate(180)
            elif orientation == 4:
                im = im.transpose(Image.FLIP_TOP_BOTTOM)
            elif orientation == 5:
                im = im.rotate(-90).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                im = im.rotate(-90)
            elif orientation == 7:
                im = im.rotate(90).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                im = im.rotate(90)
        return im
    
    def _get_image_size(self, im):
        return im.size
    
    def _scale(self, im, width, height):
        return im.resize((width, height), resample=Image.ANTIALIAS)

