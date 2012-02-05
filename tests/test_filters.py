# -*- coding: utf-8 -*-
import moar

from PIL import Image

from .utils import *


def test_pil_blur():
    thumbnail = moar.Thumbnailer(engine=moar.engines.pil.Engine)
    source = get_source('a200x140.png')

    thumb = thumbnail(source, ('blur', 20), format='PNG')
    name = thumb.key + '.png'
    assert_image(name, 'blur20pil.png')

    remove_thumb(name)


def test_pil_rotate_ccw():
    thumbnail = moar.Thumbnailer(engine=moar.engines.pil.Engine)
    source = get_source('a200x140.png')

    thumb = thumbnail(source, ('rotate', 60), format='PNG')
    name = thumb.key + '.png'
    assert_image(name, 'rotate60ccw.png')

    remove_thumb(name)


def test_pil_rotate_cw():
    thumbnail = moar.Thumbnailer(engine=moar.engines.pil.Engine)
    source = get_source('a200x140.png')

    thumb = thumbnail(source, ('rotate', -60), format='PNG')
    name = thumb.key + '.png'
    assert_image(name, 'rotate60cw.png')

    remove_thumb(name)


def test_pil_rotate_noalpha():
    thumbnail = moar.Thumbnailer(engine=moar.engines.pil.Engine)
    source = get_source('a200x140.png')

    thumb = thumbnail(source, ('rotate', 60), format='JPEG')
    name = thumb.key + '.jpeg'
    tp = get_tpath(name)
    im = Image.open(tp)
    assert im.getpixel((0, 0)) == (255, 255, 255)

    remove_thumb(name)


def test_pil_filters_comp():
    thumbnail = moar.Thumbnailer(engine=moar.engines.pil.Engine)
    source = get_source('a200x140.png')

    thumb = thumbnail(source, '150x150',
        ('rotate', 50),
        ('crop', 60, 70, 'center'),
        format='PNG'
    )
    name = thumb.key + '.png'
    assert_image(name, 'multifilter-pil.png')

    remove_thumb(name)


def test_magick_blur():
    thumbnail = moar.Thumbnailer(engine=moar.engines.magick.Engine)
    source = get_source('a200x140.png')

    thumb = thumbnail(source, ('blur', 20), format='PNG')
    name = thumb.key + '.png'
    assert_image(name, 'blur20pil.png')

    remove_thumb(name)


def test_magick_rotate_ccw():
    thumbnail = moar.Thumbnailer(engine=moar.engines.magick.Engine)
    source = get_source('a200x140.png')

    thumb = thumbnail(source, ('rotate', 60), format='PNG')
    name = thumb.key + '.png'
    assert_image(name, 'rotate60ccw.png')

    remove_thumb(name)


def test_magick_rotate_cw():
    thumbnail = moar.Thumbnailer(engine=moar.engines.magick.Engine)
    source = get_source('a200x140.png')

    thumb = thumbnail(source, ('rotate', -60), format='PNG')
    name = thumb.key + '.png'
    assert_image(name, 'rotate60cw.png')

    remove_thumb(name)


def test_magick_rotate_noalpha():
    thumbnail = moar.Thumbnailer(engine=moar.engines.magick.Engine)
    source = get_source('a200x140.png')

    thumb = thumbnail(source, ('rotate', 60), format='JPEG')
    name = thumb.key + '.jpeg'
    tp = get_tpath(name)
    im = Image.open(tp)
    assert im.getpixel((0, 0)) == (255, 255, 255)

    remove_thumb(name)


def test_magick_filters_comp():
    thumbnail = moar.Thumbnailer(engine=moar.engines.magick.Engine)
    source = get_source('a200x140.png')

    thumb = thumbnail(source, '150x150',
        ('rotate', 50),
        ('crop', 60, 70, 'center'),
        format='PNG'
    )
    name = thumb.key + '.png'
    assert_image(name, 'multifilter-magick.png')

    remove_thumb(name)


