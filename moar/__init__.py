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

* Pluggable engine support (PIL/Pillow and `Wand <http://docs.wand-py.org/>` included).
* Automatic cache: a thumbnail is generated only once.
* Pluggable storage support (FileSystem included).
* Flexible, simple syntax, generates no HTML.
* Several filters available by default:
    * Cropping
    * Rotation
    * Blur
    * Grayscale/Sepia
* Easily extendable.


:copyright: `Juan-Pablo Scaletti <http://jpscaletti.com>`_.
:license: MIT, see LICENSE for more details.

"""
from moar.thumbnailer import Thumbnailer
from moar.engines.pil_engine import PILEngine
from moar.engines.wand_engine import WandEngine
from moar.storages.file_storage import FileStorage
from moar.storages.rackspace_storage import RackspaceStorage

__version__ = '1.4.0'
