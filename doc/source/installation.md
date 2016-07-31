title: Installation
layout: /theme/page.html
description: Instructions to install Moar
next: /quickstart.html


# Installation

Install `pip` and then use it to install Moar:

	easy_install pip
    pip install moar

## Requirements

You need to have an [ImageMagick][imagemagick]{:target=_blank} and the python [wand][wand]{:target=_blank} library installed.

Prerequisites:

* ImageMagick

#### In Ubuntu 12.4:
    
    sudo apt-get install libmagickwand-dev
    pip install Wand

#### In Mac OSX:

    brew install imagemagick
    pip install Wand


## Getting the source code

Moar is actively developed on GitHub, where the code is [always available]({{ GITHUB_URL }}).

You can either clone the public repository

    git clone git://github.com/lucuma/moar.git

or, download the zipball:
    
    wget https://github.com/lucuma/moar/zipball/master

Once you have a copy of the source, you can embed it in your Python package,
or install it into your site-packages easily:

    python setup.py install

[imagemagick]: http://www.imagemagick.org/script/index.php
[wand]: http://styleshare.github.com/wand/
