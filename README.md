# Alistar

> 基于 Django 的文件备份系统

将备份文件上传到七牛云后,手动生成对应的预览界面. 

## 开发与部署

0. `git clone https://github.com/telstatic/alistar.git`
1. `cd src && cp settings.py.example settings.py` 并填写配置
2. `python manage.py createsuperuser`
3. `python manage.py runserver`
4. 访问 `http://127.0.0.1:8000` `http://127.0.0.1:8000/admin` 
