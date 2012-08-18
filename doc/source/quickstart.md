title: Quick start
template: page.html


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

Finally, you call it from your templates:

```jinja
<img src="{{ thumbnail(item.image, '100x100') }}" />
```

The thumbnailer function expects at least two parameters:

* A `source` object or dictionary with, at least, a "`path`" and "`url`" attributes/keys.
* A `geometry` parameter with the desired width and/or height of the image thumbnail.


You can also invoke it directly from your code, when you want generate the thumbnail right away.

```python
thumbnail(my_file, '100x100')
```

See the [thumbnail](thumbnail.md) section for the available options.

