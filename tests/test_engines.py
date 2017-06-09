# coding=utf-8
from os.path import join

import moar
from PIL import Image
import pytest

from .utils import get_impath, almost_equal, assert_size, tmpdir, assert_image


def test_open_close_image(engine):
    impath = get_impath()
    im = engine.open_image(impath)
    assert im
    assert engine.get_data(im)
    engine.close_image(im)


def test_get_size(engine):
    impath = get_impath()
    im = engine.open_image(impath)
    w, h = engine.get_size(im)
    assert w == 200
    assert h == 140
    engine.close_image(im)


def test_orientation(engine, tmpdir):
    test_images = [
        '1_topleft.jpg',
        '2_topright.jpg',
        '3_bottomright.jpg',
        '4_bottomleft.jpg',
        '5_lefttop.jpg',
        '6_righttop.jpg',
        '7_rightbottom.jpg',
        '8_leftbottom.jpg',
    ]
    for name in test_images:
        impath = get_impath(name)
        im = engine.open_image(impath)
        im = engine.set_orientation(im)
        tmp = join(str(tmpdir), name)
        engine._save_to(im, tmp, 'png')

        im = Image.open(tmp)
        assert almost_equal(im.getpixel((5, 15)), 85)  # grey
        assert almost_equal(im.getpixel((25, 15)), 168)  # light grey
        assert almost_equal(im.getpixel((15, 25)), 0)  # black
        engine.close_image(im)


def test_geometry_w(engine, tmpdir):
    name = 'a200x140.png'
    impath = get_impath(name)
    im = engine.open_image(impath)
    im = engine.set_geometry(im, (100, None))

    tmp = join(str(tmpdir), name)
    engine._save_to(im, tmp, 'png')
    assert_size(tmp, width=100, height=70)
    engine.close_image(im)


def test_geometry_h(engine, tmpdir):
    name = 'b94x200.png'
    impath = get_impath(name)
    im = engine.open_image(impath)
    im = engine.set_geometry(im, (None, 100))

    tmp = join(str(tmpdir), name)
    engine._save_to(im, tmp, 'png')
    assert_size(tmp, width=47, height=100)
    engine.close_image(im)


def test_geometry_wh_landscape(engine, tmpdir):
    name = 'a200x140.png'
    impath = get_impath(name)
    im = engine.open_image(impath)
    im = engine.set_geometry(im, (50, 50), {'resize': 'fit'})

    tmp = join(str(tmpdir), name)
    engine._save_to(im, tmp, 'png')
    assert_size(tmp, width=50, height=35)
    engine.close_image(im)


def test_geometry_wh_portrait(engine, tmpdir):
    name = 'b94x200.png'
    impath = get_impath(name)
    im = engine.open_image(impath)
    im = engine.set_geometry(im, (50, 50), {'resize': 'fit'})

    tmp = join(str(tmpdir), name)
    engine._save_to(im, tmp, 'png')
    assert_size(tmp, width=24, height=50)
    engine.close_image(im)


def test_geometry_wh_upscale(engine, tmpdir):
    name = 'a200x140.png'
    impath = get_impath(name)
    im = engine.open_image(impath)
    im = engine.set_geometry(im, (400, 400), {'resize': 'fit', 'upscale': True})

    tmp = join(str(tmpdir), name)
    engine._save_to(im, tmp, 'png')
    assert_size(tmp, width=400, height=280)
    engine.close_image(im)


def test_geometry_wh_stretch(engine, tmpdir):
    name = 'a200x140.png'
    impath = get_impath(name)
    im = engine.open_image(impath)
    im = engine.set_geometry(im, (50, 50), {'resize': 'stretch'})

    tmp = join(str(tmpdir), name)
    engine._save_to(im, tmp, 'png')
    assert_size(tmp, width=50, height=50)
    engine.close_image(im)


def test_get_builtin_filter(engine):
    f = engine.get_filter('blur', {})
    assert f == moar.filters.blur

    f = engine.get_filter('crop', {})
    assert f == moar.filters.crop

    f = engine.get_filter('rotate', {})
    assert f == moar.filters.rotate


def test_get_unknown_filter(engine):
    with pytest.raises(Exception):
        engine.get_filter('qwerty', {})


def test_get_custom_filter(engine):

    class MyFilter(object):

        def wand(self, im, *args, **options):
            return im

    my_filter = MyFilter()
    ff = engine.get_filter('qwerty', {'qwerty': my_filter})
    assert ff == my_filter


def test_apply_filters(engine):
    ini = 'a200x140.png'
    im = engine.open_image(get_impath(ini))
    filters = [('crop', 50, 50, 0, 0), ('rotate', 45)]
    ename = engine.__class__.__name__
    im = engine.apply_filters(im, filters, {}, {})
    out = ename + '-filters.png'
    tmp = join(str(tmpdir), out)
    engine._save_to(im, tmp)
    assert_image(tmp, out)
