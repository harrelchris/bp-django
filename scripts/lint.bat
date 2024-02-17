@echo off

:: Activate virtual environment
call .venv\Scripts\activate

python -m black app

python -m flake8 app

python -m isort .
