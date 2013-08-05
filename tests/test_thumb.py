# -*- coding: utf-8 -*-
from moar.thumb import Thumb

from .utils import get_impath, RES_PATH


URL = 'http://example.com/media/qwertyuiop.jpg'
KEY = 'qwertyuiop'
PATH = 'abc/qwertyuiop.jpg'
FULLPATH = RES_PATH + PATH


def make_thumb(url=URL, key=KEY, width=None, height=None, fullpath=FULLPATH):
    return Thumb(url, key, width, height, fullpath)


def test_repr():
    t = make_thumb()
    assert str(t) == URL


def test_stored_width_and_height():
    t = make_thumb(width=120, height=150)
    assert t.width == 120
    assert t.height == 150
    assert t.as_dict() == {
        'url': URL,
        'fullpath': FULLPATH,
        'key': KEY,
        'width': 120,
        'height': 150,
    }


def test_get_size(engine):
    name = 'pil-crop50x90.png'
    fullpath = get_impath(name)
    t = make_thumb(fullpath=fullpath)
    t._engine = engine
    assert t.width == 50
    assert t.height == 90

    name = 'a200x140.jpg'
    fullpath = get_impath(name)
    t = make_thumb(fullpath=fullpath)
    t._engine = engine
    assert t.width == 200
    assert t.height == 140
