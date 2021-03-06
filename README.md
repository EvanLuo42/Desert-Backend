# Desert
[APIDoc](https://www.apifox.cn/apidoc/shared-d0eebc73-a6eb-4636-87d4-609228585d53/)

Password: `desert_internal`

## 项目架构：
<img src="https://s2.loli.net/2022/04/20/RomNWgkw32sIQiS.png" width="700" height="500" alt="架构图"/>

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
3. [下载docker-compose.yml](https://desert-1258493860.cos.ap-shanghai.myqcloud.com/docker-compose.yml)
4. 运行`docker login --username={{ username }} ccr.ccs.tencentyun.com --password={{ password }}` ( Github的项目secrets 中的 username 和 password )
5. 运行`docker pull ccr.ccs.tencentyun.com/desert/desert-backend:latest`
6. 运行`docker pull redis:alpine`
7. 运行`docker-compose up -d docker-compose.yml`
8. 配置`nginx`

## 创建`superuser`
1. 在`desert`项目根目录运行`python3 manage.py createsuperuser`
2. 填写参数
3. 记下输出的`setup key`并拷贝到`Google Authenticator`等应用中
4. 访问管理页并登陆


# ___登入后台修改的时候一定要记得开 `SafeGuard Mode`___

## 更新剧情
1. 登入后台
2. 点击左侧`剧情`
3. 点击右上角`+Add`
4. 填写参数
5. 点击右下角`Save`

## 更新曲目
1. 登入后台
2. 确保已经添加了对应的剧情和章节
3. 点击左侧`曲目`
4. 点击右上角`+Add`
5. 填写参数
6. 点击右下角`Save`

## 更新角色
1. 登入后台
2. 点击左侧角色
3. 点击右上角`+Add`
4. 填写参数
5. 点击右下角`Save`

## 添加兑换码
1. 登入后台
2. 点击左侧`物品兑换`
3. 填写参数 ( item_id 应为 `character_` + `角色id` 或 `物品种类`( 目前只有character ) + `对应种类表id` )
4. 点击右下角`Save`
