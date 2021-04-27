# --- coding: utf-8 ---
from qiniu import Auth, put_file, CdnManager
import configparser

print('---------------------------------')
print('#                                ')
print('# 七牛软件、系统镜像库')
print('#     _    _ _     _')
print('#    / \  | (_)___| |_ __ _ _ __')
print('#   / _ \ | | / __| __/ _` | `__|')
print('#  / ___ \| | \__ \ || (_| | |')
print('# /_/   \_\_|_|___/\__\__,_|_|')

conf = configparser.ConfigParser()
conf.read('config.ini')

Accesskey = conf.get("Qiniu", "Accesskey")
Secretkey = conf.get("Qiniu", "Secretkey")
Bucket = conf.get("Qiniu", "Bucket")
Host = conf.get("Qiniu", "Host")

auth = Auth(Accesskey, Secretkey)

files = [
    './src/index.html',
    './src/softs.json',
    './src/mirrors.json',
]

uploads = []

refreshFiles = [
    Host + '/mirrors/',
    Host + '/mirrors.json',
    Host + '/mirrors/index.html',
    Host + '/softs/',
    Host + '/softs.json',
    Host + '/softs/index.html',
]

for file in files:
    if file == './src/index.html':
        uploads.append({
            'key': 'mirrors/index.html',
            'file': file,
            'token': auth.upload_token(Bucket, 'mirrors/index.html', 60)
        })

        uploads.append({
            'key': 'softs/index.html',
            'file': file,
            'token': auth.upload_token(Bucket, 'softs/index.html', 60)
        })
    else:
        uploads.append({
            'key': file.replace('./src/', ''),
            'file': file,
            'token': auth.upload_token(Bucket, file.replace('./src/', ''), 60)
        })

for item in uploads:
    ret, info = put_file(item['token'], item['key'], item['file'])

print('')
print('文件上传成功')
cdnManager = CdnManager(auth)
result = cdnManager.refresh_urls(refreshFiles)

if 200 == result[0]['code']:
    print('文件刷新成功')
else:
    print('文件刷新失败')
