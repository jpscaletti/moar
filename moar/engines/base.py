# -*- coding: utf-8 -*-
"""
# moar.engines.base

Base engine

"""
import inspect
from math import ceil
import os

from .. import filters as available_filters


class BaseEngine(object):
    
    def process(self, thumb, custom_filters):
        options = thumb.options
        path = self.get_source_path(thumb.source)
        im = self.load_image(path)
        if im is None:
            return ''
        im = self.set_orientation(im, options)
        im = self.set_geometry(im, thumb.geometry, options)
        im = self.apply_filters(im, thumb.filters, custom_filters, options)
        data = self.get_data(im, options)
        self.close_image(im)
        return data
    
    def set_orientation(self, im, options):
        if options['orientation']:
            im = self._set_orientation(im)
        return im
        
    def set_geometry(self, im, geometry, options):
        """Rescale the image to the new geometry.
        """
        if not geometry:
            return im
        
        width, height = geometry
        if not width and not height:
            return im
        
        im_width, im_height = self._get_image_size(im)

        # Geometry match the current size?
        if (width is None) or (im_width == width):
            if (height is None) or (im_height == height):
                return im
        
        ratio = float(im_width) / im_height

        if width and height:
            # Smaller than the target?
            smaller = (im_width <= width) and (im_height <= height)
            if smaller and options['upscale'] == False:
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
            new_width = int(ceil(height * ratio))
            new_height = height
        else:
            new_width = width
            new_height = int(ceil(width / ratio))
        
        im = self._scale(im, new_width, new_height)
        return im
    
    def get_source_path(self, source):
        return source.path
    
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
    
    def load_image(self, path):
        raise NotImplementedError

    def close_image(self, im):
        pass
    
    def get_data(self, im, options):
        raise NotImplementedError
    
    def _set_orientation(self, im):
        return im

    def _get_image_size(self, im):
        raise NotImplementedError
    
    def _scale(self, im, width, height):
        raise NotImplementedError 

