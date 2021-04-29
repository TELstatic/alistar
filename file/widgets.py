from django.conf import settings
from qiniu import Auth, put_data, put_file
from django import forms
from django.template import loader


class QiniuWidgets(forms.FileInput):
    template_name = 'admin/qiniu_input.html'

    def __init__(self, attrs=None, app=None, table=None, unique_list=None):
        super(QiniuWidgets, self).__init__(attrs)
        self.unique = unique_list
        if settings.DEBUG:
            env = 'dev'
        else:
            env = 'pro'
        self.filename_prefix = '{}/{}/{}/'.format(env, app, table)

    def format_value(self, value):
        return value

    def value_from_datadict(self, data, files, name):
        file = files.get(name)
        file_data = b''.join(chunk for chunk in file.chunks())
        file_type = file.name.split('.')[-1]
        unique_filename = '_'.join(list(map(lambda x: data.get(x), self.unique)))
        file_name = self.filename_prefix + '{}_{}.{}'.format(name, unique_filename, file_type)

        auth = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
        token = auth.upload_token(settings.QINIU_BUCKET, file_name, 3600)
        put_file(token, file_name, file_data)

        return settings.QINIU_HOST + '/' + file_name

    # def render(self, name, value, attrs=None, renderer=None):
    #     context = self.get_context(name, value, attrs)
    #     return loader.get_template(self.template_name).render(context)
