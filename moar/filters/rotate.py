# -*- coding: utf-8 -*-
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
    from PIL import Image
except ImportError:
    pass
try:
    from wand.color import Color
except ImportError:
    pass


def pil(im, angle, *args, **options):
    im = im.convert('RGBA')
    im = im.rotate(angle, resample=Image.BICUBIC, expand=True)
    format = options.get('format', im.format)
    if format and format.lower() != 'png':
        # a white image same size as rotated image
        white = Image.new('RGB', im.size, (255, 255, 255))
        # create a composite image using the alpha
        # layer of im as a mask
        im = Image.composite(im, white, im)
    return im


def wand(im, angle, *args, **options):
    angle = - angle  # Wand rotates clockwise
    background = None
    format = options.get('format', im.format)
    with Color('#fff') as white:
        if format and format.lower() != 'png':
            background = white
        im.rotate(angle, background=background, reset_coords=True)
    return im
