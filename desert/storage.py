import time
from hashlib import sha1

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
        filename = self.generate_filename(name)
        client.put_object(
            Bucket=bucket,
            Key='song/' + filename,
            Body=content.read()
        )
        return filename

    def generate_filename(self, filename):
        return filename + '_' + sha1(str(time.time()).encode('utf-8')).hexdigest()

    def url(self, name):
        file_url = client.get_object_url(bucket, 'song/' + name)
        return str(file_url)


