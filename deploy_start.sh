#!/usr/bin/env bash
set -e

# Run migrations, collect static assets, then exec gunicorn so PID 1 receives signals
python manage.py migrate --no-input
python manage.py collectstatic --noinput

exec gunicorn --config gunicorn.conf.py gettingstarted.wsgi
