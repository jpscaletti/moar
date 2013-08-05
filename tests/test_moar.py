# -*- coding: utf-8 -*-
from moar import Thumbnailer

from .utils import RES_PATH, assert_image


BASE_URL = 'http://media.example.com'


def test_full(engine):
    t = Thumbnailer(RES_PATH, BASE_URL)
    path = 'a200x140.png'
    thumb = t(path, '100x70', ('crop', 50, 50, 0, 0), ('rotate', 45), format='jpeg')
    print(thumb.fullpath)
    out = engine.name + '-full.jpeg'

    assert_image(thumb.fullpath, out)
    assert str(thumb) == '/'.join([BASE_URL, 't', thumb.key + '.jpeg'])
