from django.contrib import admin
from qiniu import Auth, put_file, CdnManager, put_data
from .models import File, FileSerializer
from django.conf import settings
import os
import json


class ManagerFile(admin.ModelAdmin):
    list_display = ('title', 'name', 'link', 'memo')

    admin.site.site_title = settings.APP_NAME
    admin.site.site_header = settings.APP_NAME

    search_fields = ('title', 'name', 'memo')

    actions = ['sync', 'preview']

    def preview(self, row, request):
        return True

    def sync(self, row, request):
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        bucket = settings.QINIU_BUCKET
        host = settings.QINIU_HOST

        auth = Auth(access_key, secret_key)

        filename = __file__.replace(os.path.basename(__file__), '') + '/templates/index.html'

        uploads = [
            'files/index.html',
            'files.json',
        ]

        token = auth.upload_token(bucket, uploads[0], 3600)

        put_file(token, uploads[0], filename)

        files = File.objects.all()

        serializer = FileSerializer(instance=files, many=True)

        token = auth.upload_token(bucket, uploads[1], 3600)

        put_data(token, uploads[1], json.dumps({
            'title': settings.APP_NAME,
            'url': settings.MEDIA_URL,
            'data': serializer.data,
        }))

        cdnManager = CdnManager(auth)

        for i in range(len(uploads)):
            uploads[i] = host + '/' + uploads[i]

        uploads.append(host + '/files/')

        cdnManager.refresh_urls(uploads)

        return True

    sync.short_description = '同步'
    sync.icon = 'el-icon-refresh'
    sync.type = 'warning'
    sync.style = 'color:rainbow;'
    sync.confirm = '确认同步数据?'

    preview.short_description = '查看'
    preview.icon = 'el-icon-link'
    preview.type = 'primary'
    preview.style = 'color:rainbow;'
    preview.action_type = 2
    preview.action_url = settings.QINIU_HOST + '/files/'

    class Meta:
        verbose_name = "文件"

admin.site.register(File, ManagerFile)
