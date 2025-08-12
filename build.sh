#!/usr/bin/env bash
# A simple build script for Render

set -o errexit  # Exit on error

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate