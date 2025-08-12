#!/usr/bin/env bash
# build.sh
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files (for Django Admin)
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate