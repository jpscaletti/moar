# coding=utf-8
from os.path import join

from moar import filters
from PIL import Image
import pytest

from .utils import get_impath, assert_image, tmpdir


def get_filter(engine, fname):
    mod = getattr(filters, fname)
    return getattr(mod, engine.name)


def apply_filter(engine, fname, ini, out, *args, **kwargs):
    f = get_filter(engine, fname)
    impath = get_impath(ini)
    im = engine.open_image(impath)
    im = f(im, *args, **kwargs)
    tmp = join(str(tmpdir), out)
    engine._save_to(im, tmp)
    print(tmp)
    return tmp


@pytest.skip
def test_blur(engine):
    if engine.name == 'wand':
        pytest.xfail("not implemented yet")
    ini = 'a200x140.png'
    out = engine.name + '-blur20.png'
    tp = apply_filter(engine, 'blur', ini, out, 20)
    assert_image(tp, out)


def test_rotate(engine):
    ini = 'a200x140.png'
    out = engine.name + '-rotate60.png'
    tp = apply_filter(engine, 'rotate', ini, out, 60)
    assert_image(tp, out)


def test_rotate_noalpha(engine):
    ini = 'a200x140.png'
    out = engine.name + '-rotate-no-alpha.jpeg'
    tp = apply_filter(engine, 'rotate', ini, out, -60, format='jpeg')
    im = Image.open(tp)
    assert im.getpixel((0, 0)) == (255, 255, 255)
