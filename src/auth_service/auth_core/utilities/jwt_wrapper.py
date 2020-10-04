from typing import Dict, Optional
import datetime
from django.utils import timezone

import jwt

from auth_service.settings.security import (
    JWT_SECRET_KEY,
    JWT_LIFE_TIME_SECONDS
)


"""
JWT data format:
    - email: String
    - phone_number: String
    - rights: Integer
    - expires_at: TimeStamp
"""


class JWTWrapper:
    def __init__(self,
                 encoded_jwt: Optional[str] = None,
                 data_to_generate_jwt: Dict = None):
        if not encoded_jwt:
            if data_to_generate_jwt:
                self.__data = jwt.encode(data_to_generate_jwt, JWT_SECRET_KEY).decode('utf-8')
                self.__access_token = encoded_jwt
                self.__expires_at = datetime.datetime.fromtimestamp(self.__data.get())
            else:
                raise ValueError(f'Expected encoded_jwt or data_to_generate_jwt, but received None')
        else:
            try:
                self.__data = data_to_generate_jwt
                self.__access_token = jwt.decode(encoded_jwt.encode('utf-8'), JWT_SECRET_KEY)
                self.__expires_at = timezone.now() + datetime.timedelta(seconds=JWT_LIFE_TIME_SECONDS)
            except jwt.DecodeError as e:
                raise ValueError(f'Unable encode JWT {e}')

    def is_valid(self) -> bool:
        return timezone.now() < self.__expires_at

    @property
    def access_token(self):
        return self.__access_token


def create_jwt(data_to_generate_jwt: Dict) -> JWTWrapper:
    """
    Return JWTWrapper
    """
    return JWTWrapper(data_to_generate_jwt=data_to_generate_jwt)


def decode_jwt(encoded_jwt: str) -> JWTWrapper:
    """
    Return JWTWrapper
    Raise ValueError exception if can't encode jwt
    """
    return JWTWrapper(encoded_jwt=encoded_jwt)



