#!/bin/bash

python manage.py makemigrations
python manage.py migrate
echo "DB migrated successfully"

python manage.py crontab add
