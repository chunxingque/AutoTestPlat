@echo off

echo 启动celery beat服务......
set current_dir=%~dp0
cd %current_dir%
echo 系统目录: %CD%
call conda activate autotest
celery -A application beat -l debug
@REM celery -A application beat

pause