# coding=utf-8
"""
# moar.filters.crop

Crop accepts a geometry and one or two optional values as the
coordinates of the new top-left corner (0,0 by default).
These last values can be integers (pixels), percentages or 'center'.

The geometry parameter follow the same syntax as the one of the
Thumbnailer class: It can be 'WIDTHxHEIGHT', 'WIDTH' or 'xHEIGHT'

For example, some valid values are:

```python
thumbnail(source, '200x100', ('crop', '50') )
thumbnail(source, '200x100', ('crop', 'x50', '15%', '10%') )
thumbnail(source, '200x100', ('crop', '50x50', 150, 50) )
thumbnail(source, '200x100', ('crop', '50x50', 'center', 0) )
thumbnail(source, '200x100', ('crop', '50x50', 'center', 'center') )
```
"""
from moar._compat import string_types
from moar.utils import parse_geometry


def apply(im, *args, **options):
    imw, imh = im.size
    x, y, w, h = get_box(args, imw, imh)
    if x == 0 and y == 0 and w == imw and imh == h:
        return im
    im.crop(x, y, w, h, reset_coords=True)
    return im


def get_box(args, imw, imh):
    args = list(args)

    if (len(args) == 3):
        args.append(args[2])
    else:
        args.extend([0, 0])

    width, height = parse_geometry(args[1])
    ratio = float(imw) / imh
    if not width:
        width = int(height * ratio)
    elif not height:
        height = int(width / ratio)

    x = args[2]
    y = args[3]

    if isinstance(x, string_types):
        if x.endswith('%'):
            x = imw * int(x[:-1]) / 100
        elif x == 'center':
            x = (imw - width) / 2
        elif x.endswith('px'):
            x = x[:-2]

    x = int(x)
    x = max(x, 0)

    if isinstance(y, string_types):
        if y.endswith('%'):
            y = int(imh * int(y[:-1]) / 100)
        elif y == 'center':
            y = (imh - height) / 2
        elif y.endswith('px'):
            y = int(y[:-2])

    y = int(y)
    y = max(y, 0)

    # Do not overflow
    if width + x > imw:
        width = imw - x
    if height + y > imh:
        height = imh - y

    return x, y, x + width, y + height
