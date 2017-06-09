# coding=utf-8
from __future__ import print_function

import inspect
import os

from .engines.wand_engine import WandEngine
from .storage import Storage
from .thumb import Thumb
from .optimage import optimage


RESIZE_OPTIONS = ('fill', 'fit', 'stretch')

DEFAULTS = {
    'resize': 'fill',
    'upscale': True,
    'format': None,
    'quality': 90,
    'progressive': True,
    'orientation': True,
    'optimize': False,
}


class Thumbnailer(object):

    """
    base_path:
        Optional. Used as argument for the storage (`moar.Storage`)

    base_url:
        Optional. Used as argument for the storage (`moar.Storage`)

    engine:
        An `Engine` class. By default `moar.WandEngine`.

    filters:
        Dictionary of custom extra filters than are added to
        those available by default.

    echo:
        Be verbose

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

    optimize:
        Run jpegtran and jpegoptim or pngcrush and optipng trying
        to get a smaller size file.
        Default value is `False`.

    """

    def __init__(self,
                 base_path='.', base_url='/',
                 source_storage=None, thumbs_storage=None,
                 engine=WandEngine, filters=None, echo=False, **options):
        self.source_storage = source_storage or Storage(base_path, base_url)
        self.thumbs_storage = thumbs_storage or Storage(base_path, base_url)
        if inspect.isclass(engine):
            engine = engine()
        self.engine = engine
        self.custom_filters = filters or {}
        self.echo = echo
        self.set_default_options(options)

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
        self.optimize = bool(options.get('optimize', DEFAULTS['optimize']))

    def __call__(self, path, geometry=None, *filters, **options):
        if not path:
            return Thumb()
        filters = list(filters)

        # No geometry provided
        if isinstance(geometry, (tuple, list)):
            filters.insert(0, geometry)
            geometry = None
        else:
            geometry = self.parse_geometry(geometry)

        options = self.parse_options(path, options)

        key = self.source_storage.get_key(path, geometry, filters, options)
        thumb = self.source_storage.get_thumb(path, key, options['format'])
        if thumb:
            thumb._engine = self.engine
            if self.echo:
                print(' ', thumb.url.strip('/'))
            return thumb

        fd = self.source_storage.get_source(path)
        if not fd:
            return Thumb()
        im = self.engine.open_image(fd)
        if im is None:
            return Thumb()
        data = self.process_image(im, geometry, filters, options)
        self.engine.close_image(im)

        thumb = self.thumbs_storage.save(path, key, options['format'], data)
        if self.echo:
            print(' ', thumb.url.strip('/'))
        if options['optimize']:
            optimage(thumb.fullpath)
        return thumb

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
            'optimize': bool(options.get('optimize', self.optimize)),
        }
        return options

    def get_format(self, path, options):
        format = options.get('format', self.format)
        if not format:
            _, ext = os.path.splitext(path)
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
        return eng.get_data(im, options)
