#!/bin/bash
NEW_RELIC_CONFIG_FILE=conf/newrelic.ini
GUNICORN="venv/bin/gunicorn --config conf/gun.py"
DJANGO_APP=foodspot.wsgi:application

export NEW_RELIC_CONFIG_FILE

exec newrelic-admin run-program $GUNICORN $DJANGO_APP
