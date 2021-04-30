from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.template import loader

from .models import File
from .models import FileSerializer

from .models import Soft
from .models import SoftSerializer

from .models import Mirror
from .models import MirrorSerializer


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
