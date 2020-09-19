from django.shortcuts import render
from rest_framework.decorators import api_view


@api_view(['POST'])
def authorize(request):
    email = request.data.get('email', None)
    phone_number = request.data.get('phone_number', None)
    password = request.data.get('password', None)

    return