# -*- coding: utf-8 -*-
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
try:
    from PIL import ImageFilter

    class MyGaussianBlur(ImageFilter.Filter):

        name = "GaussianBlur"

        def __init__(self, radius=2):
            self.radius = radius

        def filter(self, image):
            return image.gaussian_blur(self.radius)

except ImportError:
    pass


def pil(im, radius, *args, **options):
    im = im.filter(MyGaussianBlur(radius))
    return im


def wand(im, radius, *args, **options):
    im.resize(blur=radius)
    return im
