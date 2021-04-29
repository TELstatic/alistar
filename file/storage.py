from django.core.files.storage import FileSystemStorage
from django.conf import settings
from qiniu import Auth, put_data


class QiniuStorage(FileSystemStorage):
    def path(self, name):
        return settings.QINIU_HOST + '/' + name

    def _save(self, name, content):
        filename = 'files/' + name.replace('\\', '/')
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        bucket = settings.QINIU_BUCKET

        auth = Auth(access_key, secret_key)

        token = auth.upload_token(bucket, filename, 3600)

        put_data(token, filename, content)

        return self.path(filename)
