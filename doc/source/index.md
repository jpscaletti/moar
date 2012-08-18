title: Moar thumbnails documentation
template: page.html
index: 1


# Moar thumbnails

**Welcome to Moar!**

Moar is an MIT Licensed library, written in Python, that allows you to make custom thumbnails whenever you need them in your application.

```jinja
<img src="{{ thumbnail(source, '200x100', ['crop', 50, 50]) }}" />
```


## Features at a glance

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

<div class="warning" markdown="1">
<sup>*</sup> The Wand engine doesn't have **yet** support for the EXIF-based auto-rotation or
grayscale/sepia filters.
</div>

[pil]: http://www.pythonware.com/products/pil/
[imagemagick]: http://www.imagemagick.org/script/index.php
[wand]: http://styleshare.github.com/wand/
