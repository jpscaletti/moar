title: Thumbnail generation
template: page.html


# The "thumbnail" function

Syntax:

```python
thumbnail(source, geometry, (key1, value1), (key2, value2), ..., options)
```

The `thumbnail` function takes a source image, a geometry parameter, a number of optionals filters as tuples and/or a number of custom options (the same ones of the [Thumbnailer][thumbnailer] class), and returns the URL of the generated thumbnail.

```jinja
<img src="{{ thumbnail( ... ) }}" />
```


## Source

Source must be a local image represented as an object or a dictionary with the following attributes or keys:

path
:   absolute path to the image, including it's name.
    Eg: `/var/example.com/media/2012/05/05/lena.jpg`.

url
:   URL to the container of the images, either absolute or relative to the domain.
    Eg: `http://lucumalabs.com/media/2012/05/05/lena.jpg`, `/media/2012/05/05/lena.jpg`.

<div class=note markdown=1>
Some python web frameworks (like Django) use image objects with both of these attributes.
</div>


## Geometry

Geometry is specified as `width`x`height`, `width` or x`height`.
Width and height are in pixels. 

This value can either be a string or a callable that return a valid geometry string. Examples:

```python
thumbnail(source, '200x100')
thumbnail(source, '200')
thumbnail(source, 'x100')
thumbnail(source, get_geometry)
```

If both width and height are given, the image is rescaled to the maximum size that fits in a width x height box, preserving the aspect ratio. 

If the `resize` option is `True`, however, the image is deformed to match exactly the given dimensions,

If the geometry is `None` or an empty string, no rescaling will be applied.


## Filters

The filters are defined as a sequence of list or tuples.

    ['filter1', value], ['filter2', value1, value2], ['filter3'] ...

They are defined this way instead of using keyword arguments because the order in which are applied could matter.

The filters described below are those available in the shipped engines, but you can easily add more (see the section "[extending the library](extending.md#filters)" for more info about that).


### crop (width, height, x=0, y=0)

Crop accepts a width, height and one or two optional values as the coordinates of the new top-left corner (`(0, 0)` by default). These last values can be integers (pixels), percentages or 'center'.

For example, some valid values are:

```python
thumbnail(source, '200x100', ['crop', 50, 50])
thumbnail(source, '200x100', ['crop', 50, 50, '15%', '10%'])
thumbnail(source, '200x100', ['crop', 50, 50, 150, 50])
thumbnail(source, '200x100', ['crop', 50, 50, 'center', 0])
thumbnail(source, '200x100', ['crop', 50, 50, 'center', 'center'])
```

### grayscale

If you include this filter it will turn the image into gray-scale.

Example:

```python
thumbnail(source, '200x100', ['grayscale'])
```

### sepia (tone='#fff0c0')

This filter will turn your image into sepia tones, making it looks like an old photo.

The interesting trick about sepia images is that they are just gray-scale pictures with a different color palette. In this case the default sepia tone is #fff0c0.

If you would want to change it, the tone can be expressed as a RGB list of values or like an hex string.

Examples:

```python
thumbnail(source, '200x100', ['sepia'])
thumbnail(source, '200x100', ['sepia', 255, 240, 192])
thumbnail(source, '200x100', ['sepia', '#fff0c0'])
```

### rotate (degrees)

Rotates the image counter-clockwise by a specified number of degrees. If degrees is negative, the rotation it's clockwise instead.

Example:

```python
thumbnail(source, '200x100', ['rotate', 45])
thumbnail(source, '200x100', ['rotate', -90])
```

### blur (radius=2)

Apply a gaussian blur (smoothing) to the image. The `radius` argument determines the scale of fine detail that will be removed. Low values remove only very fine detail while high values remove larger levels of detail.

Example:

```python
thumbnail(source, '200x100', ['blur', 4])
```


## Options

The options overwrite the default ones defined in the [Thumbnailer][thumbnailer] class.

{% include "options.md" %}


[thumbnailer]: thumbnailer.md

