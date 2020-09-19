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


def create_user(email: str, phone_number: str, password: str) -> Optional[User]:
    return User.objects.create(email=email,
                               phone_number=phone_number,
                               password=sha256(password.encode()).hexdigest())
