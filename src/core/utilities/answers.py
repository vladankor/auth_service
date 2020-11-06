from typing import DefaultDict, Dict, Union, NewType
from enum import Enum
from collections import defaultdict


from py_kor.pk_mixins import ChoiceEnum


DictPath = NewType('DictPath', str)

"""
Answers format:

Result:
    description: str
    user_description: str
    data: {...}
    
Error:
    description: str
    user_description: str
    error_code: int
    data: {...}
"""


class Result:
    def __init__(self,
                 description: str = '',
                 user_description: str = '',
                 data: Dict = None):
        self.__result = {
            'description': description,
            'user_description': user_description,
            'data': data if data else {}
        }

    @property
    def json(self) -> Dict:
        return self.__result


class ErrorCode(Enum):
    # Standard - 0xx
    ERROR = 0
    INVALID_PARAMETERS = 1
    # User - 1xx
    USER_ALREADY_EXISTS = 100
    USER_NOT_FOUND = 101
    USER_NOT_CREATED = 102
    # Session - 2xx
    SESSION_NOT_FOUND = 201


class Error(Result):
    def __init__(self,
                 description: str = '',
                 user_description: str = '',
                 error_code: int = ErrorCode.ERROR.value,
                 data: Dict = None):
        super(Error, self).__init__(description, user_description, data)
        self.__result.update({'error_code': str(error_code)})
