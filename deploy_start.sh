#!/usr/bin/env bash
set -e

# Run migrations, collect static assets, then exec gunicorn so PID 1 receives signals

# 1. Run Migrations (using 'python -m' for robustness)
echo "Applying database migrations..."
python -m manage migrate --no-input

# 2. Collect Static Files
echo "Collecting static files..."
python -m manage collectstatic --no-input

# 3. Start the Web Server
echo "Starting Gunicorn server..."
exec gunicorn --config gunicorn.conf.py gettingstarted.wsgi