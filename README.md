# Desert
[APIDoc](https://www.apifox.cn/apidoc/shared-d0eebc73-a6eb-4636-87d4-609228585d53/)

Password: `desert_internal`

## 开发步骤：
1. 安装`Python 3.9` 和 `Redis` 环境并安装`Pycharm Professional`
2. 运行`pip install -r requirements.txt`安装依赖
3. 在项目根目录运行`python3 manage.py makemigrations player`生成`Player`的数据库表
4. 在项目根目录运行`python3 manage.py makemigrations song`生成`Song`的数据库表
5. 在项目根目录运行`python3 manage.py makemigrations plot`生成`Plot`的数据库表
6. 在项目根目录运行`python3 manage.py migrate`执行建表
7. 在项目根目录运行`python3 manage.py compliemessages`生成二进制语言文件
8. 在项目根目录运行`gunicorn desert.wsgi -w 5 -k gevent -b 0.0.0.0:8000`运行服务器

## 部署步骤：
1. 安装`docker-ce`
2. 安装`docker-compose`
3. [下载docker-compose.yml](https://desert-1258493860.cos.ap-shanghai.myqcloud.com/docker-compose.yml?q-sign-algorithm=sha1&q-ak=AKIDe5rs5YZIs87JMWawvbBEoOUTu5MkGADswb86IZWNIwYOuzF0g1Df0GhSZOykwkUL&q-sign-time=1650001415;1650005015&q-key-time=1650001415;1650005015&q-header-list=&q-url-param-list=&q-signature=d5d0827873e8d10d2084e5594007554b12233428&x-cos-security-token=PqyS51gyS0glU1rlYh1wsI7Ljh83vHvaed2c71a65439aae7d85a179907cf2b38AWiP4ebnKgOYjtste3wdeu5IgsGC9RJX6Qru8CQCx_DSKj2mUfT5k5mzkWqVoxs4WpemDzmWpZ_nYmZ1P9msKlG0zsOMB_iWzKLvV4Akuic2XwSpTTIInl_MFFU1TgP_zitV6OBo0zN0JRQ2uiPEccW8EU6UJ8EJZKBgbzp6MFeGp6gBVLbuoWA8kmH1mID0dRKrJSBv0eh8glXHGoSWKQ&response-content-type=application%2Foctet-stream&response-content-disposition=attachment)
4. 运行`docker login --username=100009002268 ccr.ccs.tencentyun.com --password=Desert_stuff22`
5. 运行`docker pull ccr.ccs.tencentyun.com/desert/desert-backend:latest`
6. 运行`docker pull redis:alpine`
7. 运行`docker-compose up -d docker-compose.yml`
8. 配置`nginx`
