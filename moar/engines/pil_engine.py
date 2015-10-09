# -*- coding: utf-8 -*-
"""
Pillow based engine

"""
from io import BytesIO
from os.path import splitext

from moar.engines.base import BaseEngine
available = True
try:
    from PIL import Image, ImageFile
except ImportError:
    available = False


TOP_LEFT = 1
TOP_RIGHT = 2
BOTTOM_RIGHT = 3
BOTTOM_LEFT = 4
LEFT_TOP = 5
RIGHT_TOP = 6
RIGHT_BOTTOM = 7
LEFT_BOTTOM = 8


class PILEngine(BaseEngine):

    name = 'pil'
    available = available

    def open_image(self, path):
        try:
            im = Image.open(path)
        except IOError:
            return None
        return im

    def _save_to(self, im, path, format=None):
        """Save the image for testing.
        """
        format = format or im.format
        if not format:
            _, format = splitext(path)
            format = format[1:]
        im.save(path, format=format.upper())

    def get_size(self, im):
        return im.size

    def get_data(self, im, options=None):
        """Get the raw image data.
        """
        options = options or {}
        ImageFile.MAXBLOCK = 1024 * 1024
        buf = BytesIO()
        format = options.get('format', im.format)
        if format == 'JPG':
            format = 'JPEG'
        params = {
            'format': format,
            'quality': options.get('quality'),
        }
        if format == 'JPEG' and options.get('progressive'):
            params['progressive'] = True

        palletized = im.mode == 'P' and format != 'PNG'
        cmyk_jpeg = im.mode == 'CMYK' and format == 'JPEG'
        if palletized or cmyk_jpeg:
            im = im.convert('RGB')

        im.save(buf, **params)

        raw_data = buf.getvalue()
        buf.close()
        return raw_data

    def scale(self, im, width, height):
        return im.resize((width, height), resample=Image.ANTIALIAS)

    def set_orientation(self, im):
        """Orientate the resulting thumbnail with respect to the orientation
        EXIF tags (if available)."""
        try:
            exif = im._getexif()
        except AttributeError:
            exif = None
        if not exif:
            return im
        orientation = exif.get(0x0112)
        if not orientation or orientation == TOP_LEFT:
            return im
        if orientation == TOP_RIGHT:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == BOTTOM_RIGHT:
            im = im.rotate(180)
        elif orientation == BOTTOM_LEFT:
            im = im.transpose(Image.FLIP_TOP_BOTTOM)
        elif orientation == LEFT_TOP:
            im = im.rotate(-90).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == RIGHT_TOP:
            im = im.rotate(-90)
        elif orientation == RIGHT_BOTTOM:
            im = im.rotate(90).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == LEFT_BOTTOM:
            im = im.rotate(90)
        return im
