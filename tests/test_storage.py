# coding=utf-8
from hashlib import sha1
import os

from moar import Storage

from .utils import RES_PATH, get_impath, get_raw_data


BASE_URL = 'http://example.com'


def get_random_key():
    return sha1(os.urandom(12)).hexdigest()


def test_get_thumbsdir():
    name = 'qwertyuiop'

    s = Storage(RES_PATH, BASE_URL)
    assert s.get_thumbsdir(name) == 't'

    s = Storage(RES_PATH, BASE_URL, thumbsdir='thumbs')
    assert s.get_thumbsdir(name) == 'thumbs'

    s = Storage(RES_PATH, BASE_URL, thumbsdir=lambda n: n[:3])
    assert s.get_thumbsdir(name) == name[:3]


def test_save():
    s = Storage(RES_PATH, BASE_URL)
    path = 'a200x140.png'
    name, _ = os.path.splitext(os.path.basename(path))
    key = get_random_key()
    data = get_raw_data(get_impath(path))
    thumb = s.save(path, key, 'png', data)

    assert thumb.url == '/'.join([BASE_URL, 't', name + '.' + key + '.png'])
    assert thumb.key == key


def test_get_nn_thumb():
    s = Storage(RES_PATH, BASE_URL)
    path = 'a200x140.png'
    key = get_random_key()
    thumb = s.get_thumb(path, key, 'jpeg')
    assert not thumb


def test_get_saved_thumb():
    s = Storage(RES_PATH, BASE_URL)
    path = 'a200x140.png'
    key = get_random_key()
    data = get_raw_data(get_impath(path))
    thumb = s.save(path, key, 'jpeg', data)

    thumb2 = s.get_thumb(path, key, 'jpeg')
    assert thumb.url == thumb2.url
