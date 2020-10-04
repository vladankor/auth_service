from typing import Optional
from hashlib import sha256

from auth_core.models import User
from auth_core.utilities.answers import Result, Error, ErrorCode


def is_user_exists(email: Optional[str], phone_number: Optional[str]) -> bool:
    if email and phone_number:
        return User.objects \
            .filter(email=email, phone_number=phone_number) \
            .exists()
    elif email:
        return User.objects \
            .filter(email=email) \
            .exists()
    elif phone_number:
        return User.objects \
            .filter(phone_number=phone_number) \
            .exists()
    return False


def validate_access_token(access_token: Optional[str]) -> bool:
    if not access_token:
        return False
    return True


def error_user_already_exists_msg(**kwargs) -> Error:
    fields_errors = []
    for field_name, field_value in kwargs.items():
        if field_value is not None:
            fields_errors.append(f'{field_name}: {field_value}')

    return Error(description=f'User with {" ".join(fields_errors)} already exists',
                 user_description=f'User with {" ".join(fields_errors)} already exists',  # TODO: Add translation
                 error_code=ErrorCode.USER_ALREADY_EXISTS.value())


def error_user_not_found_msg(**kwargs) -> Error:
    fields_errors = {}
    for field_name, field_value in kwargs.items():
        if field_value is not None:
            fields_errors.update({field_name: field_value})

    return Error(description=f'User not found',
                 user_description=f'User not found',  # TODO: Add translation
                 error_code=ErrorCode.USER_NOT_FOUND.value(),
                 data=fields_errors)


def create_user(email: str, phone_number: str, password: str) -> Optional[User]:
    return User.objects.create(email=email,
                               phone_number=phone_number,
                               password=sha256(password.encode()).hexdigest())


def result_user_created_msg(**kwargs) -> Result:
    fields_results = {}
    for field_name, field_value in kwargs.items():
        if field_value is not None:
            fields_results.update({field_name: field_value})
    return Result(description=f'User has been created',
                  user_description=f'User has been created',  # TODO: Add translation
                  data=fields_results)
