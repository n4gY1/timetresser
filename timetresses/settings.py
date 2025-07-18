import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)wo^pxcqp)z&5!u@h*o0mx#(7e&(^u92!uqm1!ns&w(i%&@x&i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ALLOWED_HOSTS = ['https://timetresser-917e75b313f7.herokuapp.com','timetresser-917e75b313f7.herokuapp.com','localhost']
#ALLOWED_HOSTS = ["idopontok.run.place", "localhost", "127.0.0.1"]
ALLOWED_HOSTS = ["mytimes.hu", "localhost", "127.0.0.1"]
#ALLOWED_HOSTS = ["*"]
#CSRF_TRUSTED_ORIGINS = ["https://idopontok.run.place"]
AUTH_USER_MODEL = 'account.User'
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1","https://mytimes.hu"]
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'mytimesdev@gmail.com'
EMAIL_HOST_PASSWORD = "izuznwjcalojwcbi"
EMAIL_USE_TLS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'booking',
    'service_provider',
    'rating',


]

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'timetresses.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'service_provider.context_processors.get_context_processors',
            ],
        },
    },
]

WSGI_APPLICATION = 'timetresses.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
USE_TZ = True
TIME_ZONE = 'Europe/Budapest'

USE_I18N = True

STATIC_URL = 'static/'
#STATICFILES_DIRS = [BASE_DIR / "static",]

#STATIC_ROOT = "/home/nagy-webpages/timetresser/publishstaticfiles" #hogy ennek van e köze hozzá????

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# if os.getcwd() == '/app':
#    DEBUG = False
#    SECURE_SSL_REDIRECT = True
