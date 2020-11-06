import os


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '50ka1uk5@ouw1rt4d=rz(z=^-9bs&13wotb962@zx^0tflyisn')

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', '50ka1uk5@ouw1rt4d=rz(z=^-9bs&13wotb962@zx^0tflyisn')
JWT_LIFE_TIME_SECONDS = int(os.environ.get('JWT_LIFE_TIME_SECONDS', 60 * 60 * 24 * 8))

TOKEN_LIFE_TIME_SECONDS = int(os.environ.get('TOKEN_LIFE_TIME_SECONDS', 60 * 60))
REFRESH_TOKEN_LIFE_TIME_SECONDS = int(os.environ.get('REFRESH_TOKEN_LIFE_TIME_SECONDS', 60 * 60))

# CORS integration
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'enctype',
    'x-device_id',
    'x-device_type',
    'x-auth-token'
]

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:8080',
    '127.0.0.1:8888',
    '127.0.0.1',
)

SECURE_SSL_REDIRECT = True
