# -*- coding: utf-8 -*-
import pytest

from .utils import assert_image
from .test_filters import apply_filter


def test_sepia(engine):
    if engine.name == 'wand':
        pytest.xfail("not implemented yet")
    ini = 'a200x140.png'
    out = engine.name + '-sepia.png'
    tp = apply_filter(engine, 'sepia', ini, out)
    assert_image(tp, out)


def test_sepia_rgb(engine):
    if engine.name == 'wand':
        pytest.xfail("not implemented yet")
    ini = 'a200x140.png'
    out = engine.name + '-sepia240_220_190.png'
    tp = apply_filter(engine, 'sepia', ini, out, 240, 220, 190)
    assert_image(tp, out)


def test_sepia_hex(engine):
    if engine.name == 'wand':
        pytest.xfail("not implemented yet")
    ini = 'a200x140.png'
    out = engine.name + '-sepiaFFAF2E.png'
    tp = apply_filter(engine, 'sepia', ini, out, '#ffaf2e')
    assert_image(tp, out)


def test_grayscale(engine):
    if engine.name == 'wand':
        pytest.xfail("not implemented yet")
    ini = 'a200x140.png'
    out = engine.name + '-grayscale.png'
    tp = apply_filter(engine, 'grayscale', ini, out)
    assert_image(tp, out)
