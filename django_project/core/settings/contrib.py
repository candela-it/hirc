from .base import *

# Extra installed apps
INSTALLED_APPS += (
    # 'raven.contrib.django',  # enable Raven plugin
    'south',
    'pipeline',
    'reversion',
    'django.contrib.humanize',
    'django.contrib.comments',
    'django_comments_xtd',
    'social.apps.django_app.default'
)

# use underscore template function
PIPELINE_TEMPLATE_FUNC = '_.template'

# enable cached storage - requires uglify.js (node.js)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_DISABLE_WRAPPER = True


#Emails are disabled.
COMMENTS_APP = 'django_comments_xtd'
COMMENTS_XTD_CONFIRM_EMAIL = False
COMMENTS_XTD_THREADED_EMAILS = False
#Setting 0 means threaded comments are disabled.
COMMENTS_XTD_MAX_THREAD_LEVEL = 5
COMMENTS_XTD_FORM_CLASS = 'web.forms.CustomXtdCommentForm'

# python social auth required settings
AUTHENTICATION_BACKENDS = (
    'social.backends.openstreetmap.OpenStreetMapOAuth',
)

SOCIAL_AUTH_OPENSTREETMAP_KEY = 'LBqrPd0Y3YE9RKkn4RUVc5sDDcoVjbYpart7qdsr'
SOCIAL_AUTH_OPENSTREETMAP_SECRET = 'sFlquDZLeU1aqsYCIbMAetLVrELunyIvV7mPCR2Q'
