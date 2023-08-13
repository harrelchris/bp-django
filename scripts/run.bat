@echo off

:: Activate virtual environment
call .venv\Scripts\activate

python app\manage.py runserver localhost:80
