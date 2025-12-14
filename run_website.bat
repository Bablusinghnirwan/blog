@echo off
echo Starting Literal Studio...
echo.
echo Access the site at: http://127.0.0.1:8000/
echo Access the Admin Studio at: http://127.0.0.1:8000/admin/
echo.
call venv\Scripts\activate
python manage.py runserver
pause
