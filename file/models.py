from django.db import models
from django.utils import timezone
from rest_framework import serializers

from .storage import QiniuStorage


class File(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    name = models.CharField(max_length=200, verbose_name='文件名')
    link = models.FileField(storage=QiniuStorage(), verbose_name='文件')
    memo = models.CharField(max_length=200, verbose_name='备注')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='更新时间')

    class Meta:
        verbose_name = "文件"
        verbose_name_plural = "文件列表"

    def __str__(self):
        return self.title


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

