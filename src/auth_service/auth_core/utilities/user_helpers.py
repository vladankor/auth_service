from typing import Optional
from hashlib import sha256

from auth_core.models import User


def is_user_exists(email: str, phone_number: str) -> bool:
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


def error_user_already_exists_msg(**kwargs) -> str:
    fields_errors = []
    for field_name, field_value in kwargs.items():
        if field_value is not None:
            fields_errors.append(f'{field_name}: {field_value}')

    return f'User with {" ".join(fields_errors)} already exists'


def error_user_not_found_msg(**kwargs) -> str:
    fields_errors = []
    for field_name, field_value in kwargs.items():
        if field_value is not None:
            fields_errors.append(f'{field_name}: {field_value}')

    return f'User with {" ".join(fields_errors)} not found'


def create_user(email: str, phone_number: str, password: str) -> Optional[User]:
    return User.objects.create(email=email,
                               phone_number=phone_number,
                               password=sha256(password.encode()).hexdigest())
