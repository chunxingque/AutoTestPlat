@echo off

echo 启动后端服务......
set current_dir=%~dp0
cd %current_dir%
echo 系统目录: %CD%
call conda activate autotest
python manage.py runserver 0.0.0.0:8000

pause