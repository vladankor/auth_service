from rest_framework.decorators import api_view
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseServerError

from auth_core.utilities.user_helpers import is_user_exists, create_user, error_user_already_exists_msg


def validate_user_parameters(email, phone_number, password):
    if (email is None and phone_number is None) or password is None:
        return False
    return True


def error_invalid_user_parameters_msg(email, phone_number, password) -> str:
    if email is None and phone_number is None:
        if password is None:
            return 'Email or phone number and password must not be empty'
        else:
            return 'Email or phone number must not be empty'
    if password is None:
        return 'Password must not be empty'


@api_view(['POST'])
def register(request):
    email = request.data.get('email', None)
    phone_number = request.data.get('phone_number', None)
    password = request.data.get('password', None)
    if not validate_user_parameters(email, phone_number, password):
        return HttpResponseBadRequest(content=error_invalid_user_parameters_msg(email, phone_number, password))

    if is_user_exists(email, phone_number):
        return HttpResponse(content=error_user_already_exists_msg(email, phone_number), status=409)

    if create_user(email, phone_number, password) is None:
        return HttpResponseServerError(content='User creation failed')

    return HttpResponse(content='User created', status=201)
