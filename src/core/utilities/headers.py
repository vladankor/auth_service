from enum import Enum


class XHTTPRequestHeaders(Enum):
    X_AUTHENTICATION_TOKEN = 'X-Authentication-Token'
    X_REFRESH_TOKEN = 'X-Refresh-Token'
    X_DEVICE_ID = 'X-Device-ID'


class HTTPRequestHeaders(Enum):
    AUTHORIZATION = 'HTTP_AUTHORIZATION'


class XHTTPResponseHeaders(Enum):
    X_AUTHENTICATION_TOKEN = 'X-Authentication-Token'
    X_REFRESH_TOKEN = 'X-Refresh-Token'
    X_DEVICE_ID = 'X-Device-ID'
