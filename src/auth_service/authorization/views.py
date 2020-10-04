from rest_framework.decorators import api_view
from django.http.response import JsonResponse

from auth_core.utilities.user_helpers import (
    is_user_exists,
    error_user_not_found_msg,
    result_user_created_msg,
)
from auth_core.utilities.answers import Result, Error, ErrorCode


@api_view(['POST'])
def authorize(request):
    email = request.data.get('email', None)
    phone_number = request.data.get('phone_number', None)
    access_token = request.data.get('access_token', None)

    if not is_user_exists(email, phone_number):
        return JsonResponse(data=error_user_not_found_msg(email=email, phone_number=phone_number),
                            status=404)

    return JsonResponse(data=result_user_created_msg(result='Successful').result)
