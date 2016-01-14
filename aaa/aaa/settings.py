# coding=<utf-8>
"""
Django settings for aaa project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os,platform
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

FILE_SAVE_PATH = "/home/wenshang/upload/"
#from mini.models import Syssetting

if 'Windows' in platform.system():
    FILE_SAVE_PATH = "d:/upload/"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2=t!h7pnfy=$!xmsbm0uv9*k^y#1pyqxd37__z*#h+bu!(2-l2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

#DEBUG_TOOLBAR_PATCH_SETTINGS = False

INTERNAL_IPS = ('127.0.0.1',)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mini',
   # 'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
   # 'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'aaa.urls'

WSGI_APPLICATION = 'aaa.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mininas',
	'USER':'root',
	'PASSWORD':'wenshang',
	'HOST':'',
	'PORT':'3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#DEBUG_TOOLBAR_PATCH_SETTINGS = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(__file__),'static')

STATICFILES_DIRS = (
	('css',os.path.join(STATIC_ROOT,'css').replace('\\','/')),
	('js',os.path.join(STATIC_ROOT,'js').replace('\\','/')),
	('images',os.path.join(STATIC_ROOT,'images').replace('\\','/')),
	('im1',os.path.join(STATIC_ROOT,'images/Default/Home/').replace('\\','/')),
)

STATICFILES_FINDERS = (
	"django.contrib.staticfiles.finders.FileSystemFinder",
	"django.contrib.staticfiles.finders.AppDirectoriesFinder"
)


#DEBUG_TOOLBAR_CONFIG = {
    # Django's test client sets wsgi.multiprocess to True inappropriately
#    'RENDER_PANELS': False,
#}
