@echo off

echo 启动celery worker服务......
set current_dir=%~dp0
cd %current_dir%
echo 系统目录: %CD%
call conda activate autotest
celery -A application worker -l debug -P eventlet
@REM celery -A application worker -P eventlet

pause