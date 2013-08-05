title: Quick start
template: page.html
prev: [Installation](/installation.md)
next: [Thumbnail generation](/thumbnail.md)


# Quick start

First, define a thumbnailer to use:

```python
from moar import Thumbnailer

thumbnail = Thumbnailer()
```

Then, make it accesible in your templates. For instance, as a jinja2 global:

```python
render.set_global('thumbnail', thumbnail)
```

Finally, you call it from your code:

```jinja
<img src="{{ thumbnail(item.image, '100x100') }}" />
```

or like this:

```jinja
{% with t = thumbnail(item.image, '100x100') %}
<img src="{{ t.url }}" width="{{ t.width }}" height="{{ t.heigth }}" />
{% endwith %}
```

The thumbnailer function expects at least two parameters:

* A relative file path, either as a string or as a dictionary with the form `{'path': <relpath>}`
* A `geometry` parameter with the desired width and/or height of the image thumbnail.

It also takes several other parameters describing further processing like cropping, rotating, etc.
See the [thumbnail](thumbnail.md) section for the available options.

The output of the thumbnailer is an object like this:

```python
class Thumb:
    url = <absolute URL of the thumbnail>
    width = <thumbnail width>
    height = <thumbnail height>

    def __repr__(self):
        return self.url
```

You can invoke it from your templates or directly from your python code, when you want generate the thumbnail right away.

```
>>> t = thumbnail(my_file.jpg, '100x100')
>>> print(t)
http://example.org/media/t/3423423af38.jpg
>>> print(t.width, t.height)
(100, 100)
```

