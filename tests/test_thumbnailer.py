# coding=utf-8
from moar import Storage
from moar.thumbnailer import Thumbnailer, DEFAULTS, RESIZE_OPTIONS
import pytest

from .utils import RES_PATH, MockMethod


BASE_URL = 'http://media.example.com'


class MockStorage(object):

    def __init__(self):
        self.get_thumb = MockMethod(return_value={})
        self.get_key = MockMethod(return_value='key')
        self.get_source = MockMethod(return_value='path')
        self.save = MockMethod(return_value={})


class MockEngine(object):

    def __init__(self):
        self.open_image = MockMethod(return_value='im')
        self.close_image = MockMethod()
        self.get_size = MockMethod(return_value=(20, 10))
        self.get_data = MockMethod(return_value='data')
        self.set_orientation = MockMethod(return_value='im')
        self.set_geometry = MockMethod(return_value='im')
        self.apply_filters = MockMethod(return_value='im')


class MockThumb(object):
    pass


def test_new_thumbnailer():
    t = Thumbnailer(RES_PATH, BASE_URL)
    assert t.engine
    assert t.source_storage
    assert t.source_storage.base_path == RES_PATH
    assert t.source_storage.base_url == BASE_URL
    assert t.thumbs_storage
    assert t.thumbs_storage.base_path == RES_PATH
    assert t.thumbs_storage.base_url == BASE_URL


def test_parse_geometry():
    t = Thumbnailer(RES_PATH, BASE_URL)
    assert t.parse_geometry('200x140') == (200, 140)
    assert t.parse_geometry('100') == (100, None)
    assert t.parse_geometry('100x') == (100, None)
    assert t.parse_geometry('x50') == (None, 50)
    assert t.parse_geometry(None) is None
    assert t.parse_geometry(lambda: '20x10') == (20, 10)
    with pytest.raises(ValueError):
        assert t.parse_geometry('axb')


def test_get_key():
    sto = Storage(RES_PATH, BASE_URL)
    # t.get_key(path, geometry, filters, options)

    assert sto.get_key('qwertyuiop.jpg', None, [], {}) == sto.get_key('qwertyuiop.jpg', None, [], {})
    assert sto.get_key('abc.png', (100, 30), [], {}) == '8820aadc6048490c65d46c997d40c2aa'
    assert sto.get_key('abc.png', None, [], {}) == '88db0e707dc54b57a5e0c9e52699c6cd'
    assert sto.get_key('abc.png', None, [('rotate', 60)], {'format': 'JPEG'}) == \
        '2469c18428fe35fb2422bc94d7acff23'
    assert sto.get_key('abc.png', None, [], {'resize': 'fit'}) == 'cc88837caa4d797437decd01e187dde1'
    assert sto.get_key('abc.png', (100, 30), [], {'resize': 'fit'}) == 'a5fde43ca5ab38038805e7687b2c586e'


def test_options():
    t = Thumbnailer(RES_PATH, BASE_URL)
    for k, v in DEFAULTS.items():
        assert getattr(t, k) == v

    t = Thumbnailer(RES_PATH, BASE_URL, format='png')
    assert t.format == 'PNG'

    for r in RESIZE_OPTIONS:
        t = Thumbnailer(RES_PATH, BASE_URL, resize=r)
        assert t.resize == r

    t = Thumbnailer(RES_PATH, BASE_URL, resize='lalala')
    assert t.resize == DEFAULTS['resize']

    new_options = {
        'upscale': False,
        'quality': 80,
        'progressive': False,
        'orientation': False,
    }
    t = Thumbnailer(RES_PATH, BASE_URL, **new_options)
    for k, v in new_options.items():
        assert getattr(t, k) == v


def test_make_existing_thumb():
    ssto = MockStorage()
    tsto = MockStorage()
    mock_thumb = MockThumb()
    ssto.get_thumb = MockMethod(mock_thumb)

    e = MockEngine()
    t = Thumbnailer(RES_PATH, BASE_URL, source_storage=ssto, thumbs_storage=tsto, engine=e)
    path = 'abc.jpg'
    geometry = '20x10'
    filters = [('blur', 20)]
    options = {'format': 'PNG'}
    t(path, geometry, *filters, **options)

    assert not e.open_image.was_called
    assert not e.close_image.was_called
    assert not e.get_size.was_called
    assert not e.get_data.was_called
    assert not e.set_orientation.was_called
    assert not e.set_geometry.was_called
    assert not e.apply_filters.was_called
    assert not tsto.save.was_called
