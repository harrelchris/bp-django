import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
LOGS = ROOT / "logs"

LOGS.mkdir(exist_ok=True)

accesslog = str(LOGS / "gunicorn.access.log")
errorlog = str(LOGS / "gunicorn.error.log")

bind = "localhost:8000"
chdir = "app"
daemon = False
workers = 2
wsgi_app = "core.wsgi:application"
