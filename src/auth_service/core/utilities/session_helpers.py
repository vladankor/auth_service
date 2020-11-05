from typing import Optional
from uuid import uuid4

from django.utils import timezone

from core.models import Session, User
from core.utilities.jwt_wrapper import create_jwt

from auth_service.settings.main import SERVICE_NAME
from auth_service.settings.security import JWT_LIFE_TIME_SECONDS


def is_session_exists_by_user_and_device(user: User) -> bool:
    return Session.objects\
        .filter(user=user)


def is_session_exists_by_token(token: str) -> bool:
    return Session.objects\
        .filter(token=token)


def create_session(user: User) -> Session:
    data_to_generate_jwt = {
        'iss': SERVICE_NAME,
        'sub': user.uuid,
        'aud': user.uuid,
        'exp': timezone.now() + timezone.timedelta(seconds=JWT_LIFE_TIME_SECONDS),
        'iat': timezone.now(),
        'jti': str(uuid4()) + str(uuid4()) + str(uuid4()) + str(uuid4()),
    }
    jwt_token = create_jwt(data_to_generate_jwt)
    return Session.objects\
        .create(authentication_token=jwt_token.value,
                refresh_token=str(uuid4()) + str(uuid4()) + str(uuid4()) + str(uuid4()),
                user=user,
                expires_at=jwt_token.expires_at)


def get_session_by_authentication_token(authentication_token: str) -> Optional[Session]:
    return Session.objects\
        .filter(authentication_token=authentication_token)\
        .first()


def is_session_expired(session: Session) -> bool:
    return session.expires_at > timezone.datetime.now()
