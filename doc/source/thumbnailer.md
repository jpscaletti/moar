title: Thumbnailer class
template: page.html

# Thumbnailer class

Syntax:

```python
from moar import Thumbnailer

thumbnail = Thumbnailer([engine], [storage],
                [filters=extra_filters], [**default_options])
```

Moar come with support for pluggable engines and storages. By default it use `moar.engines.pil.Engine` and `moar.storages.filesystem.Storage`.

When you call the thumbnail instance, the current storage class will generates a key that represent a thumbnail made from that image with that specific filters and options. If a thumbnail with that key hasn't been generated before, it'll make a new one, store it using the key as an id, and returns it.

The default storage class (`moar.storages.filesystem.Storage`) store the generated thumbnails inside a `"t"` folder in the same path as the source image (this can be changed). Other storages will operate different, for example, storing the key in a local database and uploading the thumbnail to a remote server.


## Filters

You can use the `filters` parameter to define a list of custom filters, adding them to those included by default. E.g.:

```python
from image_filters import watermak, enhace

thumbnail = Thumbnailer(filters=[watermak, enhace])
```

<div class=note markdown=1>
The filters has to have a method named after the current engine (eg: `"wand"` or `"pil"`) or the'll be unusable. See the "[extending the library](extending.md#filters)" section for more details.
</div>

## Default Options

These options are the default for all thumbnails. However, they can be overwritten in individual `thumbnail` calls.

{% include "options.md" %}

