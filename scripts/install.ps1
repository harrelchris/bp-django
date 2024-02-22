# Create virtual environment
if (-not (Test-Path .venv)) {
    python -m venv .venv
}

# Activate virtual environment
.venv\Scripts\activate

# Update virtual environment
python -m pip install pip setuptools wheel --upgrade

# Install dependencies
pip install -r requirements/dev.txt --upgrade

# Create .env from example
if (-not (Test-Path .env)) {
    Copy-Item .\envs\dev.env .env
}

# Delete the existing database
if (Test-Path db.sqlite3) {
    Remove-Item db.sqlite3
}

# Initialize a clean database
python app\manage.py makemigrations
python app\manage.py migrate

# Create super users
python app/manage.py createsuperuser --username root --email root@email.com --noinput
python app/manage.py createsuperuser --username sudo --email sudo@email.com --noinput
python app/manage.py createsuperuser --username user --email user@email.com --noinput

# Collect static files
python app/manage.py collectstatic --noinput
