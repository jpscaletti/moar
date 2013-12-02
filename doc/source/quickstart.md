title: Quick start
layout: /theme/page.html
prev: /installation.html
next: /thumbnail.html


# Quick start

First, define a thumbnailer to use with the images base path and base URL:

```python
from moar import Thumbnailer

thumbnail = Thumbnailer(MEDIA_PATH, MEDIA_URL)
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
{% with t = thumbnail(image, '100x100') %}
<img src="{{ t.url }}" width="{{ t.width }}" height="{{ t.heigth }}" />
{% endwith %}
```

The `image` argument is a relative file path of the local image.

The `geometry` argument is the desired width and/or height of the image thumbnail.

The function also takes several other parameters describing further processing like cropping, rotating, etc.
See the [thumbnail](thumbnail.html) section for the available options.

The output of the thumbnailer is an object similar to this:

```python
class Thumb:
    url = <absolute URL of the thumbnail>
    width = <thumbnail width>
    height = <thumbnail height>

    def __repr__(self):
        return self.url
```

You can invoke it from your templates or directly from your python code, when you want generate the thumbnail right away.


```python
>>> thumbnailer = Thumbnail(
>>>   u'/var/www/example/static/media',
>>>   u'http://media.example.org'
>>> )
>>> t = thumbnailer('foobar/my_file.jpg', '100x100')
>>> print(t)

http://media.example.org/foobar/t/my_file-23af38.jpg

>>> print(t.width, t.height)

(100, 100)
```

