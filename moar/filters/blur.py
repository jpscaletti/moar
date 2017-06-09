# coding=utf-8
"""
# moar.filters.blur

Apply a gaussian blur (smoothing) to the image. The `radius` argument
determines the scale of fine detail that will be removed. Low values remove
only very fine detail while high values remove larger levels of detail.

Example:

```python
thumbnail(source, '200x100', ('blur', 4) )
```

"""


def apply(im, radius, *args, **options):
    im.resize(blur=radius)
    return im
