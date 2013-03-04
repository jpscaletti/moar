# -*- coding: utf-8 -*-
import moar

from .utils import *


ENGINE = moar.engines.pil.Engine


def test_load_image():
    thumbnail = moar.Thumbnailer(engine=ENGINE)
    source = get_source('a200x140.png')
    
    thumb = thumbnail(source, format='PNG')
    name1 = thumb.key + '.png'
    assert_image(name1, 'default-pil.png')
    assert thumb.url == str(thumb)
    
    thumb2 = thumbnail(source, format='PNG')
    assert str(thumb) == str(thumb2)

    remove_thumb(name1)

    source = get_source('a200x140.jpg')
    thumb = thumbnail(source)
    name2 = thumb.key + '.jpg'
    assert_exists(name2)
    
    remove_thumb(name2)


def test_options():
    thumbnail = moar.Thumbnailer(engine=ENGINE)
    source = get_source('a200x140.png')

    thumb = thumbnail(source, format='JPEG', quality=20, progressive=True)
    name = thumb.key + '.jpg'
    assert_exists(name)

    remove_thumb(name)


def test_orientation():
    thumbnail = moar.Thumbnailer(engine=ENGINE)
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

    for sname in test_images:
        source = get_source(sname)
        thumb = thumbnail(source, orientation=True)
        name = thumb.key + '.jpg'
        assert_image(name, sname)

        remove_thumb(name)


def test_geometry_w():
    thumbnail = moar.Thumbnailer(engine=ENGINE)

    source = get_source('a200x140.jpg')
    thumb = thumbnail(source, '100')
    name = thumb.key + '.jpg'
    assert_size(name, width=100, height=70)

    remove_thumb(name)


def test_geometry_h():
    thumbnail = moar.Thumbnailer(engine=ENGINE)

    source = get_source('b94x200.png')
    thumb = thumbnail(source, 'x100')
    name = thumb.key + '.jpg'
    assert_size(name, width=47, height=100)

    remove_thumb(name)


def test_geometry_wh():
    thumbnail = moar.Thumbnailer(engine=ENGINE)

    source = get_source('a200x140.png')
    thumb = thumbnail(source, '50x50', format='PNG', resize='fit')
    name = thumb.key + '.png'
    assert_size(name, width=50, height=35)

    remove_thumb(name)

    source = get_source('b94x200.png')
    thumb = thumbnail(source, '50x50', format='PNG', resize='fit')
    name = thumb.key + '.png'
    assert_size(name, width=24, height=50)

    remove_thumb(name)


def test_geometry_wh_upscale():
    thumbnail = moar.Thumbnailer(engine=ENGINE)

    source = get_source('a200x140.jpg')
    thumb = thumbnail(source, '400x400', upscale=True, resize='fit')
    name = thumb.key + '.jpg'
    assert_size(name, width=400, height=280)

    remove_thumb(name)


def test_geometry_wh_resize():
    thumbnail = moar.Thumbnailer(engine=ENGINE)

    source = get_source('a200x140.jpg')
    thumb = thumbnail(source, '50x50', resize='stretch')
    name = thumb.key + '.jpg'
    assert_size(name, width=50, height=50)

    remove_thumb(name)


def test_geometry_callable():
    thumbnail = moar.Thumbnailer(engine=ENGINE)

    source = get_source('a200x140.jpg')
    thumb = thumbnail(source, lambda: str(50 * 2))
    name = thumb.key + '.jpg'
    assert_size(name, width=100, height=70)

    remove_thumb(name)

