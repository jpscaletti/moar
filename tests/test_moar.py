# -*- coding: utf-8 -*-
import os
import shutil
from moar import Thumbnailer

from .utils import get_impath, assert_image


def test_full(engine, tmpdir):
    base_path = str(tmpdir)
    base_url = 'http://media.example.com'
    t = Thumbnailer(base_path, base_url)
    path = 'images/a200x140.png'

    # Copy the source image to the test dir
    sourcepath = str(tmpdir.mkdir('images'))
    shutil.copy2(get_impath('a200x140.png'), sourcepath)

    thumb = t(path, '100x70', ('crop', 50, 50, 0, 0), ('rotate', 45), format='jpeg')

    assert str(thumb) == '/'.join([base_url, 'images/t', thumb.key, 'a200x140.jpeg'])
    assert thumb.fullpath == os.path.join(base_path, 'images', 't', thumb.key, 'a200x140.jpeg')
    ref = engine.name + '-full.jpeg'
    assert_image(thumb.fullpath, ref)

    thumb = t(path, '100x70', ('crop', 50, 50, 0, 0), ('rotate', 45), format='jpeg')
    assert thumb


def test_survive_invalid_source_image(engine, tmpdir):
    base_path = str(tmpdir)
    base_url = 'http://media.example.com'
    t = Thumbnailer(base_path, base_url)
    path = 'noimage.png'
    thumb = t(path, '100x70')
    assert thumb

    thumb = t(None, '100x70')
    assert thumb.url == ''
