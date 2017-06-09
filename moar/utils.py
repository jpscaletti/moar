# coding=utf-8
from __future__ import print_function


def parse_geometry(geometry):
    """Parse a geometry string and returns a (width, height) tuple
    Eg:
        '100x200' ==> (100, 200)
        '50' ==> (50, None)
        '50x' ==> (50, None)
        'x100' ==> (None, 100)
        None ==> None

    A callable `geometry` parameter is also supported.
    """
    if not geometry:
        return None, None
    if callable(geometry):
        geometry = geometry()
    geometry = str(geometry).split('x')
    if len(geometry) == 1 or (len(geometry) > 1 and not geometry[1]):
        width = int(geometry[0])
        height = None
    else:
        w = geometry[0]
        width = int(w) if w else None
        height = int(geometry[1])
    return (width, height)
