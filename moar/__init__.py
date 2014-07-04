# -*- coding: utf-8 -*-
"""
=========
Moar
=========

A library, written in Python, that allows you to make custom thumbnails wherever you need them.

    <img src="{{ thumbnail(source, '200x100', ('crop', 50, 50)) }}" />


See the documentation online at http://lucuma.github.com/moar/


Features at a glance
---------------------

* Pluggable engine support (PIL/Pillow and _Wand: http://docs.wand-py.org/ included).
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
_MIT License: http://www.opensource.org/licenses/mit-license.php

© 2011 by _Lúcuma labs: http://lucumalabs.com

"""
from moar.thumbnailer import Thumbnailer
from moar.engines.pil_engine import PILEngine
from moar.engines.wand_engine import WandEngine
from moar.storages.file_storage import FileStorage


__version__ = '1.2.3'
