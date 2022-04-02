import time
from hashlib import md5

from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from qcloud_cos import CosConfig, CosS3Client

from desert import settings

secret_id = settings.COS_SECRET_ID
secret_key = settings.COS_SECRET_KEY
region = settings.REGION
bucket = settings.BUCKET
config = CosConfig(Region=region, Secret_id=secret_id, Secret_key=secret_key)
client = CosS3Client(config)
host = 'https://' + bucket + '.cos.' + region + '.myqcloud.com/'


@deconstructible
class TencentStorage(Storage):
    def save(self, name, content, max_length=None):
        client.put_object(
            Bucket=bucket,
            Key='song/' + self.generate_filename(name),
            Body=content.read()
        )
        return name

    def url(self, name):
        file_url = client.get_object_url(bucket, 'song/' + name)
        return str(file_url)

    def generate_filename(self, filename):
        return md5((filename + str(time.time_ns())).encode('utf-8')).hexdigest()
