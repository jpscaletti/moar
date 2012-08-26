title: Moar thumbnails
template: index.html


Moar is a MIT Licensed library, written in Python, that allows you to make custom thumbnails only changing the template code. The result is cached and can be deleted an regenerated transparently, so your uploaded images can keep-up with your changing design without a glitch.

```jinja
<img src="{{ thumbnail(source, '200x100', ['crop', 50, 50]) }}" />
```


<div class="maintoc" markdown="1">
# Table of contents

* [Installation](/installation.md)
* [Quickstart](/quickstart.md)
* [The "thumbnail" function](/thumbnail.md)
* [Thumbnailer options](/thumbnailer.md)
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
