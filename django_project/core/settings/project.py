from .contrib import *

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        # Or path to database file if using sqlite3.
        'NAME': 'hirc_dev',
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'HOST': '',
        # Set to empty string for default.
        'PORT': '',
    }
}

# Project apps
INSTALLED_APPS += (
    'imagery_requests',
    'django.contrib.comments',
    'django_comments_xtd',
    'questions',
    'web',
    'social.apps.django_app.default'
)

# custom user for the project
AUTH_USER_MODEL = 'imagery_requests.CustomUser'

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

COMMENTS_APP = "django_comments_xtd"
COMMENTS_XTD_CONFIRM_EMAIL = False
#Setting 0 means threaded comments are disabled.
COMMENTS_XTD_MAX_THREAD_LEVEL = 4

# python social auth required settings
AUTHENTICATION_BACKENDS = (
    'social.backends.openstreetmap.OpenStreetMapOAuth',
    'django.contrib.auth.backends.ModelBackend'
)

SOCIAL_AUTH_OPENSTREETMAP_KEY = 'LBqrPd0Y3YE9RKkn4RUVc5sDDcoVjbYpart7qdsr'
SOCIAL_AUTH_OPENSTREETMAP_SECRET = 'sFlquDZLeU1aqsYCIbMAetLVrELunyIvV7mPCR2Q'


PIPELINE_JS = {
    'contrib': {
        'source_filenames': (
            'js/jquery-1.11.1.min.js',
            'js/csrf-ajax.js',
            'js/underscore-min.js',
            'js/semantic.min.js',
            'js/leaflet.js'
        ),
        'output_filename': 'js/contrib.js',
    }
}

PIPELINE_CSS = {
    'contrib': {
        'source_filenames': (
            'css/semantic.min.css',
            'css/leaflet.css',
            'css/custom.css',
            # 'css/bootstrap.min.css',
            # 'css/bootstrap-responsive.min.css',
        ),
        'output_filename': 'css/contrib.css',
        'extra_context': {
            'media': 'screen, projection',
        },
    }
}
