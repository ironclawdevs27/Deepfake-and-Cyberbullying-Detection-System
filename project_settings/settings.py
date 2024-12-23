import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.abspath(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = '@)0qp0!&-vht7k0wyuihr+nk-b8zrvb5j^1d@vl84cd1%)f=dz'

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ml_app.apps.MlAppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Ensure CSRF middleware is enabled
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project_settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Ensure templates are accessible
        'DIRS': [os.path.join(PROJECT_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                # Required for CSRF token in templates
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'project_settings.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(PROJECT_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False
USE_L10N = False
USE_TZ = False

STATIC_ROOT = "/home/app/staticfiles/"
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'uploaded_images'),
    os.path.join(PROJECT_DIR, 'static'),
    os.path.join(PROJECT_DIR, 'models'),
]

CONTENT_TYPES = ['video']
MAX_UPLOAD_SIZE = "104857600"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'uploaded_videos')

# CSRF Settings
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000',
                        'http://localhost:8000']  # Add your domain(s) here
CSRF_COOKIE_SECURE = not DEBUG  # Ensure CSRF cookies are secure in production
# Ensure session cookies are secure in production
SESSION_COOKIE_SECURE = not DEBUG

if DEBUG == False:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'log.django',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'file'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            },
        },
    }
