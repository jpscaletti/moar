# coding=utf-8
from io import BytesIO
import os

from PIL import Image, ImageChops


THIS_PATH = os.path.dirname(__file__)
RES_PATH = os.path.join(THIS_PATH, u'assets')
tmpdir = os.path.join(RES_PATH, u't')


def get_impath(name='a200x140.png'):
    return os.path.join(RES_PATH, name)


def almost_equal(val1, val2, error=3):
    return abs(val1 - val2) <= error


def assert_size(path, width=None, height=None):
    im = Image.open(path)
    w, h = im.size
    if width:
        assert w == width
    if height:
        assert h == height


def assert_image(tp, cname, assert_equal=True):
    test = Image.open(tp).convert('RGB')
    cp = get_impath(cname)
    control = Image.open(cp).convert('RGB')
    try:
        diff = ImageChops.difference(test, control).getbbox()
        print('DIFF', diff)
        equal = diff is None
    except ValueError as e:
        print(e)
        equal = False
    if assert_equal:
        assert equal
    else:
        assert not equal


def get_raw_data(path, format=None):
    buf = BytesIO()
    im = Image.open(path)
    format = format or im.format
    im.save(buf, format=format)
    raw_data = buf.getvalue()
    buf.close()
    return raw_data


class MockMethod(object):
    was_called = False
    args = None
    kwargs = None

    def __init__(self, return_value=None):
        self.return_value = return_value

    def __call__(self, *args, **kwargs):
        self.was_called = True
        self.args = args
        self.kwargs = kwargs
        return self.return_value
