
# Welcome to Moar

Hi, this is Moar, a on-the-fly thubnailer library written in Python and MIT licensed.

Your site design changes a lot, but that means manually generate new thumbnails for all the uploaded images.

Not anymore. With **Moar** you can upload once and generate thumbnails on the fly, just changing a line in your templates.

```jinja
<img src="{{ thumbnail(source, '200x100', ['crop', 50, 50]) }}" />
```

The thumbnails are cached and can be deleted or regenerated transparently. And the library can be extended to store them in custom backends.

See the documentation online at http://lucuma.github.com/moar/
or in [doc/source](https://github.com/lucuma/moar/tree/master/doc/source).


## Features at a glance

* Pluggable engine support ([PIL](http://www.pythonware.com/products/pil/) and [GraphicsMagick](http://www.graphicsmagick.org/) included).
* Automatic cache: a thumbnail is generated only once.
* Pluggable storage support (FileSystem included).
* Flexible, simple syntax, generates no HTML.
* Several filters available by default:
    * Cropping
    * Rotation
    * Blur
    * Grayscale/Sepia
* Easily extendable.


---------------------------------------
[MIT License] (http://www.opensource.org/licenses/mit-license.php).
© [Lúcuma] (http://lucumalabs.com).  
