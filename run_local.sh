#!/usr/bin/env bash
cp /src/supervisor.ini /etc/supervisor.d/supervisor.ini
supervisord -c /etc/supervisord.conf -j /etc/supervisor.pid
python ./yuehu/manage.py runserver 0.0.0.0:8000
