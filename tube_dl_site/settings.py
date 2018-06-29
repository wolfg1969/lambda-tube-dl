import environ

from .base_settings import *


current = environ.Path(__file__)
project_root = current - 2

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, SECRET_KEY),
    ALLOWED_HOSTS=(list, ['*']),

    AWS_REGION=(str, 'us-east-1'),
    AWS_ACCESS_KEY_ID=(str, ''),
    AWS_SECRET_ACCESS_KEY=(str, ''),
    AWS_SESSION_TOKEN=(str, ''),
    AWS_S3_BUCKET_NAME=(str, ''),

    STAGE=(str, ''),

    DOWNLOAD_URL_TIMEOUT=(int, 3600),  # one hour
)  # set default values and casting
environ.Env.read_env(project_root('.env')) # reading .env file

DEBUG = env('DEBUG')
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = env('ALLOWED_HOSTS')

SECRET_KEY = env('SECRET_KEY')

INSTALLED_APPS += [
    'django_s3_storage',
    'tube_dl.apps.TubeDlConfig'
]

DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'

AWS_REGION = env('AWS_REGION')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = env('AWS_SESSION_TOKEN')
AWS_S3_BUCKET_NAME = env('AWS_S3_BUCKET_NAME')

VIDEO_FORMAT = 'webm'

LAMBDA_STAGE = env('STAGE')

DOWNLOAD_URL_TIMEOUT = env('DOWNLOAD_URL_TIMEOUT')
