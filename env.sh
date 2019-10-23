# Twilio Credentials
export TWILIO_ACCOUNT_SID='ACab88975749256b2c164ca5808e67f46c'
export TWILIO_AUTH_TOKEN='9861f67b382cc35fa8e7cd1712f2a049'
export FROM_NUMBER='+12563635191'

# Auth0 credentials
export AUTH0_CLIENT_ID='ZJI7LxM6T0VJ0PpXdFlaCSrkDK7xy7BD'
export AUTH0_DOMAIN='dev-9sgdpaff.auth0.com'
export AUTH0_CLIENT_SECRET='cVbUhz1PosdBeAyOhA8EZ18Y0OxO1eVplucb7xpr9-89jXLlvk9p1MmAfL9udKGi'

# Rapid commands
./manage.py makemigrations
./manage.py migrate
./manage.py runserver 0.0.0.0:8000
