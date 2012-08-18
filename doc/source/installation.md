title: Installation
template: page.html
description: Instructions to install Moar


# Installation

To install with `pip`, just do

	pip install moar

## Requirements

You need to have an image library installed. Moar ships with support for the [Python Imaging Library][pil]{:target=_blank} and [ImageMagick][imagemagick]{:target=_blank} via [wand][wand]{:target=_blank}. 


### Python Imaging Library (PIL) installation

Prerequisites:

* libjpeg
* zlib

Ubuntu 10.04 package installation:

    sudo apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev

Then, install the [Python Imaging Library][pil]{:target=_blank} using pip:

    pip install pil

Watch the output for messages on what support got compiled in, you at least want to see the following:

    --- JPEG support available
    --- ZLIB (PNG/ZIP) support available


### Wand installation

Prerequisites:

* ImageMagick

#### In Ubuntu 12.4:
    
    sudo apt-get install libmagickwand-dev
    pip install Wand==0.2

#### In Mac OSX:

    brew install imagemagick
    pip install Wand==0.2


## Getting the source code

Moar is actively developed on GitHub, where the code is [always available]({{ GITHUB_URL }}).

You can either clone the public repository

    git clone git://github.com/lucuma/moar.git

download the tarball

    wget https://github.com/lucuma/moar/tarball/master

or, download the zipball:
    
    wget https://github.com/lucuma/moar/zipball/master

Once you have a copy of the source, you can embed it in your Python package,
or install it into your site-packages easily:

    python setup.py install


[pil]: http://www.pythonware.com/products/pil/
[imagemagick]: http://www.imagemagick.org/script/index.php
[wand]: http://styleshare.github.com/wand/

