@echo off

echo ������˷���......
set current_dir=%~dp0
cd %current_dir%
echo ϵͳĿ¼: %CD%
call conda activate autotest
python manage.py runserver 0.0.0.0:8000

pause