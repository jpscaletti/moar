# coding=utf-8
"""
Wand based engine.
Wand is a ctypes-based simple MagickWand API (http://docs.wand-py.org/).

"""
from os.path import splitext

from .base import BaseEngine
from moar._compat import string_types

from wand import image


class WandEngine(BaseEngine):

    def open_image(self, path_or_stream):
        if not path_or_stream:
            return None
        if isinstance(path_or_stream, string_types):
            opts = {'filename': path_or_stream}
        else:
            opts = {'file': path_or_stream}
        try:
            im = image.Image(**opts)
        except Exception:
            return None
        return im

    def close_image(self, im):
        im.close()

    def _save_to(self, im, path, format=None):
        """Save the image for testing.
        """
        format = format or im.format
        if not format:
            _, format = splitext(path)
            format = format[1:]
        im.format = format.lower()
        im.save(filename=path)

    def get_size(self, im):
        return im.size

    def get_data(self, im, options=None):
        options = options or {}
        format = options.get('format', im.format)
        im.format = format
        quality = options.get('quality')
        if quality:
            im.compression_quality = quality
        if format == 'JPEG' and options.get('progressive'):
            im.progressive = True
        return im.make_blob()

    def scale(self, im, width, height):
        im.resize(width, height)
        return im

    def set_orientation(self, im):
        orientation = im.orientation
        if not orientation or orientation == 'top_left':
            return im
        if orientation == 'top_right':
            im.flop()
        elif orientation == 'bottom_right':
            im.rotate(180)
        elif orientation == 'bottom_left':
            im.flip()
        elif orientation == 'left_top':
            im.rotate(90)
            im.flop()
        elif orientation == 'right_top':
            im.rotate(90)
        elif orientation == 'right_bottom':
            im.rotate(-90)
            im.flop()
        elif orientation == 'left_bottom':
            im.rotate(-90)
        return im
