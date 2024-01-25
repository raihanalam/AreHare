
from pathlib import Path
import os
from channels.routing import ProtocolTypeRouter
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = os.path.join(BASE_DIR,'static')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-86!##us@n-5it1_qwf1n*3iyz0%1asj4j*ds01gb7+mrnaf32a'
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

# ALLOWED_HOSTS = ['arehare.com', 'www.arehare.com']
ALLOWED_HOSTS = list(config('ALLOWED_HOSTS').split(','))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'Account_App',
    'Main_App',
    'Dashboard_App',
    'Message_App',
    'Work_App',
    'Wallet_App',
    'Notification_App',
    'Search_App',
    'Admin_App',

    'notifications',
    'channels',
    'django_cleanup.apps.CleanupConfig',
    'ckeditor',
    'bootstrap4',
    'crispy_bootstrap4',
    'crispy_forms',
    'bootstrap_datepicker_plus',
    'captcha',

    #Social Auth
    #'django.contrib.sites',
    #'allauth',
    #'allauth.account',
    #'allauth.socialaccount',
    #'allauth.socialaccount.providers.google',
    
]


#Social Auth
#SITE_ID = 1
#SOCIALACCOUNT_LOGIN_ON_GET=True

#We can use bootstrap, bootstrap3, bootstrap4, uni-form
CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_TEMPLATE_FORMS = 'bootstrap4'
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap4'

AUTH_USER_MODEL = 'Account_App.User'


CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ['http://arehare.com', 'https://arehare.com']


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'FSMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'FSMS.wsgi.application'
ASGI_APPLICATION = 'FSMS.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": ['redis://localhost:6379'],
        },
    },
}
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels.layers.InMemoryChannelLayer',
#     },
# }
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'fsms',
#         'USER': 'raihan',
#         'PASSWORD': '161189',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USERNAME"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators


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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_L10N = True

USE_TZ = True



DATE_INPUT_FORMATS = [
    '%m/%d/%Y',  # '10/25/2006'
    '%Y-%m-%d',  # '2006-10-25'
    '%m/%d/%y',  # '10/25/06'
    '%b %d %Y',  # 'Oct 25 2006'
    '%b %d, %Y',  # 'Oct 25, 2006'
    '%d %b %Y',  # '25 Oct 2006'
    '%d %b, %Y',  # '25 Oct, 2006'
    '%B %d %Y',  # 'October 25 2006'
    '%B %d, %Y',  # 'October 25, 2006'
    '%d %B %Y',  # '25 October 2006'
    '%d %B, %Y',  # '25 October, 2006'
]

DATE_INPUT_FORMATS = ("%d/%m/%Y",)



# Emailing settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = 'raihanhridoybd@gmail.com'
EMAIL_HOST_USER = 'raihanhridoybd@gmail.com'
EMAIL_HOST_PASSWORD = 'pduthzzzcdqcbuof'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


PASSWORD_RESET_TIMEOUT = 14400





#Recaptcha Settings

# AUTHENTICATION_BACKENDS = ['users.backends.EmailBackend']


#social settings

AUTHENTICATION_BACKENDS = [
    # 'users.backends.EmailBackend',
   
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    #'allauth.account.auth_backends.AuthenticationBackend',
   
]
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'SCOPE': [
#             'profile',
#             'email',
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'online',
#         }
#     }
# }

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

RECAPTCHA_PUBLIC_KEY = '6LcUtMIiAAAAAKeeAcEwomxD9YyjgbBYKbXoHlfH'
RECAPTCHA_PRIVATE_KEY = '6LcUtMIiAAAAAI7D3-2q9cWaThhOS37lqPlzNQwA'
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'


# Add the following line to set STATIC_ROOT
if config('DEBUG'):
    STATICFILES_DIRS = [
        STATIC_DIR,
    ]
    STATIC_ROOT = os.path.join(BASE_DIR,'static_root/')
else:
    STATIC_ROOT = '/home/ubuntu/AreHare/AreHare/static_root/'


MEDIA_URL = 'media/'

if config('DEBUG'):
    MEDIA_ROOT = os.path.join(BASE_DIR,'media/')
else:
    MEDIA_ROOT = '/home/ubuntu/AreHare/AreHare/media/'

#Unauthorized Access
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/account/signin/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CKEDITOR_CONFIGS = {
    'default': {
        'height': 'full', 
        'width': 'full', 
    },
}

