from pathlib import Path

import environ

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent

env.read_env(BASE_DIR / ".env")

LOG_ROOT = Path(env.str("LOG_ROOT"))

LOG_ROOT.mkdir(exist_ok=True)

accesslog = str(LOG_ROOT / "gunicorn.access.log")
errorlog = str(LOG_ROOT / "gunicorn.error.log")

bind = "localhost:8000"
chdir = "app"
daemon = False
workers = 2
wsgi_app = "core.wsgi:application"
