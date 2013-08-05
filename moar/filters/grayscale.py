# -*- coding: utf-8 -*-
"""
# moar.filters.grayscale

Examples:

```python
thumbnail(source, '200x100', ('grayscale', ) )
```
"""
from . import sepia


def get_ramp():
    tone = (255, 255, 255)
    return sepia.make_linear_ramp(tone)


def pil(im, *args, **options):
    ramp = get_ramp()
    return sepia.pil(im, ramp=ramp, *args, **options)


def wand(im, *args, **options):
    ramp = get_ramp()
    return sepia.wand(im, ramp=ramp, *args, **options)
