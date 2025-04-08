# 自动化测试平台

## 平台简介

AutoTestPlat是基于[django-vue3-admin](https://gitee.com/huge-dream/django-vue3-admin.git)平台进行开发的自动化测试平台，目前支持web自动化测试，支持定时任务管理。

## 准备工作

```
Python >= 3.11.0 (最低3.9+版本)
nodejs >= 16.0
Mysql >= 8.0 (可选，默认数据库sqlite3，支持5.7+，推荐8.0版本)
Redis (最新版)
```

## 后端

1. 进入项目目录: `cd backend`
2. 进入配置文件目录，复制模板配置文件env.example.py，重命名为env.py，在 env.py 中配置数据库信息

   ```
   cd conf
   cp env.example.py env.py
   ```

   mysql数据库版本建议：8.0
   mysql数据库字符集：utf8mb4
3. 安装依赖环境

```
python -m pip install -r requirements.txt
```

4. 执行迁移命令：

```
python manage.py makemigrations
python manage.py migrate
```

5. 初始化数据

```
python manage.py init
```

4. 启动项目

```
python manage.py runserver 0.0.0.0:8000
```

或使用 uvicorn :

```
uvicorn application.asgi:application --port 8000 --host 0.0.0.0 --workers 8
```

### celery定时任务

初始化数据库

```
python manage.py  makemigrations dvadmin3_celery
python manage.py  migrate dvadmin3_celery
python manage.py  makemigrations django_celery_results
python manage.py  migrate django_celery_results
```

celery启动

```
# windows需要加-P eventlet参数
celery -A application worker -l debug -P eventlet
celery -A application beat -l debug
```



### web自动化工具

支持selenium和playwright


#### selenium

使用selenium，需要配置谷歌浏览器驱动,[谷歌浏览器驱动下载地址](https://googlechromelabs.github.io/chrome-for-testing/#stable),下载后放置到一个合适的配置，然后配置电脑的环境变量即可。
打开一个cmd, 测试驱动是否正常。

```
chromedriver -h
```


#### playwright

浏览器安装

```
playwright install # 安装支持的浏览器：cr, chromium, ff, firefox, wk 和 webkit
playwright install chromium # 安装指定的chromium浏览器
```


## 前端

### 安装依赖

```bash
# 进入项目目录
cd web

# 安装依赖
npm install yarn
yarn install --registry=https://registry.npmmirror.com
```

### 开发环境启动

```
yarn run dev
# 浏览器访问 http://localhost:8080
# 配置文件: .env.development
```

### 编译与部署

#### 本地编译与部署

```
yarn run build:local
# 配置文件: .env.local_prod
```

编译后的静态文件会发布到 `backend/templates/web/ 目录下, `启动后端后，访问  `http://后端IP:后端端口/web/`，就可以访问到前端了，这样可以实现前后端统一部署，就不用额外的独立部署前端了。

#### 前端独立编译与部署

```
yarn run build
# 配置文件: .env.production
```

前端独立部署需要修改配置文件，主要修改 `VITE_API_URL参数,把这个参数修改为实际的api地址`；编译后可以使用nginx进行部署。

## 访问项目

- 访问地址：[http://localhost:8080](http://localhost:8080) (默认为此地址，如有修改请按照配置文件)
- 账号：`superadmin` 密码：`admin123456`

# 参考链接

gitee地址：[https://gitee.com/huge-dream/django-vue3-admin](https://gitee.com/huge-dream/django-vue3-admin)👩‍👦‍👦
