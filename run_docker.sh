#!/usr/bin/env bash
cp /src/supervisor.ini /etc/supervisor.d/supervisor.ini
supervisord -c /etc/supervisord.conf -j /etc/supervisor.pid
python ./yuehu/manage.py migrate && uwsgi --chdir=/src/yuehu --pidfile=/tmp/app.pid --http=0.0.0.0:8000 --module=yuehu.wsgi:application --processes=3 --threads=50 --max-requests=5000 --harakiri=30 --vacuum --master
