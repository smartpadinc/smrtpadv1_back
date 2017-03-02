"""
Django settings for smrtpadv1_back project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import envvars


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

envvars.load(BASE_DIR + '/.env')

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('ENABLE_DEBUG')

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'oauth2_provider',
    'rest_framework_docs',
    'rest_framework',
    'rest_framework.authtoken',
    'user',
    'properties',
    'utils'
]

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope'},
    #'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore'
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    #'DEFAULT_PERMISSION_CLASSES': (
    #    'rest_framework.permissions.IsAuthenticated',
    #)
}

REST_FRAMEWORK_DOCS = {
    'HIDE_DOCS': False,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware'
]

LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'dev-api.smartpad.local:8096',
)

ROOT_URLCONF = 'smrtpadv1_back.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates/")
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'smrtpadv1_back.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('SMPD_DB_NAME'),
        'USER': os.environ.get('SMPD_DB_USER'),
        'PASSWORD': os.environ.get('SMPD_DB_PASS'),
        'HOST': os.environ.get('SMPD_DB_HOST'),
        'PORT': os.environ.get('SMPD_DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
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

# https://ian.pizza/b/2013/04/16/getting-started-with-django-logging-in-5-minutes/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'app_log': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/smartpad/api.log',
            'maxBytes': 1024*1024*15, # 15MB
            'backupCount': 10,
            'formatter': 'verbose'
        },
        'system_error_log': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/smartpad/error.log',
            'maxBytes': 1024*1024*15, # 15MB
            'backupCount': 10,
            'formatter': 'verbose'
        },
        'db_log': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/smartpad/db.log',
            'maxBytes': 1024*1024*15, # 15MB
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['system_error_log'],
            'level': 'ERROR',
        },
        'django.server': {
            'handlers': ['system_error_log'],
            'level': 'ERROR',
        },
        'django.template': {
            'handlers': ['system_error_log'],
            'level': 'ERROR',
        },
        'django.db.backends': {
            'handlers': ['db_log'],
            'level': 'ERROR',
        },
        'user': {
            'handlers': ['app_log',],
            'level': 'DEBUG',
        },
        'properties': {
            'handlers': ['app_log',],
            'level': 'DEBUG',
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "assets/")
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "assets/"),
# ]
STATIC_URL = '/assets/'


## OPTIONS ##

OPT_STATUS = (
    ('A', 'Active'),
    ('I', 'Inactive'),
    ('D', 'Deleted')
)

OPT_COUNTRY = (
    ('ph', 'Philippines'),
    ('sg', 'Singapore'),
)

OPT_VALID_IDS = {
    ('0', 'none'),
    ('1', 'SSS'),
    ('2', 'Passport'),
    ('3', "Driver's License"),
}

OPT_USER_TYPE = (
    ('1', 'TENANT'),
    ('2', 'OWNER'),
    ('3', 'AGENT'),
)

OPT_PROPERTY_TYPE = (
    ('1', 'Studio'),
    ('2', '1-Bedroom'),
    ('3', '2-Bedroom'),
    ('4', '3-Bedroom'),
    ('6', 'Townhouse'),
)

OPT_PAYMENT_TYPE = (
    ('1', 'Cash'),
    ('2', 'Post-dated Cheque'),
    ('3', 'Flexible'),
)

OPT_PAYMENT_INTERVAL = (
    ('1', 'Monthly'),
    ('2', 'Quarterly'),
    ('3', 'Semi-Annually'),
    ('4', 'Annually'),
)

OPT_RENT_STATUS = (
    ('1', 'Open'),
    ('2', 'Rented'),
    ('3', 'Available Soon'),
)
