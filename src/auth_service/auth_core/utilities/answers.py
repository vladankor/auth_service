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

    #def add_data(self, dict_path: DictPath, value: Union[str, Dict], create_if_not_exists=True):
    #    current_node = self.__result
    #    sub_node_names = dict_path.split('.')
    #    for sub_node_name, count in zip(sub_node_names, range(len(sub_node_names))):
    #        # В общем, нужно здесь что-то придумать с концом и вообще перенести эту штуку в py_kor
    #        if count == len(sub_node_names):
    #            break
    #        sub_node = current_node.get(sub_node_name, None)
    #        if sub_node is None:
    #            if not create_if_not_exists:
    #                raise ValueError(f'Node {sub_node} not found')
    #            current_node[sub_node_name] = {}
    #    if current_node is None:
    #        current_node = sub_node

    @property
    def result(self):
        return self.__result


class ErrorCode(Enum):
    ERROR = 0
    USER_ALREADY_EXISTS = 1
    USER_NOT_FOUND = 2


class Error(Result):
    def __init__(self,
                 description: str = '',
                 user_description: str = '',
                 error_code: int = ErrorCode.ERROR.value(),
                 data: Dict = None):
        super(Error, self).__init__(description, user_description, data)
        self.__result.update({'error_code': str(error_code)})
