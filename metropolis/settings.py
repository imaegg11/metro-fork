"""
Django settings for metropolis project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'Change me'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'core',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'captcha',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.TimezoneMiddleware',
]

ROOT_URLCONF = 'metropolis.urls'

TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'django.template.context_processors.request',
                    ],
                },
            },
        ]

WSGI_APPLICATION = 'metropolis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# Auth settings

AUTH_USER_MODEL = 'core.User'

# Timetable settings

TIMETABLE_FORMATS = {
    'pre-2020': {
        'schedule': [
            {'info': '08:45 - 10:05', 'position': [{1}, {1}]},
            {'info': '10:15 - 11:30', 'position': [{2}, {2}]},
            {'info': '12:30 - 13:45', 'position': [{3}, {4}]},
            {'info': '13:50 - 15:05', 'position': [{4}, {3}]},
        ],
        'courses': 4,
        'positions': {1, 2, 3, 4},
        'cycle': {
            'length': 2,
            'duration': 'day',
        },
        'question': {
            'prompt': 'Your Nth course on day 1 is this course. N = ?',
            'choices': [
                (1, 1),
                (2, 2),
                (3, 3),
                (4, 4),
            ]
        }
    },
    'covid': {
        'schedule': [
            {'info': '08:45 - 12:30 (In person)', 'position': [{1}, {2}, {3}, {4}]},
            {'info': '08:45 - 12:30 (At home)', 'position': [{2}, {1}, {4}, {3}]},
            {'info': '14:00 - 15:15 (At home)', 'position': [{3, 4}, {3, 4}, {1, 2}, {1, 2}]},
        ],
        'courses': 2,
        'positions': {1, 2, 3, 4},
        'cycle': {
            'length': 4,
            'duration': 'day',
        },
        'question': {
            'prompt': 'On which day are you in person for this course?',
            'choices': [
                (1, 1),
                (2, 2),
                (3, 3),
                (4, 4),
            ]
        }
    },
    'week': {
        'schedule': [
            {'info': '09:00 - 11:30', 'position': [{1, 5, 7}, {3, 6, 7}]},
            {'info': '12:15 - 14:45', 'position': [{2, 5, 7}, {4, 6, 7}]},
        ],
        'courses': 4,
        'positions': {1, 2, 3, 4, 5, 6, 7},
        'cycle': {
            'length': 2,
            'duration': 'week',
        },
        'question': {
            'prompt': 'When do you have class for this course?',
            'choices': [
                (1, 'Week 1 Morning'),
                (2, 'Week 1 Afternoon'),
                (3, 'Week 2 Morning'),
                (4, 'Week 2 Afternoon'),
                (5, 'This course is a 2-credit Co-op in Week 1.'),
                (6, 'This course is a 2-credit Co-op in Week 2.'),
                (7, 'This course is a 4-credit Co-op.'),
            ]
        }
    },
}

# Authentication settings

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_FORMS = {
    'login': 'allauth.account.forms.LoginForm',
    'signup': 'core.forms.MetropolisSignupForm',
    'add_email': 'allauth.account.forms.AddEmailForm',
    'change_password': 'allauth.account.forms.ChangePasswordForm',
    'set_password': 'allauth.account.forms.SetPasswordForm',
    'reset_password': 'allauth.account.forms.ResetPasswordForm',
    'reset_password_from_key': 'allauth.account.forms.ResetPasswordKeyForm',
    'disconnect': 'allauth.socialaccount.forms.DisconnectForm',
}
LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/accounts/profile'
LOGOUT_REDIRECT_URL = "/"

# ReCaptcha settings

RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
RECAPTCHA_REQUIRED_SCORE = 0.85

# NavBar settings

NAVBAR = {
    'Announcements': '/announcements',
    'Clubs': '/clubs',
    'Calendar': '/calendar',
}

# Announcements settings

ANNOUNCEMENTS_CUSTOM_FEEDS = [
]

# Google Analytics settings

GOOGLE_ANALYTICS_TRACKING_ID = None
GOOGLE_ANALYTICS_ON_ALL_VIEWS = False

# API settings

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# CORS settings

CORS_URLS_REGEX = r'^.*/data/?$'

CORS_ALLOW_METHODS = [
    'GET',
    'HEAD',
    'OPTIONS',
]

CORS_ALLOW_ALL_ORIGINS = True

# Misc settings

SITE_ID = 1

TOS_URL = '/terms'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

try:
    from metropolis.config import *
except ImportError:
    print("Please create a config file to override values in settings.py")
