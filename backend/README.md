## 常用命令

### 初始化文件生成

项目部署时，需要生成一些初始化数据，这些初始化数据放置在 `dvadmin\system\fixtures` 目录, 如果想修改这些初始化数据，可以手动修改，也可以从数据库中生成这些初始化数据

生成所有初始化数据

```
python manage.py generate_init_json
```

生成系统菜单的初始化数据

```
python manage.py generate_init_json menu
```

注意：生成的parent值有可能是错误的，不过初始化时会纠正回来，导入数据库重新导出初始化数据，这样parent值就正常了


### 数据库初始化

dvadmin.system应用数据库初始化时，使用以下命令：

```
python manage.py  makemigrations system
python manage.py  migrate system
```
