# -*- coding: utf-8 -*-
"""
# moar.filters.sepia

This filter will turn your image into sepia tones, making it looks like an
old photo.

The interesting trick about sepia images is that they are just gray-scale
pictures with a different color palette. In this case the default sepia tone
is #fff0c0.

If you would want to change it, the tone can be expressed as a RGB list of
values or like an hex string.

Examples:

```python
thumbnail(source, '200x100', ('sepia', ) )
thumbnail(source, '200x100', ('sepia', 255, 240, 192) )
thumbnail(source, '200x100', ('sepia', '#fff0c0') )
```
"""
try:
    from PIL import ImageOps
except ImportError:
    pass
from moar._compat import string_types


SEPIA_DEFAULT_TONE = (255, 240, 192)


def pil(im, *args, **options):
    ramp = options.get('ramp', get_ramp(args))
    original_mode = im.mode
    # Make grayscale
    im = ImageOps.autocontrast(im.convert('L'))
    # Apply tone
    im.putpalette(ramp)
    # Restore mode
    im = im.convert(original_mode)
    return im


def wand(im, *args, **options):
    raise NotImplementedError
    return im


def get_ramp(args):
    if not args or not args[0]:
        tone = SEPIA_DEFAULT_TONE
    elif len(args) == 1:
        tone = hex_to_rgb(args[0])
    else:
        tone = args[:3]
    return make_linear_ramp(tone)


def hex_to_rgb(color):
    """Transforms an hex color (eg: #ffaf2e, #fff) into a RGB tuple.
    """
    if not isinstance(color, string_types):
        return color
    color = color.lstrip('#')
    len_color = len(color)
    try:
        if len_color >= 6:
            return tuple([int(c, 16) for c in (color[0:2], color[2:4], color[4:6])])
        elif len_color >= 3:
            return tuple([int(c, 16) * 17 for c in color[0:3]])
        raise ValueError
    except ValueError as error:
        raise ValueError("'%s' is not an hex color (%s)" % (color, error.message))


def make_linear_ramp(white):
    """ Normalizes a RGB tuple to 0..1 values.
    """
    ramp = []
    r, g, b = white
    for i in range(255):
        ramp.extend([(r * i) / 255, (g * i) / 255, (b * i) / 255])
    return ramp
