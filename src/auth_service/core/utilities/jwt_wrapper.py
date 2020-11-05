from typing import Dict, Optional
from django.utils import timezone

import jwt

from auth_service.settings.security import (
    JWT_SECRET_KEY,
    JWT_LIFE_TIME_SECONDS
)
from auth_service.settings.main import SERVICE_NAME


"""
JWT data format
"""


class JWTWrapper:
    def __init__(self,
                 encoded_jwt: Optional[str] = None,
                 data_to_generate_jwt: Dict = None):
        if not encoded_jwt:
            if data_to_generate_jwt:
                self.__data = jwt.encode(payload=data_to_generate_jwt, key=JWT_SECRET_KEY).decode('utf-8')
                self.__value = encoded_jwt
                self.__expires_at = timezone.datetime.fromtimestamp(data_to_generate_jwt.get('exp'))
            else:
                raise ValueError(f'Expected encoded_jwt or data_to_generate_jwt, but received None')
        else:
            try:
                self.__data = data_to_generate_jwt
                self.__value = jwt.decode(encoded_jwt.encode('utf-8'), key=JWT_SECRET_KEY, issuer=SERVICE_NAME)
                self.__expires_at = timezone.now() + timezone.timedelta(seconds=JWT_LIFE_TIME_SECONDS)
            except jwt.DecodeError as e:
                raise ValueError(f'Unable encode JWT {e}')

    def is_valid(self) -> bool:
        return timezone.now() < self.__expires_at

    @property
    def expires_at(self):
        return self.__expires_at

    @property
    def value(self):
        return self.__value


def create_jwt(data_to_generate_jwt: Dict) -> JWTWrapper:
    """
    Return JWTWrapper
    Raise ValueError exception if data_to_generate_jwt is NOne
    """
    return JWTWrapper(data_to_generate_jwt=data_to_generate_jwt)


def decode_jwt(encoded_jwt: str) -> JWTWrapper:
    """
    Return JWTWrapper
    Raise ValueError exception if can't encode jwt
    """
    return JWTWrapper(encoded_jwt=encoded_jwt)



