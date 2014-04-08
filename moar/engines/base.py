# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import inspect
from math import ceil

from moar import filters as available_filters


class BaseEngine(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def open_image(self, fullpath):
        pass

    def close_image(self, im):
        pass

    @abstractmethod
    def get_size(self, im):
        pass

    @abstractmethod
    def get_data(self, im, options):
        pass

    @abstractmethod
    def scale(self, im, width, height):
        return im

    @abstractmethod
    def set_orientation(self, im):
        return im

    def set_geometry(self, im, geometry, options=None):
        """Rescale the image to the new geometry.
        """
        if not geometry:
            return im
        options = options or {}

        width, height = geometry
        if not width and not height:
            return im

        im_width, im_height = self.get_size(im)

        # Geometry match the current size?
        if (width is None) or (im_width == width):
            if (height is None) or (im_height == height):
                return im

        ratio = float(im_width) / im_height

        if width and height:
            # Smaller than the target?
            smaller = (im_width <= width) and (im_height <= height)
            if smaller and not options['upscale']:
                return im

            resize = options.get('resize', 'fill')
            if resize == 'fill':
                new_width = width
                new_height = int(ceil(width / ratio))
                if new_height < height:
                    new_height = height
                    new_width = int(ceil(height * ratio))
            elif resize == 'fit':
                new_width = int(ceil(height * ratio))
                new_height = height
                if new_width > width:
                    new_width = width
                    new_height = int(ceil(width / ratio))
            elif resize == 'stretch':
                new_width = width
                new_height = height

        elif height:
            # Smaller than the target?
            smaller = im_height <= height
            if smaller and not options['upscale']:
                return im

            new_width = int(ceil(height * ratio))
            new_height = height

        else:
            # Smaller than the target?
            smaller = im_width <= width
            if smaller and not options['upscale']:
                return im

            new_width = width
            new_height = int(ceil(width / ratio))

        im = self.scale(im, new_width, new_height)
        return im

    def apply_filters(self, im, filters, custom_filters, options):
        for f in filters:
            fname = f[0]
            args = f[1:]
            ff = self.get_filter(fname, custom_filters)
            im = ff(im, *args, **options)
        return im

    def get_filter(self, fn, custom_filters):
        f = custom_filters.get(fn)
        if f is None:
            f = getattr(available_filters, fn)
        if inspect.isclass(f):
            f = f()
        return getattr(f, self.name)
