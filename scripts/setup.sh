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
pip install -r requirements.txt --upgrade

# Create .env from example
if [ ! -d ".env" ]; then
    cp .env.example .env
fi

# Delete the existing database
if [ ! -d "db.sqlite3" ]; then
    rm "db.sqlite3"
fi

#:: Initialize a clean database
python3 app/manage.py makemigrations
python3 app/manage.py migrate

# Delete migrations during development
# rm app\public\migrations\0001_initial.py

# Create super user
python3 app/manage.py createsuperuser --noinput
