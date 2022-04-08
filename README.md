# Desert
[APIDoc](https://www.apifox.cn/apidoc/shared-d0eebc73-a6eb-4636-87d4-609228585d53/)

Password: `desert_internal`

## 开发步骤：
1. 安装`Python 3.9` 和 `Redis` 环境并安装`Pycharm Professional`
2. 运行`pip install -r requirements.txt`安装依赖
3. 在项目根目录运行`python3 manage.py makemigrations player`生成`Player`的数据库表
4. 在项目根目录运行`python3 manage.py makemigrations song`生成`Song`的数据库表
5. 在项目根目录运行`python3 manage.py migrate`执行建表
6. 在项目根目录运行`python3 manage.py compliemessages`生成二进制语言文件
7. 配置并点击`Pycharm`右上角的`Run desert`运行服务器
