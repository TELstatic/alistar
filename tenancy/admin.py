import json
import os
import re

from django.conf import settings
from django.contrib import admin
from django.http import JsonResponse
from qiniu import Auth, put_data, BucketManager, build_batch_delete
from qiniu import put_file, CdnManager
from simpleui.admin import AjaxAdmin

from .models import File, FileSerializer
from .models import Mirror, MirrorSerializer
from .models import Soft, SoftSerializer


class ManagerFile(AjaxAdmin):
    list_display = ('title', 'name', 'link', 'memo')

    admin.site.site_title = settings.APP_NAME
    admin.site.site_header = settings.APP_NAME

    def delete_queryset(self, request, queryset):
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        bucket = settings.QINIU_BUCKET
        host = settings.QINIU_HOST

        auth = Auth(access_key, secret_key)

        bucketManager = BucketManager(auth)

        keys = []

        for item in queryset:
            filename = str(item.link)
            if (filename.startswith(host)):
                filename = filename.replace(host + '/', '')
            else:
                if re.match(r'^https?:/{2}\w.+$', filename):
                    continue
            keys.append(filename)

        bucketManager.batch(build_batch_delete(bucket, keys))

        queryset.delete()

    def delete_model(self, request, obj):
        filename = str(obj.link)
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        bucket = settings.QINIU_BUCKET
        host = settings.QINIU_HOST

        auth = Auth(access_key, secret_key)

        bucketManager = BucketManager(auth)

        obj.delete()

        if (filename.startswith(host)):
            bucketManager.delete(bucket, filename.replace(host + '/', ''))
            return True

        if not re.match(r'^https?:/{2}\w.+$', filename):
            bucketManager.delete(bucket, filename)
            return True

        return True

    search_fields = ('title', 'name', 'memo')

    actions = ['sync', 'preview', 'review', 'fetch']

    def fetch(self, request, queryset):
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        bucket = settings.QINIU_BUCKET
        host = settings.QINIU_HOST

        auth = Auth(access_key, secret_key)
        bucketManager = BucketManager(auth)

        url = request.POST['link']
        key = 'files/' + os.path.basename(url)

        bucketManager.fetch(url, bucket, key)

        soft = Soft()

        soft.title = request.POST['title']
        soft.name = request.POST['name']
        soft.link = host + '/' + key
        soft.memo = request.POST['memo']

        soft.save()

        return JsonResponse({
            'status': 'success',
            'msg': '???????????????'
        })

    fetch.short_description = '??????'
    fetch.icon = 'el-icon-link'
    fetch.type = 'primary'
    fetch.style = 'color:rainbow;'

    fetch.layer = {
        'title': '??????????????????',
        'tips': '????????????????????????',
        'confirm_button': '??????',
        'cancel_button': '??????',
        'width': '50%',
        'params': [
            {
                'type': 'input',
                'key': 'title',
                'label': '??????',
                'require': True
            },
            {
                'type': 'input',
                'key': 'name',
                'label': '??????',
                'require': True
            },
            {
                'type': 'input',
                'key': 'link',
                'label': '??????',
                'require': True
            },
            {
                'type': 'input',
                'key': 'memo',
                'label': '??????',
                'require': True
            },
        ],
    }

    def preview(self, request, queryset):
        return True

    def review(self, request, queryset):
        return True

    def sync(self, request, queryset):
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
            'msg': '???????????????'
        })

    sync.short_description = '??????'
    sync.icon = 'el-icon-refresh'
    sync.type = 'warning'
    sync.style = 'color:rainbow;'

    sync.layer = {
        'title': '???????????????????',
        'tips': '?????????,?????????????????????????????????json????????????????????????????????????',
        'confirm_button': '??????',
        'cancel_button': '??????',
        'width': '50%',
    }

    preview.short_description = '??????'
    preview.icon = 'el-icon-link'
    preview.type = 'success'
    preview.style = 'color:rainbow;'
    preview.action_type = 2
    preview.action_url = settings.QINIU_HOST + '/files/'

    review.short_description = '??????'
    review.icon = 'el-icon-view'
    review.type = 'info'
    review.style = 'color:rainbow;'
    review.action_type = 2
    review.action_url = '/files'


class ManagerSoft(AjaxAdmin):
    list_display = ('title', 'name', 'link', 'memo')

    def delete_queryset(self, request, queryset):
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        bucket = settings.QINIU_BUCKET
        host = settings.QINIU_HOST

        auth = Auth(access_key, secret_key)

        bucketManager = BucketManager(auth)

        keys = []

        for item in queryset:
            filename = str(item.link)
            if (filename.startswith(host)):
                filename = filename.replace(host + '/', '')
            else:
                if re.match(r'^https?:/{2}\w.+$', filename):
                    continue
            keys.append(filename)

        bucketManager.batch(build_batch_delete(bucket, keys))

        queryset.delete()

    def delete_model(self, request, obj):
        filename = str(obj.link)
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        bucket = settings.QINIU_BUCKET
        host = settings.QINIU_HOST

        auth = Auth(access_key, secret_key)

        bucketManager = BucketManager(auth)

        obj.delete()

        if (filename.startswith(host)):
            bucketManager.delete(bucket, filename.replace(host + '/', ''))
            return True

        if not re.match(r'^https?:/{2}\w.+$', filename):
            bucketManager.delete(bucket, filename)
            return True

        return True

    admin.site.site_title = settings.APP_NAME
    admin.site.site_header = settings.APP_NAME

    search_fields = ('title', 'name', 'memo')

    actions = ['sync', 'preview', 'review', 'fetch']

    def preview(self, request, queryset):
        return True

    def review(self, request, queryset):
        return True

    def sync(self, request, queryset):
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
            'msg': '???????????????'
        })

    sync.short_description = '??????'
    sync.icon = 'el-icon-refresh'
    sync.type = 'warning'
    sync.style = 'color:rainbow;'

    sync.layer = {
        'title': '???????????????????',
        'tips': '?????????,?????????????????????????????????json????????????????????????????????????',
        'confirm_button': '??????',
        'cancel_button': '??????',
        'width': '50%',
    }

    def fetch(self, request, queryset):
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        bucket = settings.QINIU_BUCKET
        host = settings.QINIU_HOST

        auth = Auth(access_key, secret_key)
        bucketManager = BucketManager(auth)

        url = request.POST['link']
        key = 'softs/' + os.path.basename(url)

        bucketManager.fetch(url, bucket, key)

        soft = Soft()

        soft.title = request.POST['title']
        soft.name = request.POST['name']
        soft.link = host + '/' + key
        soft.memo = request.POST['memo']

        soft.save()

        return JsonResponse({
            'status': 'success',
            'msg': '???????????????'
        })

    fetch.short_description = '??????'
    fetch.icon = 'el-icon-link'
    fetch.type = 'primary'
    fetch.style = 'color:rainbow;'

    fetch.layer = {
        'title': '??????????????????',
        'tips': '????????????????????????',
        'confirm_button': '??????',
        'cancel_button': '??????',
        'width': '50%',
        'params': [
            {
                'type': 'input',
                'key': 'title',
                'label': '??????',
                'require': True
            },
            {
                'type': 'input',
                'key': 'name',
                'label': '??????',
                'require': True
            },
            {
                'type': 'input',
                'key': 'link',
                'label': '??????',
                'require': True
            },
            {
                'type': 'input',
                'key': 'memo',
                'label': '??????',
                'require': True
            },
        ],
    }

    preview.short_description = '??????'
    preview.icon = 'el-icon-link'
    preview.type = 'success'
    preview.style = 'color:rainbow;'
    preview.action_type = 2
    preview.action_url = settings.QINIU_HOST + '/softs/'

    review.short_description = '??????'
    review.icon = 'el-icon-view'
    review.type = 'info'
    review.style = 'color:rainbow;'
    review.action_type = 2
    review.action_url = '/softs'


class ManagerMirror(AjaxAdmin):
    list_display = ('title', 'name', 'link', 'memo')

    admin.site.site_title = settings.APP_NAME
    admin.site.site_header = settings.APP_NAME

    def delete_queryset(self, request, queryset):
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        bucket = settings.QINIU_BUCKET
        host = settings.QINIU_HOST

        auth = Auth(access_key, secret_key)

        bucketManager = BucketManager(auth)

        keys = []

        for item in queryset:
            filename = str(item.link)
            if (filename.startswith(host)):
                filename = filename.replace(host + '/', '')
            else:
                if re.match(r'^https?:/{2}\w.+$', filename):
                    continue
            keys.append(filename)

        bucketManager.batch(build_batch_delete(bucket, keys))

        queryset.delete()

    def delete_model(self, request, obj):
        filename = str(obj.link)
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        bucket = settings.QINIU_BUCKET
        host = settings.QINIU_HOST

        auth = Auth(access_key, secret_key)

        bucketManager = BucketManager(auth)

        obj.delete()

        if (filename.startswith(host)):
            bucketManager.delete(bucket, filename.replace(host + '/', ''))
            return True

        if not re.match(r'^https?:/{2}\w.+$', filename):
            bucketManager.delete(bucket, filename)
            return True

        return True

    search_fields = ('title', 'name', 'memo')

    actions = ['sync', 'preview', 'review', 'fetch']

    def fetch(self, request, queryset):
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        bucket = settings.QINIU_BUCKET
        host = settings.QINIU_HOST

        auth = Auth(access_key, secret_key)
        bucketManager = BucketManager(auth)

        url = request.POST['link']
        key = 'mirrors/' + os.path.basename(url)

        bucketManager.fetch(url, bucket, key)

        soft = Soft()

        soft.title = request.POST['title']
        soft.name = request.POST['name']
        soft.link = host + '/' + key
        soft.memo = request.POST['memo']

        soft.save()

        return JsonResponse({
            'status': 'success',
            'msg': '???????????????'
        })

    fetch.short_description = '??????'
    fetch.icon = 'el-icon-link'
    fetch.type = 'primary'
    fetch.style = 'color:rainbow;'

    fetch.layer = {
        'title': '??????????????????',
        'tips': '????????????????????????',
        'confirm_button': '??????',
        'cancel_button': '??????',
        'width': '50%',
        'params': [
            {
                'type': 'input',
                'key': 'title',
                'label': '??????',
                'require': True
            },
            {
                'type': 'input',
                'key': 'name',
                'label': '??????',
                'require': True
            },
            {
                'type': 'input',
                'key': 'link',
                'label': '??????',
                'require': True
            },
            {
                'type': 'input',
                'key': 'memo',
                'label': '??????',
                'require': True
            },
        ],
    }

    def preview(self, request, queryset):
        return True

    def review(self, request, queryset):
        return True

    def sync(self, request, queryset):
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
            'msg': '???????????????'
        })

    sync.short_description = '??????'
    sync.icon = 'el-icon-refresh'
    sync.type = 'warning'
    sync.style = 'color:rainbow;'

    sync.layer = {
        'title': '???????????????????',
        'tips': '?????????,?????????????????????????????????json????????????????????????????????????',
        'confirm_button': '??????',
        'cancel_button': '??????',
        'width': '50%',
    }

    preview.short_description = '??????'
    preview.icon = 'el-icon-link'
    preview.type = 'success'
    preview.style = 'color:rainbow;'
    preview.action_type = 2
    preview.action_url = settings.QINIU_HOST + '/mirrors/'

    review.short_description = '??????'
    review.icon = 'el-icon-view'
    review.type = 'info'
    review.style = 'color:rainbow;'
    review.action_type = 2
    review.action_url = '/mirrors'


admin.site.register(Soft, ManagerSoft)
admin.site.register(Mirror, ManagerMirror)
admin.site.register(File, ManagerFile)
