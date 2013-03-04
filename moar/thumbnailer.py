# -*- coding: utf-8 -*-
"""

"""
from hashlib import md5
import sys

from .engines.pil import Engine as PILEngine
from .engines.pil import available as pil_available
from .storages import filesystem
from .utils import StorageDict


INSTALL_PIL_MSG = '''Moar uses by default the Python Image Library (PIL) but
we couldn't found it installed.
Please see the documentation of Moar to find how to install it or how to choose
a different engine.'''

RESIZE_OPTIONS = ('fill', 'fit', 'stretch')


class Thumb(object):

    def __init__(self, source, geometry, filters, options):
        self.source = source
        self.geometry = geometry
        self.filters = filters
        self.options = options

        self.url = None
        self.key = self.get_key()
    
    def get_key(self):
        l = [str(self.source), str(self.geometry), str(self.filters),
            str(self.options)]
        seed = ' '.join(l)
        return md5(seed).hexdigest()
    
    def __repr__(self):
        return self.url


class Thumbnailer(object):
    """
    engine:
        An `Engine` class. By default `moar.engines.PILEngine`.
    
    storage:
        An `Storage` class. By default `moar.storages.filesystem.Storage`.
    
    filters:
        Dictionary of extra filters than are added to
        those available by default.
    
    upscale:
        A boolean that controls if the image can be upscaled or not.
        For example if your source is `100x100` and you request a thumbnail
        of size `200x200` and upscale is `False` this will return a
        thumbnail of size 100x100.
        If upscale were `True` this would result in a thumbnail size
        `200x200` (upscaled).
        The default value is `True`.

    quality:
        When the output format is jpeg, quality is a value between 0-100
        that controls the thumbnail write quality.
        Default value is `90`.

    progressive:
        This controls whether to save jpeg thumbnails as progressive jpegs.
        Default value is `True`.

    orientation:
        This controls whether to orientate the resulting thumbnail with
        respect to the source EXIF tags for orientation.
        Default value is `True`.

    format:
        This controls the write format and thumbnail extension. Formats 
        supported by the shipped engines are `'JPEG'` and `'PNG'`.
        Default value is `'JPEG'`.
    
    fit:
        A boolean that controls if the image is fitted in the given dimensions
        (even if doesn't match exactly the size) or if is expanded to cover
        Default value is `False`.

    resize:
        When setting the new geometry, this controls if the image is deformed
        to match exactly the given dimensions, regardless of the aspect ratio
        of the original image.
        This can be `fill`, `fit` or `upscale`.
        Default value is `fill`.
    """

    def __init__(self, engine=PILEngine, storage=None, filters=None, **default_options):
        if not pil_available and engine == PILEngine:
            print INSTALL_PIL_MSG
            sys.exit(1)
        if type(engine) == type:
            engine = engine()
        self.engine = engine

        if storage is None:
            storage = filesystem.Storage
        if type(storage) == type:
            storage = storage()
        self.storage = storage;
        
        self.custom_filters = filters or {}

        resize = default_options.get('resize', RESIZE_OPTIONS[0])
        if resize not in RESIZE_OPTIONS:
            resize = RESIZE_OPTIONS[0]

        self.upscale = bool(default_options.get('upscale', True))
        self.resize = resize
        self.format = default_options.get('format', 'JPEG').upper()
        self.quality = int(default_options.get('quality', 90))
        self.progressive = bool(default_options.get('progressive', True))
        self.orientation = bool(default_options.get('orientation', True))
    
    def parse_geometry(self, geometry):
        if not geometry:
            return
        
        if callable(geometry):
            geometry = geometry()
        
        geometry = geometry.split('x')

        if len(geometry) == 1:
            width = int(geometry[0])
            height = None
        else:
            w = geometry[0]
            width = int(w) if w else None
            height = int(geometry[1])
        
        return (width, height)
    
    def __call__(self, source, geometry=None, *filters, **options):
        filters = list(filters)
        
        if isinstance(source, dict):
            source = StorageDict(source)
        
        # No geometry provided
        if isinstance(geometry, (tuple, list)):
            filters.insert(0, geometry)
            geometry = None
        
        geometry = self.parse_geometry(geometry)

        resize = options.get('resize', self.resize)
        if resize not in RESIZE_OPTIONS:
            resize = self.resize
        
        _options = {
            'upscale': bool(options.get('upscale', self.upscale)),
            'resize': resize,
            'format': options.get('format', self.format).upper(),
            'quality': int(options.get('quality', self.quality)),
            'progressive': bool(options.get('progressive', self.progressive)),
            'orientation': bool(options.get('orientation', self.orientation)),
        }

        thumb = Thumb(source, geometry, filters, _options)
        url = self.storage.get(thumb)
        if url:
            thumb.url = url
            return thumb
        raw_data = self.engine.process(thumb, self.custom_filters)
        thumb.url = self.storage.save(thumb, raw_data)
        return thumb

