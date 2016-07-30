# # -*- coding: utf-8 -*-
# """
# Amazon S3 storage.

# """
# from io import BytesIO
# import mimetypes
# import os

# from moar._compat import urlparse, url_quote
# from moar.thumb import Thumb
# from moar.storages.base import BaseStorage


# class S3Storage(BaseStorage):

#     """Amazon S3 storage.

#     client:
#         A boto3 S3 client.

#     bucket:
#         Bucket name.

#     """

#     def __init__(self, client, bucket):
#         self.client = client
#         self.bucket = bucket
#         super(self.__class__, self).__init__()

#     def get_source(self, path):
#         """Download the file to a temporary place and
#         returns the absolute path to it.
#         """
#         pass

#     def get_thumb(self, path, key, format):
#         thumbpath = self._get_thumbpath(path, key)
#         try:
#             obj = self.container.get_object(thumbpath)
#         except Exception:
#             return None
#         fullpath = os.path.join(self.base_path, path)
#         encoded_name = url_quote(obj.name)
#         url = urlparse.urljoin(self.container.cdn_uri, encoded_name)
#         return Thumb(url, key, fullpath=fullpath)

#     def _get_thumbpath(self, path, key):
#         head, tail = os.path.split(path)
#         return os.path.join(head, key, tail)

#     def save(self, path, key, format, data, w=None, h=None):
#         thumbpath = self._get_thumbpath(path, key)
#         content_type = mimetypes.guess_type(path)
#         if content_type and content_type[0] and content_type[1]:
#             content_type = '/'.join(content_type)
#         else:
#             content_type = None
#         obj = self.container.upload_file(
#             BytesIO(data),
#             obj_name=thumbpath,
#             content_type=content_type,
#         )
#         fullpath = os.path.join(self.base_path, path)
#         encoded_name = url_quote(obj.name)
#         url = urlparse.urljoin(self.container.cdn_uri, encoded_name)
#         return Thumb(url, key, fullpath=fullpath)
