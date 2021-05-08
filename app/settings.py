"""Django settings for the main application (app)"""

from Cubic3D.settings import *

ROOT_URLCONF = 'app.urls'

WSGI_APPLICATION = 'app.wsgi.application'

if platform == 'win32':
    SITE_ID = 2
else:
    SITE_ID = 3

# Application definition
INSTALLED_APPS = [
    
    # Add your apps here to enable them
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'app',
    'google_analytics',
    'verify_email',
]
