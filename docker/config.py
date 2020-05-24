import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG') == 'True')

ALLOWED_HOSTS = [os.getenv('ALLOWED_HOST')]

SESSION_COOKIE_SECURE = (os.getenv('SESSION_COOKIE_SECURE') == 'True')
CSRF_COOKIE_SECURE = (os.getenv('CSRF_COOKIE_SECURE') == 'True')

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DB_HOST'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'NAME': os.getenv('DB_NAME')
    }
}

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_USE_TLS = (os.getenv('EMAIL_USE_TLS') == 'True')
EMAIL_USE_SSL = (os.getenv('EMAIL_USE_SSL') == 'True')
EMAIL_FROM = os.getenv('EMAIL_FROM')
