@echo off

echo ����celery worker����......
set current_dir=%~dp0
cd %current_dir%
echo ϵͳĿ¼: %CD%
call conda activate autotest
celery -A application worker -l debug -P eventlet
@REM celery -A application worker -P eventlet

pause