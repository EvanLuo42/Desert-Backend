from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from qcloud_cos import CosConfig, CosS3Client

from desert import settings, constant
from desert.utils import generate_filename

secret_id = settings.COS_SECRET_ID
secret_key = settings.COS_SECRET_KEY
region = settings.REGION
bucket = settings.BUCKET
config = CosConfig(Region=region, Secret_id=secret_id, Secret_key=secret_key)
client = CosS3Client(config)


@deconstructible
class SongStorage(Storage):
    def save(self, name, content, max_length=None):
        client.put_object(
            Bucket=bucket,
            Key=constant.SONG_STORAGE_PATH + name,
            Body=content.read()
        )
        return name

    def url(self, name):
        file_url = client.get_presigned_url(
            Method=constant.GET_METHOD,
            Bucket=bucket,
            Key=constant.SONG_STORAGE_PATH + name,
            Expired=120
        )
        return str(file_url)

    def generate_filename(self, filename):
        return generate_filename(filename, constant.SONG_EXTENSION)

    def delete(self, name):
        client.delete_object(bucket, constant.SONG_STORAGE_PATH + name)
        return name


@deconstructible
class ImageStorage(Storage):
    def save(self, name, content, max_length=None):
        client.put_object(
            Bucket=bucket,
            Key=constant.IMAGE_STORAGE_PATH + name,
            Body=content.read()
        )
        return name

    def url(self, name):
        file_url = client.get_presigned_url(
            Method=constant.GET_METHOD,
            Bucket=bucket,
            Key=constant.IMAGE_STORAGE_PATH + name,
            Expired=120
        )
        return str(file_url)

    def generate_filename(self, filename):
        return generate_filename(filename, constant.IMAGE_EXTENSION)

    def delete(self, name):
        client.delete_object(bucket, constant.IMAGE_STORAGE_PATH + name)
        return name
