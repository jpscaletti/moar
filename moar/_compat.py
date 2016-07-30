# coding=utf-8
"""
Utilities for writing code that runs on Python 2 and 3.
"""
import sys
try:
    from urllib.parse import urlparse
    from urllib.parse import quote as url_quote
    from urllib.request import urlopen
except ImportError:
    import urlparse
    from urllib import quote as url_quote
    from urllib import urlopen

PY2 = sys.version_info[0] == 2
string_types = (basestring, ) if PY2 else (str, )
