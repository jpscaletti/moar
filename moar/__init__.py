# coding=utf-8
"""
=========
Moar
=========

A library, written in Python, that allows you to make custom thumbnails wherever you need them.

    <img src="{{ thumbnail(source, '200x100', ('crop', 50, 50)) }}" />


See the documentation online at http://lucuma.github.com/moar/


Features at a glance
---------------------

* Pluggable engine support (`Wand <http://docs.wand-py.org/>` included).
* Automatic cache: a thumbnail is generated only once.
* Pluggable storage support (includes local files and S3 storages).
* Flexible, simple syntax, generates no HTML.
* Several filters available by default:
    * Cropping
    * Rotation
    * Blur
* Easily extendable.


:copyright: `Juan-Pablo Scaletti <http://jpscaletti.com>`_.
:license: MIT, see LICENSE for more details.

"""
from moar.storage import Storage
from moar.thumbnailer import Thumbnailer
from moar.engines.wand_engine import WandEngine

__version__ = '3.0.0'
