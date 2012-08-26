title: Extending the library
template: page.html

# Extending the library



# Add a filter

```python
pil(im, *args, **options)
wand(im, *args, **options)
```


# Add a storage

```python
get(self, thumb)
save(self, thumb, raw_data)
```


# Add an engine

```python
load_image(self, path)
close_image(self, im)
get_data(self, im, options)
```

