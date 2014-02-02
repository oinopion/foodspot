#!/bin/bash
exec venv/bin/gunicorn --config conf/gun.py foodspot.wsgi:application
