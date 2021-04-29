from django.db import models
from django import forms
from .widgets import QiniuWidgets


class QiniuField(models.URLField):
    def __init__(self, *args, **kwargs):
        self.app = kwargs.pop('app', '')
        self.table = kwargs.pop('table', '')
        self.unique_list = kwargs.pop('unique_list', '')
        super(QiniuField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': QiniuFormField,
            'app': self.app,
            'table': self.table,
            'unique_list': self.unique_list
        }
        defaults.update(kwargs)
        return super(QiniuField, self).formfield(**defaults)


class QiniuFormField(forms.fields.URLField):
    def __init__(self, app=None, table=None, unique_list=None, **kwargs):
        kwargs.update({'widget': QiniuWidgets(app=app, table=table, unique_list=unique_list)})
        super(QiniuFormField, self).__init__(**kwargs)
