"""Django settings for the store application (store)"""

from Cubic3D.settings import *

ROOT_URLCONF = 'store.urls'

if platform == 'win32':
    SITE_ID = 3
else:
    SITE_ID = 5

WSGI_APPLICATION = 'store.wsgi.application'

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
    'store',
    'google_analytics',
    'verify_email',
]
