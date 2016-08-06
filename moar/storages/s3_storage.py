# coding=utf-8
"""
Amazon S3 storage.

"""
import os

import requests

from ..thumb import Thumb
from .base import BaseStorage


HTTP_OK = 200


class S3Storage(BaseStorage):

    """Amazon S3 storage.

    client:
        A boto3 S3 client.
    bucket:
        Bucket name.
    """

    def __init__(self, client, bucket_name):
        self.client = client
        self.bucket_name = bucket_name
        super(self.__class__, self).__init__()

    def get_source(self, path):
        """Returns the source image file descriptor.

        path:
            Path to the source image
        """
        bucket_name = self.get_bucket(path)
        try:
            img = self.client.get_object(Bucket=bucket_name, Key=path)
            return img['Body']
        except:
            return None

    def get_bucket(self, path):
        # bucket_name could be a callable
        # In that case, the name is built on the fly, based on the source path
        bucket_name = self.bucket_name
        if callable(self.bucket_name):
            bucket_name = self.bucket_name(path)
        return bucket_name

    def get_thumb(self, path, key, format):
        """Get the stored thumbnail if exists.

        path:
            path of the source image
        key:
            key of the thumbnail
        format:
            thumbnail's file extension
        """
        url = self.get_url(key)
        resp = requests.head(url)
        if resp.status_code != HTTP_OK:
            return Thumb()
        return Thumb(url=url, key=key)

    def get_thumbpath(self, path, key, format):
        """Return the thumbnail's path.

        path:
            path of the source image
        key:
            key of the thumbnail
        format:
            thumbnail file extension
        """
        relpath = os.path.dirname(path)
        name, _ = os.path.splitext(os.path.basename(path))
        name = '{}.{}.{}'.format(name, key, format.lower())
        return os.path.join(relpath, name)

    def get_url(self, path):
        bucket_name = self.get_bucket(path)
        return '{base}/{bucket}/{path}'.format(
            base=self.client.meta.endpoint_url,
            bucket=bucket_name,
            path=path,
        )

    def save(self, path, key, format, data):
        """Save a newly generated thumbnail.

        path:
            path of the source image
        key:
            key of the thumbnail
        format:
            thumbnail's file extension
        data:
            thumbnail's binary data
        """
        bucket_name = self.get_bucket(path)
        thumbpath = self.get_thumbpath(path, key, format)
        self.client.put_object(
            ACL='public-read',
            Body=data,
            Bucket=bucket_name,
            Key=thumbpath,
            StorageClass='REDUCED_REDUNDANCY'
        )
        url = self.get_url(thumbpath)
        return Thumb(url=url, key=key)
