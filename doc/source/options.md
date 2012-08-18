upscale
:   Upscale is a boolean that controls if the image can be upscaled or not. For example if your source is `"100x100"` and you request a thumbnail of size `"200x200"` and upscale is `False` this will return a thumbnail of size 100x100. If upscale were `True` this would result in a thumbnail size `"200x200"` (upscaled). The default value is `True`.

quality
:   When the output format is jpeg, quality is a value between 0-100 that controls the thumbnail write quality. Default value is `90`.

progressive
:   This controls whether to save jpeg thumbnails as progressive jpegs. Default value is `True`.

orientation
:   This controls whether to orientate the resulting thumbnail with respect to the source EXIF tags for orientation. Default value is `True`.

format
:   This controls the write format and thumbnail extension. Formats supported by the shipped engines are `"JPEG"` and `"PNG"`. Default value is `"JPEG"`.

resize
:   When setting the new geometry, this controls if the image is deformed to match exactly the given dimensions, regardless of the aspect ratio of the original image. If `resize` is `True`, the `upscale` option is ignored. Default value is `False`.