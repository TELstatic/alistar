from django.urls import path

from . import views

urlpatterns = [
    path('files', views.file, name='file.index'),
    path('softs', views.soft, name='soft.index'),
    path('mirrors', views.mirror, name='mirror.index'),
    path('', views.index, name='index'),
]
