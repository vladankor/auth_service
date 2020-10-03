from rest_framework.decorators import api_view
from django.http.response import HttpResponse, Http404

from auth_core.utilities.user_helpers import is_user_exists, error_user_not_found_msg


@api_view(['POST'])
def authorize(request):
    email = request.data.get('email', None)
    phone_number = request.data.get('phone_number', None)
    access_token = request.data.get('access_token', None)

    if not is_user_exists(email, phone_number):
        return Http404(content=error_user_not_found_msg(email, phone_number))

    return HttpResponse()