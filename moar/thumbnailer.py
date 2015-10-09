# -*- coding: utf-8 -*-
from __future__ import print_function

from os.path import join as pjoin
from os.path import splitext, exists

from moar._compat import string_types
from moar.engines.pil_engine import PILEngine
from moar.storages.file_storage import FileStorage
from moar.thumb import Thumb


INSTALL_PIL_MSG_OR_CHANGE_ENGINE = '''Moar uses by default the Python Image Library (PIL) but we couldn't found it installed.
Please see the documentation of Moar to find how to install it or how to choose a different engine.'''

NO_STORAGE_FOUND = '''
No storage was defined.
'''

RESIZE_OPTIONS = ('fill', 'fit', 'stretch')

DEFAULTS = {
    'resize': 'fill',
    'upscale': True,
    'format': None,
    'quality': 90,
    'progressive': True,
    'orientation': True,
}


class Thumbnailer(object):

    """
    engine:
        An `Engine` class. By default `moar.PILEngine`.

    storage:
        An `Storage` class. By default `moar.FileStorage`.

    filters:
        Dictionary of custom extra filters than are added to
        those available by default.

    resize:
        When setting the new geometry, this controls if the image is deformed
        to match exactly the given dimensions, regardless of the aspect ratio
        of the original image.
        This can be `fill`, `fit` or `upscale`.
        Default value is `fill`.

    upscale:
        A boolean that controls if the image can be upscaled or not.
        For example if your source is `100x100` and you request a thumbnail
        of size `200x200` and upscale is `False` this will return a
        thumbnail of size 100x100.
        If upscale were `True` this would result in a thumbnail size
        `200x200` (upscaled).
        The default value is `True`.

    format:
        This controls the write format and thumbnail extension. Formats
        supported by the shipped engines are `'JPEG'` and `'PNG'`.
        Default value is `'JPEG'`.

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

    """

    def __init__(self, base_path=None, base_url='/', storage=None,
                 engine=PILEngine, filters=None, echo=False, **options):
        self.base_path = base_path
        self.set_storage(base_path, base_url, storage)
        self.set_engine(engine)
        self.custom_filters = filters or {}
        self.echo = echo
        self.set_default_options(options)

    def set_storage(self, base_path, base_url, storage):
        if storage is None:
            if not base_url:
                raise ValueError(NO_STORAGE_FOUND)
            storage = FileStorage(base_path, base_url)
        if isinstance(storage, type):
            storage = storage()
        self.storage = storage

    def set_engine(self, engine):
        if engine == PILEngine and not PILEngine.available:
            raise ImportError(INSTALL_PIL_MSG_OR_CHANGE_ENGINE)
        if isinstance(engine, type):
            engine = engine()
        self.engine = engine

    def set_default_options(self, options):
        resize = options.get('resize', DEFAULTS['resize'])
        if resize not in RESIZE_OPTIONS:
            resize = DEFAULTS['resize']
        format = options.get('format', DEFAULTS['format'])
        if format:
            format = format.upper()
            if format == 'JPG':
                format = 'JPEG'

        self.resize = resize
        self.upscale = bool(options.get('upscale', DEFAULTS['upscale']))
        self.format = format
        self.quality = int(options.get('quality', DEFAULTS['quality']))
        self.progressive = bool(options.get('progressive', DEFAULTS['progressive']))
        self.orientation = bool(options.get('orientation', DEFAULTS['orientation']))

    def __call__(self, path, geometry=None, *filters, **options):
        path = self.parse_path(path)
        if not path:
            return Thumb('', None)
        filters = list(filters)

        # No geometry provided
        if isinstance(geometry, (tuple, list)):
            filters.insert(0, geometry)
            geometry = None
        else:
            geometry = self.parse_geometry(geometry)

        options = self.parse_options(path, options)

        key = self.storage.get_key(path, geometry, filters, options)
        thumb = self.storage.get_thumb(path, key, options['format'])
        if thumb:
            thumb._engine = self.engine
            if self.echo:
                print(' ', thumb.url.strip('/'))
            return thumb

        fullpath = self.storage.get_source_path(path)
        if not exists(fullpath):
            return Thumb('', None)

        im = self.engine.open_image(fullpath)
        if im is None:
            return Thumb('', None)
        data, w, h = self.process_image(im, geometry, filters, options)
        thumb = self.storage.save(path, key, options['format'], data, w, h)
        if self.echo:
            print(' ', thumb.url.strip('/'))
        return thumb

    def parse_path(self, path):
        """Parse the path argument maintaining backwards compatibility.
        """
        if not path:
            return None
        if isinstance(path, string_types):
            return path

        if hasattr(path, 'path'):
            return getattr(path, 'path')
        if hasattr(path, 'relpath') and hasattr(path, 'name'):
            return pjoin(getattr(path, 'relpath').strip('/'), getattr(path, 'name'))

        if 'path' in path:
            return path['path']
        if 'relpath' in path and 'name' in path:
            return pjoin(path['relpath'].strip('/'), path['name'])

        return None

    def parse_geometry(self, geometry):
        """Parse a geometry string and returns a (width, height) tuple
        Eg:
            '100x200' ==> (100, 200)
            '50' ==> (50, None)
            '50x' ==> (50, None)
            'x100' ==> (None, 100)
            None ==> None

        A callable `geometry` parameter is also supported.
        """
        if not geometry:
            return
        if callable(geometry):
            geometry = geometry()
        geometry = geometry.split('x')
        if len(geometry) == 1 or (len(geometry) > 1 and not geometry[1]):
            width = int(geometry[0])
            height = None
        else:
            w = geometry[0]
            width = int(w) if w else None
            height = int(geometry[1])
        return (width, height)

    def parse_options(self, path, options):
        resize = options.get('resize', self.resize)
        if resize not in RESIZE_OPTIONS:
            resize = self.resize

        return {
            'upscale': bool(options.get('upscale', self.upscale)),
            'resize': resize,
            'format': self.get_format(path, options),
            'quality': int(options.get('quality', self.quality)),
            'progressive': bool(options.get('progressive', self.progressive)),
            'orientation': bool(options.get('orientation', self.orientation)),
        }
        return options

    def get_format(self, path, options):
        format = options.get('format', self.format)
        if not format:
            _, ext = splitext(path)
            if ext:
                format = ext[1:].upper()
        format = format or 'JPEG'
        format = format.upper()
        if format == 'JPG':
            format = 'JPEG'
        return format

    def process_image(self, im, geometry, filters, options):
        eng = self.engine
        if options.get('orientation'):
            im = eng.set_orientation(im)
        im = eng.set_geometry(im, geometry, options)
        im = eng.apply_filters(im, filters, self.custom_filters, options)
        data = eng.get_data(im, options)
        w, h = eng.get_size(im)
        eng.close_image(im)
        return data, w, h
