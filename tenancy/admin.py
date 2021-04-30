from django.contrib import admin
from qiniu import Auth, put_file, CdnManager, put_data
from .models import File, FileSerializer
from .models import Mirror, MirrorSerializer
from .models import Soft, SoftSerializer
from django.conf import settings
import os
import json
from django.utils.html import format_html
from django.http import JsonResponse
from simpleui.admin import AjaxAdmin


class ManagerFile(AjaxAdmin):
    list_display = ('title', 'name', 'link', 'memo')

    admin.site.site_title = settings.APP_NAME
    admin.site.site_header = settings.APP_NAME

    search_fields = ('title', 'name', 'memo')

    actions = ['sync', 'preview', 'review']

    def preview(self, row, request):
        return True

    def review(self, row, request):
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

        return JsonResponse({
            'status': 'success',
            'msg': '处理成功！'
        })

    sync.short_description = '同步'
    sync.icon = 'el-icon-refresh'
    sync.type = 'warning'
    sync.style = 'color:rainbow;'

    sync.layer = {
        'title': '确认同步数据?',
        'tips': '使用后,系统会将本地数据库生成json后更新七牛对应的静态文件',
        'confirm_button': '确认',
        'cancel_button': '取消',
        'width': '50%',
    }

    preview.short_description = '查看'
    preview.icon = 'el-icon-link'
    preview.type = 'primary'
    preview.style = 'color:rainbow;'
    preview.action_type = 2
    preview.action_url = settings.QINIU_HOST + '/files/'

    review.short_description = '预览'
    review.icon = 'el-icon-link'
    review.type = 'primary'
    review.style = 'color:rainbow;'
    review.action_type = 2
    review.action_url = '/files'


class ManagerSoft(AjaxAdmin):
    list_display = ('title', 'name', 'link', 'memo')

    def url(self, obj):
        return format_html('<a href="' + str(obj.link) + '">' + str(obj.link) + '</a>')

    url.short_description = '链接'

    admin.site.site_title = settings.APP_NAME
    admin.site.site_header = settings.APP_NAME

    search_fields = ('title', 'name', 'memo')

    actions = ['sync', 'preview', 'review']

    def preview(self, row, request):
        return True

    def review(self, row, request):
        return True

    def sync(self, row, request):
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        bucket = settings.QINIU_BUCKET
        host = settings.QINIU_HOST

        auth = Auth(access_key, secret_key)

        filename = __file__.replace(os.path.basename(__file__), '') + '/templates/index.html'

        uploads = [
            'softs/index.html',
            'softs.json',
        ]

        token = auth.upload_token(bucket, uploads[0], 3600)

        put_file(token, uploads[0], filename)

        softs = Soft.objects.all()

        serializer = SoftSerializer(instance=softs, many=True)

        token = auth.upload_token(bucket, uploads[1], 3600)

        put_data(token, uploads[1], json.dumps({
            'title': settings.APP_NAME,
            'url': settings.MEDIA_URL,
            'data': serializer.data,
        }))

        cdnManager = CdnManager(auth)

        for i in range(len(uploads)):
            uploads[i] = host + '/' + uploads[i]

        uploads.append(host + '/softs/')

        cdnManager.refresh_urls(uploads)

        return JsonResponse({
            'status': 'success',
            'msg': '处理成功！'
        })

    sync.short_description = '同步'
    sync.icon = 'el-icon-refresh'
    sync.type = 'warning'
    sync.style = 'color:rainbow;'

    sync.layer = {
        'title': '确认同步数据?',
        'tips': '使用后,系统会将本地数据库生成json后更新七牛对应的静态文件',
        'confirm_button': '确认',
        'cancel_button': '取消',
        'width': '50%',
    }

    preview.short_description = '查看'
    preview.icon = 'el-icon-link'
    preview.type = 'primary'
    preview.style = 'color:rainbow;'
    preview.action_type = 2
    preview.action_url = settings.QINIU_HOST + '/softs/'

    review.short_description = '预览'
    review.icon = 'el-icon-link'
    review.type = 'primary'
    review.style = 'color:rainbow;'
    review.action_type = 2
    review.action_url = '/softs'


class ManagerMirror(AjaxAdmin):
    list_display = ('title', 'name', 'link', 'memo')

    admin.site.site_title = settings.APP_NAME
    admin.site.site_header = settings.APP_NAME

    search_fields = ('title', 'name', 'memo')

    actions = ['sync', 'preview', 'review']

    def preview(self, row, request):
        return True

    def review(self, row, request):
        return True

    def sync(self, row, request):
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        bucket = settings.QINIU_BUCKET
        host = settings.QINIU_HOST

        auth = Auth(access_key, secret_key)

        filename = __file__.replace(os.path.basename(__file__), '') + '/templates/index.html'

        uploads = [
            'mirrors/index.html',
            'mirrors.json',
        ]

        token = auth.upload_token(bucket, uploads[0], 3600)

        put_file(token, uploads[0], filename)

        mirrors = Mirror.objects.all()

        serializer = MirrorSerializer(instance=mirrors, many=True)

        token = auth.upload_token(bucket, uploads[1], 3600)

        put_data(token, uploads[1], json.dumps({
            'title': settings.APP_NAME,
            'url': settings.MEDIA_URL,
            'data': serializer.data,
        }))

        cdnManager = CdnManager(auth)

        for i in range(len(uploads)):
            uploads[i] = host + '/' + uploads[i]

        uploads.append(host + '/mirrors/')

        cdnManager.refresh_urls(uploads)

        return JsonResponse({
            'status': 'success',
            'msg': '处理成功！'
        })

    sync.short_description = '同步'
    sync.icon = 'el-icon-refresh'
    sync.type = 'warning'
    sync.style = 'color:rainbow;'

    sync.layer = {
        'title': '确认同步数据?',
        'tips': '使用后,系统会将本地数据库生成json后更新七牛对应的静态文件',
        'confirm_button': '确认',
        'cancel_button': '取消',
        'width': '50%',
    }

    preview.short_description = '查看'
    preview.icon = 'el-icon-link'
    preview.type = 'primary'
    preview.style = 'color:rainbow;'
    preview.action_type = 2
    preview.action_url = settings.QINIU_HOST + '/mirrors/'

    review.short_description = '预览'
    review.icon = 'el-icon-link'
    review.type = 'primary'
    review.style = 'color:rainbow;'
    review.action_type = 2
    review.action_url = '/mirrors'


admin.site.register(Soft, ManagerSoft)
admin.site.register(Mirror, ManagerMirror)
admin.site.register(File, ManagerFile)
