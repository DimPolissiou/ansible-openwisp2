import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '{{ openwisp2_secret_key }}'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '{{ inventory_hostname }}',
{% for host in openwisp2_allowed_hosts %}
    '{{ host }}',
{% endfor %}
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_netjsonconfig',
    'django_netjsonconfig.admin_theme',
    'django.contrib.admin',
    'sortedm2m',
    'reversion',
    'django_x509',
     'leaflet',
    'djgeojson',
    'django_cas_ng',
    'guardian',
    'rules.apps.AutodiscoverRulesConfig',
    'django_actions',
    'search_listview',
    'bootstrap_themes',
    'crispy_forms',
    'rest_framework',
    'collectd_rest',
    'devices',
{% for app in openwisp2_extra_django_apps %}
    '{{ app }}',
{% endfor %}
{% if openwisp2_sentry.get('dsn') %}
    'raven.contrib.django.raven_compat',
{% endif %}
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'openwisp2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'openwisp2.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': '{{ openwisp2_database.engine }}',
        'NAME': '{{ openwisp2_database.name }}',
{% if openwisp2_database.user %}
        'USER': '{{ openwisp2_database.user }}',
{% endif %}
{% if openwisp2_database.password %}
        'PASSWORD': '{{ openwisp2_database.password }}',
{% endif %}
{% if openwisp2_database.host %}
        'HOST': '{{ openwisp2_database.host }}',
{% endif %}
{% if openwisp2_database.port %}
        'PORT': '{{ openwisp2_database.port }}',
{% endif %}
{% if openwisp2_database.options %}
        'OPTIONS': {{ openwisp2_database.options|to_nice_json }}
{% endif %}
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = '{{ openwisp2_language_code }}'
TIME_ZONE = '{{ openwisp2_time_zone }}'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = '%s/static' % BASE_DIR
MEDIA_ROOT = '%s/media' % BASE_DIR
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

NETJSONCONFIG_SHARED_SECRET = '{{ openwisp2_shared_secret }}'
{% if openwisp2_context %}
NETJSONCONFIG_CONTEXT = {{ openwisp2_context|to_nice_json }}
{% endif %}

# django x509 settings
DJANGO_X509_DEFAULT_CERT_VALIDITY = {{ openwisp2_default_cert_validity }}
DJANGO_X509_DEFAULT_CA_VALIDITY = {{ openwisp2_default_ca_validity }}

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
        'verbose': {
            'format': '\n\n[%(levelname)s %(asctime)s] module: %(module)s, process: %(process)d, thread: %(thread)d\n%(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'main_log': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR, 'log/error.log'),
            'maxBytes': 5242880.0,
            'backupCount': 3,
            'formatter': 'verbose'
        },
{% if openwisp2_sentry.get('dsn') %}
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'filters': ['require_debug_false']
        },
{% endif %}
    },
    'root': {
        'level': 'INFO',
        'handlers': [
            'main_log',
            'console',
            'mail_admins',
{% if openwisp2_sentry.get('dsn') %}
            'sentry'
{% endif %}
        ]
    }
}

{% if openwisp2_sentry.get('dsn') %}
RAVEN_CONFIG = {{ openwisp2_sentry|to_nice_json }}
{% endif %}


LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (51.47879, 0),
    'DEFAULT_ZOOM': 5,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
    'PLUGINS': {
        'basics': {
            'js': ['http://fgnass.github.io/spin.js/dist/spin.min.js',
                   'http://makinacorpus.github.io/Leaflet.Spin/leaflet.spin.js'],
            'auto-include': True
                }
        }
}

SERIALIZATION_MODULES = {
    'geojson': 'djgeojson.serializers'
}

AUTHENTICATION_BACKENDS = (
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend', # default
    'guardian.backends.ObjectPermissionBackend',
    'django_cas_ng.backends.CASBackend',
)

GUARDIAN_RENDER_403 = True

LOGIN_URL = 'cas_ng_login'
LOGIN_REDIRECT_URL = 'devices_home'
LOGOUT_URL = 'cas_ng_login'
LOGOUT_REDIRECT_URL = 'cas_ng_login'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

CAS_SERVER_URL = '{{ openwisp2_cas_server }}'
CAS_VERSION = '3'
CAS_REDIRECT_URL = 'devices/'
AFFILIATION_FIELD = '{{ openwisp2_cas_affiliation }}'

COLLECTD_RRD_DIR = '{{ openwisp2_collectd_rrd_dir }}'
