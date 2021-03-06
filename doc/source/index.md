title: Moar: on-the-fly image thumbnailer
layout: /theme/index.html


Welcome to **Moar**, an on-the-fly image thumbnailer library written in Python and MIT licensed.

Your site design changes a lot, but that means manually generate new thumbnails for all the uploaded images. Not anymore. With Moar you can upload once and generate thumbnails dynamically, just changing a line in your templates.

Example (using Jinja2):

```jinja
<img src="{{ thumbnail(source, '200x100', ['crop', 50, 50]) }}" />
```

The thumbnails are cached and can be deleted or regenerated transparently. And the library can be extended to store them in custom backends.


# Table of contents

* [Installation](/installation.html)
* [Quickstart](/quickstart.html)
* [Thumbnail generation](/thumbnail.html)
* [Thumbnailer class](/thumbnailer.html)
<!-- * [Extending the library](/extending.html) -->


# Features at a glance

* Pluggable engine support (ships with [ImageMagick][imagemagick]{:target=_blank}) support).
* Automatic cache: a thumbnail is generated only once.
* Pluggable storage support.
* Flexible, simple syntax, generates no HTML.
* Auto-rotates the image according to its EXIF information.
* Several filters available by default:
    * Cropping
    * Rotation
    * Blur
* Easily extendable to add your oen filters.

[imagemagick]: http://www.imagemagick.org/script/index.php

