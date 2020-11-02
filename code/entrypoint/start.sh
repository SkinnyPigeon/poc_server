#!/bin/bash

python3 /code/00-run-me.py

gunicorn -b 0.0.0.0:2021 --workers=3 --chdir /code/api pymail:app
