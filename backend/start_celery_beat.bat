@echo off

echo ����celery beat����......
set current_dir=%~dp0
cd %current_dir%
echo ϵͳĿ¼: %CD%
call conda activate autotest
celery -A application beat -l debug
@REM celery -A application beat

pause