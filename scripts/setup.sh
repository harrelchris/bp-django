#!/usr/bin/env bash

VENV=".venv"

# Create virtual environment
if [ ! -d "$VENV" ]; then
    python3 -m venv $VENV
fi

# Activate virtual environment
source $VENV/bin/activate

# Update virtual environment
python3 -m pip install pip setuptools wheel --upgrade

# Install dependencies
pip install -r requirements/dev.txt --upgrade

# Create .env from example
if [ ! -d ".env" ]; then
    cp envs/dev.env .env
fi

# Delete the existing database
if [ ! -d "db.sqlite3" ]; then
    rm "db.sqlite3"
fi

# Initialize a clean database
python3 app/manage.py makemigrations
python3 app/manage.py migrate

# Create super users
python3 app/manage.py createsuperuser --username root --email root@email.com --noinput
python3 app/manage.py createsuperuser --username sudo --email sudo@email.com --noinput
python3 app/manage.py createsuperuser --username user --email user@email.com --noinput

# Collect static files
# python3 app/manage.py collectstatic --noinput

# Install initial data
# python3 app/manage.py loaddata app/fixtures/data.json

# Delete migrations during development
# rm app\public\migrations\0001_initial.py
