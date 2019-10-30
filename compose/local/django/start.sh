#!/bin/sh

export TWILIO_ACCOUNT_SID='ACab88975749256b2c164ca5808e67f46c'
export TWILIO_AUTH_TOKEN='9861f67b382cc35fa8e7cd1712f2a049'
export FROM_NUMBER='+12563635191'

export NEXMO_ACCOUNT_KEY='3dd87d1b'
export NEXMO_ACCOUNT_SECRET='zqeWclg6BnedHNd1'

python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000