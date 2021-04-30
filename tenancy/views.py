from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.template import loader

from .models import File, Soft, Mirror
from .models import FileSerializer, SoftSerializer, MirrorSerializer


def index(request):
    if request.META.get("HTTP_X_FORWARDED_HOST"):
        host = 'http://' + request.META.get("HTTP_X_FORWARDED_HOST")
    else:
        host = 'http://' + request.get_host()

    return JsonResponse({
        'title': settings.APP_NAME,
        'data': [
            {
                'name': '文件列表',
                'link': host + '/files'
            },
            {
                'name': '软件列表',
                'link': host + '/softs'
            },
            {
                'name': '镜像列表',
                'link': host + '/mirrors'
            },
        ],
    })


def file(request):
    if not request.is_ajax():
        template = loader.get_template('index.html')
        return HttpResponse(template.render({}, request))
    else:
        files = File.objects.all()
        serializer = FileSerializer(instance=files, many=True)
        return JsonResponse({
            'title': settings.APP_NAME,
            'url': settings.MEDIA_URL,
            'data': serializer.data,
        })


def soft(request):
    if not request.is_ajax():
        template = loader.get_template('index.html')
        return HttpResponse(template.render({}, request))
    else:
        soft = Soft.objects.all()
        serializer = SoftSerializer(instance=soft, many=True)
        return JsonResponse({
            'title': settings.APP_NAME,
            'url': settings.MEDIA_URL,
            'data': serializer.data,
        })


def mirror(request):
    if not request.is_ajax():
        template = loader.get_template('index.html')
        return HttpResponse(template.render({}, request))
    else:
        mirrors = Mirror.objects.all()
        serializer = MirrorSerializer(instance=mirrors, many=True)
        return JsonResponse({
            'title': settings.APP_NAME,
            'url': settings.MEDIA_URL,
            'data': serializer.data,
        })
