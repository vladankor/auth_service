from typing import Optional
from uuid import uuid4

from django.utils import timezone

from core.models import User
from core.utilities.answers import Result, Error, ErrorCode
from core.utilities.security import hash_password


def is_user_exists(email: Optional[str], phone_number: Optional[str]) -> bool:
    if email and phone_number:
        return User.objects\
            .filter(email=email, phone_number=phone_number)\
            .exists()
    elif email:
        return User.objects\
            .filter(email=email)\
            .exists()
    elif phone_number:
        return User.objects\
            .filter(phone_number=phone_number)\
            .exists()
    return False


def get_user(email: Optional[str], phone_number: Optional[str]) -> Optional[User]:
    if email and phone_number:
        return User.objects\
            .filter(email=email, phone_number=phone_number)\
            .first()
    elif email:
        return User.objects\
            .filter(email=email)\
            .first()
    elif phone_number:
        return User.objects\
            .filter(phone_number=phone_number)\
            .first()
    return None


def validate_authentication_token(authentication_token: Optional[str]) -> bool:
    if not authentication_token:
        return False
    return True


def create_user(email: str, phone_number: str, password: str) -> Optional[User]:
    uuid = str(uuid4()) + str(uuid4()) + str(uuid4()) + str(uuid4())
    return User.objects\
        .create(email=email,
                phone_number=phone_number,
                password=hash_password(password),
                uuid=uuid)


# Results:

def result_user_create_msg(**kwargs) -> Result:
    fields_results = {}
    for field_name, field_value in kwargs.items():
        if field_value is not None:
            fields_results.update({field_name: field_value})
    return Result(description='User has been created',
                  user_description='User has been created',  # TODO: Add translation
                  data=fields_results)


# Errors:

def error_user_invalid_parameters_msg(email: str, phone_number: str, password: str, error_code: ErrorCode) -> Error:
    if email is None and phone_number is None:
        if password is None:
            return Error(description='Email or phone number and password must not be empty',
                         user_description='Email or phone number and password must not be empty',
                         error_code=error_code.value)
        else:
            return Error(description='Email or phone number must not be empty',
                         user_description='Email or phone number must not be empty',
                         error_code=error_code.value)
    if password is None:
        return Error(description='Password must not be empty',
                     user_description='Password must not be empty',
                     error_code=error_code.value)


def error_user_create_msg(**kwargs) -> Error:
    fields_errors = {}
    for field_name, field_value in kwargs.items():
        if field_value is not None:
            fields_errors.update({field_name: field_value})

    return Error(description='User not created',
                 user_description='User not created',  # TODO: Add translation
                 error_code=ErrorCode.USER_NOT_CREATED.value,
                 data=fields_errors)


def error_user_already_exists_msg(**kwargs) -> Error:
    fields_errors = []
    for field_name, field_value in kwargs.items():
        if field_value is not None:
            fields_errors.append(f'{field_name}: {field_value}')

    return Error(description=f'User with {" ".join(fields_errors)} already exists',
                 user_description=f'User with {" ".join(fields_errors)} already exists',  # TODO: Add translation
                 error_code=ErrorCode.USER_ALREADY_EXISTS.value)


def error_user_not_found_msg(**kwargs) -> Error:
    fields_errors = {}
    for field_name, field_value in kwargs.items():
        if field_value is not None:
            fields_errors.update({field_name: field_value})

    return Error(description='User not found',
                 user_description='User not found',  # TODO: Add translation
                 error_code=ErrorCode.USER_NOT_FOUND.value,
                 data=fields_errors)


def error_invalid_password() -> Error:
    return Error(description='Invalid password',
                 user_description='Invalid password',
                 error_code=ErrorCode.INVALID_PARAMETERS.value)
