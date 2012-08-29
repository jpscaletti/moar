title: Moar thumbnails
template: index.html


Welcome to **Moar**, an on-the-fly image thumbnailer library written in Python and MIT licensed.

Your site design changes a lot, but that means manually generate new thumbnails for all the uploaded images. Not anymore. With Moar you can upload once and generate thumbnails dynamically, just changing a line in your templates.

Example (using Jinja2):

```jinja
<img src="{{ thumbnail(source, '200x100', ['crop', 50, 50]) }}" />
```

The thumbnails are cached and can be deleted or regenerated transparently. And the library can be extended to store them in custom backends.


<div class="maintoc" markdown="1">
# Table of contents

* [Installation](/installation.md)
* [Quickstart](/quickstart.md)
* [Thumbnail generation](/thumbnail.md)
* [Thumbnailer class](/thumbnailer.md)
<!-- * [Extending the library](/extending.md) -->
</div>


# Features at a glance

* Pluggable engine support ([PIL][pil]{:target=_blank} and [Wand][wand]{:target=_blank} (a wrapper for [ImageMagick][imagemagick]{:target=_blank}) included<sup>*</sup>).
* Automatic cache: a thumbnail is generated only once.
* Pluggable storage support (FileSystem included).
* Flexible, simple syntax, generates no HTML.
* Auto-rotates the image according to its EXIF information. <sup>*</sup>
* Several filters available by default:
    * Cropping
    * Rotation
    * Blur
    * Grayscale/Sepia <sup>*</sup>
* Easily extendable.

<div class="warning" markdown="1"><sup>*</sup> The Wand engine doesn't have **yet** support for the EXIF-based auto-rotation or grayscale/sepia filters.</div>

[pil]: http://www.pythonware.com/products/pil/
[imagemagick]: http://www.imagemagick.org/script/index.php
[wand]: http://styleshare.github.com/wand/
