from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.template import loader

from .models import File
from .models import FileSerializer


def index(request):
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
