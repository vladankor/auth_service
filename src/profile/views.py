from typing import Type

from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from django.http.request import HttpRequest
from django.db import transaction

from core.utilities.user_helpers import (
    is_user_exists,
    create_user,
    result_user_create_msg,
    error_user_invalid_parameters_msg,
    error_user_create_msg,
    error_user_already_exists_msg,
    get_user,
    error_user_not_found_msg,
    error_invalid_password,
)
from core.utilities.answers import Result, Error, ErrorCode
from core.utilities.security import check_password
from core.utilities.session_helpers import create_session
from core.utilities.headers import XHTTPRequestHeaders, HTTPRequestHeaders
from core.models import Session


def validate_user_parameters(email, phone_number, password):
    if (email is None and phone_number is None) or password is None:
        return False
    return True


@api_view(['POST'])
def register(request: Type[HttpRequest]):
    email = request.POST.get('email', None)
    phone_number = request.POST.get('phone_number', None)
    password = request.POST.get('password', None)
    if not validate_user_parameters(email, phone_number, password):
        return JsonResponse(data=error_user_invalid_parameters_msg(email=email,
                                                                   phone_number=phone_number,
                                                                   password=password,
                                                                   error_code=ErrorCode.USER_NOT_CREATED.value).json,
                            status=400)

    if is_user_exists(email, phone_number):
        return JsonResponse(data=error_user_already_exists_msg(email=email,
                                                               phone_number=phone_number).json,
                            status=409)

    if create_user(email, phone_number, password) is None:
        return JsonResponse(data=error_user_create_msg().json,
                            status=500)

    return JsonResponse(data=result_user_create_msg().json,
                        status=201)


@api_view(['POST'])
def authenticate(request: Type[HttpRequest]):
    email = request.POST.get('email', None)
    phone_number = request.POST.get('phone_number', None)
    password = request.POST.get('password', None)
    if not validate_user_parameters(email, phone_number, password):
        return JsonResponse(data=error_user_invalid_parameters_msg(email=email,
                                                                   phone_number=phone_number,
                                                                   password=password,
                                                                   error_code=ErrorCode.INVALID_PARAMETERS.value),
                            status=400)

    u = get_user(email, phone_number)
    if u is None:
        return JsonResponse(data=error_user_not_found_msg(email=email, phone_number=phone_number).json,
                            status=400)
    if not check_password(u.password, password):
        return JsonResponse(data=error_invalid_password().json)

    with transaction.atomic():
        s = create_session(u)
        if s is None:
            return JsonResponse(data=Error(description='Failed to create session',
                                           user_description='Failed to create session',
                                           error_code=ErrorCode.SESSION_NOT_FOUND.value).json,
                                status=500)

        response = JsonResponse(data=Result(description='Authenticated',
                                            user_description='Authenticated',
                                            data={'authentication_token': s.authentication_token,
                                                  'refresh_token': s.refresh_token}).json,
                                status=200)
        return response


@api_view(['POST'])
def refresh_token(request: Type[HttpRequest]):
    authentication_token_value = request.POST.get('authentication_token')
    refresh_token_value = request.POST.get('refresh_token')
    device_id_value = request.POST.get('device_id')

    session = Session.objects\
        .filter(authentication_token=authentication_token_value)\
        .select_related('user', 'device')\
        .first()
    if not session:
        return JsonResponse(data=Error(description='Invalid token',
                                       user_description='Invalid token',
                                       error_code=ErrorCode.SESSION_NOT_FOUND.value).json,
                            status=403)

    if session.refresh_token != refresh_token_value:
        return JsonResponse(data=Error(description='Invalid refresh token',
                                       user_description='Invalid refresh token',
                                       error_code=ErrorCode.SESSION_NOT_FOUND.value).json,
                            status=403)

    if session.device_id != device_id_value:
        return JsonResponse(data=Error(description='Unauthenticated device',
                                       user_description='Unauthenticated device',
                                       error_code=ErrorCode.SESSION_NOT_FOUND.value).json,
                            status=403)

    with transaction.atomic():
        d = session.device
        u = session.user
        s = create_session(u)

        session.delete()

        response = JsonResponse(data=Result(description='Refreshed',
                                            user_description='Refreshed',
                                            data={'authentication_token': s.authentication_token,
                                                  'refresh_token': s.refresh_token,
                                                  'device_id': d.id}).json,
                                status=200)
        return response


@api_view(['GET'])
def authorize(request: Type[HttpRequest]):
    authentication_token_value = request.headers.get(XHTTPRequestHeaders.X_AUTHENTICATION_TOKEN, None)
    device_id_value = request.headers.get(XHTTPRequestHeaders.X_DEVICE_ID, None)

    if authentication_token_value is None or device_id_value is None:
        return

    return JsonResponse(data=Result(description='Authorized',
                                    user_description='Authorized',
                                    data={}).json,
                        status=200)


@api_view(['GET'])
def information(request: Type[HttpRequest]):
    pass


@api_view(['POST'])
def update(request: Type[HttpRequest]):
    authentication_token_value = request.headers.get(XHTTPRequestHeaders.X_AUTHENTICATION_TOKEN, None)
    device_id_value = request.POST.get(XHTTPRequestHeaders.X_DEVICE_ID, None)


@api_view(['POST', 'DELETE'])
def delete(request: Type[HttpRequest]):
    pass