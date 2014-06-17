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
    'questions',
    'web'
)

# reversion depends on CustomUSer, so it needs to be placed after
# 'imagery_requests' migration which creates CustomUser
INSTALLED_APPS += (
    'reversion',
)


# define settings which are readable from templates
TEMPLATE_READABLE_VALUES = ("PROJECT_TITLE", )

# project TITLE
PROJECT_TITLE = 'TEST H.O.T. Imagery Request Coordination service TEST'

# custom user for the project
AUTH_USER_MODEL = 'imagery_requests.CustomUser'

# redirect logged in user to the home page
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/openstreetmap'

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False


PIPELINE_JS = {
    'contrib': {
        'source_filenames': (
            'js/jquery-1.11.1.min.js',
            'js/csrf-ajax.js',
            'js/underscore-min.js',
            'js/semantic.min.js',
            'js/leaflet.js',
            'js/leaflet.draw.js',
            'js/leaflet-omnivore.min.js',
            'js/tiles/Bing.js',
            'js/Leaflet.MakiMarkers.js',
            'js/jquery-ui-1.10.4.custom.min.js',
            'js/map.js'
        ),
        'output_filename': 'js/contrib.js',
    }
}

PIPELINE_CSS = {
    'contrib': {
        'source_filenames': (
            'css/semantic.min.css',
            'css/leaflet.css',
            'css/leaflet.draw.css',
            'css/ui-lightness/jquery-ui-1.10.4.custom.min.css',
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
