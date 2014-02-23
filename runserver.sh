#!/bin/bash
NEW_RELIC_CONFIG_FILE=conf/newrelic.ini
NEW_RELIC_ADMIN="venv/bin/newrelic-admin"
GUNICORN="venv/bin/gunicorn --config conf/gun.py"
DJANGO_APP=foodspot.wsgi:application

export NEW_RELIC_CONFIG_FILE

exec $NEW_RELIC_ADMIN run-program $GUNICORN $DJANGO_APP
