import re

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from qiniu import Auth, put_data


class QiniuStorage(FileSystemStorage):
    def path(self, name):
        return settings.QINIU_HOST + '/' + name

    def url(self, name):
        if re.match(r'^https?:/{2}\w.+$', name):
            return name
        else:
            return self.path(name)

    def _save(self, name, content):
        filename = self.generate_filename(name).replace('\\', '/')
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        bucket = settings.QINIU_BUCKET

        auth = Auth(access_key, secret_key)

        token = auth.upload_token(bucket, filename, 3600)

        put_data(token, filename, content)

        return self.path(filename)
