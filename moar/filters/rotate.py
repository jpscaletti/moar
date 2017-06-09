# coding=utf-8
"""
# moar.filters.rotate

Rotates the image counter-clockwise by a specified number of degrees.
If degrees is negative, the rotation it's clockwise instead.

Example:

```python
thumbnail(source, '200x100', ('rotate', 45) )
thumbnail(source, '200x100', ('rotate', -90) )
```
"""
try:
    from wand.color import Color
except ImportError:
    pass


def apply(im, angle, *args, **options):
    angle = - angle  # Wand rotates clockwise
    background = None
    format = options.get('format', im.format)
    with Color('#fff') as white:
        if format and format.lower() != 'png':
            background = white
        im.rotate(angle, background=background, reset_coords=True)
    return im
