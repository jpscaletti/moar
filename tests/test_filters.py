# coding=utf-8
from os.path import join

from moar import filters
from PIL import Image
import pytest

from .utils import get_impath, assert_image, tmpdir


def apply_filter(engine, fname, ini, out, *args, **kwargs):
    ff = getattr(filters, fname)
    impath = get_impath(ini)
    im = engine.open_image(impath)
    im = ff.apply(im, *args, **kwargs)
    tmp = join(str(tmpdir), out)
    engine._save_to(im, tmp)
    print(tmp)
    return tmp


@pytest.mark.skip
def test_blur(engine):
    ename = engine.__class__.__name__
    ini = 'a200x140.png'
    out = ename + '-blur20.png'
    tp = apply_filter(engine, 'blur', ini, out, 20)
    assert_image(tp, out)


def test_rotate(engine):
    ename = engine.__class__.__name__
    ini = 'a200x140.png'
    out = ename + '-rotate60.png'
    tp = apply_filter(engine, 'rotate', ini, out, 60)
    assert_image(tp, out)


def test_rotate_noalpha(engine):
    ename = engine.__class__.__name__
    ini = 'a200x140.png'
    out = ename + '-rotate-no-alpha.jpeg'
    tp = apply_filter(engine, 'rotate', ini, out, -60, format='jpeg')
    im = Image.open(tp)
    assert im.getpixel((0, 0)) == (255, 255, 255)
