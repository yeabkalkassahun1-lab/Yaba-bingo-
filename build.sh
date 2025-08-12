#!/usr/bin/env bash
# build.sh - Simplified for use with rootDir in render.yaml
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate