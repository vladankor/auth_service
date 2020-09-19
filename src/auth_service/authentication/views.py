from rest_framework.decorators import api_view
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseServerError

from auth_core.utilities.user_helpers import is_user_exists, create_user


def validate_user_parameters(email, phone_number, password):
    if (email is None and phone_number is None) or password is None:
        return False
    return True


def error_invalid_user_parameters(email, phone_number, password):
    if email is None and phone_number is None:
        if password is None:
            return 'Email or phone number and password must not be empty'
        else:
            return 'Email or phone number must not be empty'
    if password is None:
        return 'Password must not be empty'


def error_user_already_exists(**kwargs):
    fields_str = ''
    for field_name, field_value in kwargs.items():
        if field_value is not None:
            fields_str = fields_str + '{}: {} '.format(field_name, field_value)

    return 'User with ' + fields_str + 'already exists'


@api_view(['POST'])
def register(request):
    email = request.data.get('email', None)
    phone_number = request.data.get('phone_number', None)
    password = request.data.get('password', None)
    if not validate_user_parameters(email, phone_number, password):
        return HttpResponseBadRequest(description=error_invalid_user_parameters(email, phone_number, password))

    if is_user_exists(email, phone_number):
        return HttpResponse(description=error_user_already_exists(email, phone_number), status=409)

    if create_user(email, phone_number, password) is None:
        return HttpResponseServerError(description='User creation failed')

    return HttpResponse(description='User created', status=201)
