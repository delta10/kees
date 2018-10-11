# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kees',
    }
}

EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'
EMAIL_HOST_USER = None
EMAIL_HOST_PASSWORD = None
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_FROM = 'noreply@test.com'
