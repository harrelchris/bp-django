#!/usr/bin/env bash

# Create virtual environment
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Update virtual environment
python3 -m pip install pip setuptools wheel --upgrade

# Install dependencies
pip install -r requirements/dev.txt --upgrade

# Create .env from example
if [ ! -f ".env" ]; then
    cp ./envs/dev.env .env
fi

# Delete the existing database
if [ -f "db.sqlite3" ]; then
    rm db.sqlite3
fi

# Initialize a clean database
python3 app/manage.py makemigrations
python3 app/manage.py migrate

# Create super users
python3 app/manage.py createsuperuser --username root --email root@email.com --noinput
python3 app/manage.py createsuperuser --username sudo --email sudo@email.com --noinput
python3 app/manage.py createsuperuser --username user --email user@email.com --noinput

# Collect static files
python3 app/manage.py collectstatic --noinput
