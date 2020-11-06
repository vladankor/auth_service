from typing import Type
from uuid import uuid4

from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from django.http.request import HttpRequest
from django.db import transaction
from django.utils import timezone

from core.utilities.security import check_password, hash_password
from core.utilities.answers import Result, Error, ErrorCode
from service.models import Service, ServiceSession, ServiceType, Token
from auth_service.settings.security import TOKEN_LIFE_TIME_SECONDS


@api_view(['POST'])
def register(request: Type[HttpRequest]):
    service_name = request.POST.get('service_name')
    service_type = request.POST.get('service_type')
    service_password = request.POST.get('service_password')
    service_client_redirection_uri = request.POST.get('service_client_redirection_uri')

    if service_name is None\
            or service_type is None\
            or service_password is None\
            or service_client_redirection_uri is None:
        return JsonResponse(data=Error(description='Invalid parameter',
                                       user_description='Invalid parameter').json,
                            status=400)

    if Service.objects\
            .filter(name=service_name)\
            .exists():
        return JsonResponse(data=Error(description=f'Service with name {service_name} already exists',
                                       user_description=f'Service with name {service_name} already exists').json,
                            status=400)

    service = Service.objects\
        .create(uuid=uuid4(),
                name=service_name,
                service_type=service_type,
                client_redirection_uri=service_client_redirection_uri,
                secret=uuid4(),
                service_password=hash_password(service_password))

    if service is None:
        return JsonResponse(data=Error(description='Failed to create service',
                                       user_description='Failed to create service').json,
                            status=500)


@api_view(['POST'])
def authenticate(request: Type[HttpRequest]):
    service_name = request.POST.get('service_name')
    service_password = request.POST.get('service_password')

    service = Service.objects\
        .filter(name=service_name)\
        .first()

    if service is None:
        return JsonResponse(data=Error(description=f'Service {service_name} not found or password is incorrect',
                                       user_description=f'Service {service_name} not found or password is incorrect').json,
                            status=400)

    if not check_password(service.service_password, service_password):
        return JsonResponse(data=Error(description=f'Service {service_name} not found or password is incorrect',
                                       user_description=f'Service {service_name} not found or password is incorrect'),
                            status=400)

    with transaction.atomic():
        service_session = ServiceSession.objects\
            .create(service=service,
                    authentication_token=uuid4(),
                    expires_at=timezone.now() + timezone.timedelta(seconds=TOKEN_LIFE_TIME_SECONDS),
                    refresh_token=uuid4())

        if service_session is None:
            return JsonResponse(data=Error(description='Failed to create service session',
                                           user_description='Failed to create service session').json,
                                status=500)

    return JsonResponse(data=Result(description='Authenticated',
                                    user_description='Authenticated',
                                    data={'authentication_token': service_session.authentication_token,
                                          'expires_at': service_session.expires_at,
                                          'refresh_token': service_session.refresh_token}).json,
                        status=200)


@api_view(['POST'])
def refresh_token(request: Type[HttpRequest]):
    pass


@api_view(['GET'])
def information(request: Type[HttpRequest], service_name: str):
    service = Service.objects\
        .filter(name=service_name)\
        .first()

    if service is None:
        return JsonResponse(data=Error(description=f'Service {service_name} not found',
                                       user_description=f'Service {service_name} not found').json,
                            status=404)

    session = ServiceSession.objects\
        .filter(service=service,
                authentication_token=request.authentication_token)\
        .first()

    if session is None or session.expires_at < timezone.now():
        return JsonResponse(data=Error(description='Unauthorized',
                                       user_description='Unauthorized').json,
                            status=403)

    return JsonResponse(data=Result(description='Authenticated',
                                    user_description='Authenticated',
                                    data={'uuid': session.service.uuid,
                                          'name': session.service.name,
                                          'type': session.service.type,
                                          'client_redirection_uri': session.service.client_redirection_uri,
                                          'secret': session.service.secret}).json,
                        status=200)


@api_view(['POST'])
def update(request: Type[HttpRequest], service_name: str):
    service = Service.objects\
        .filter(name=service_name)\
        .first()

    if service is None:
        return JsonResponse(data=Error(description=f'Service {service_name} not found',
                                       user_description=f'Service {service_name} not found').json,
                            status=404)

    session = ServiceSession.objects\
        .filter(service=service,
                authentication_token=request.authentication_token)\
        .first()

    if session is None or session.expires_at < timezone.now():
        return JsonResponse(data=Error(description='Unauthorized',
                                       user_description='Unauthorized').json,
                            status=403)

    if request.POST.get('service_name'):
        service.name = request.POST.get('service_name')
    if request.POST.get('client_redirection_uri'):
        service.client_redirection_uri = request.POST.get('client_redirection_uri')
    service.save()


@api_view(['POST'])
def delete(request: Type[HttpRequest], service_name: str):
    service = Service.objects\
        .filter(name=service_name)\
        .first()

    if service is None:
        return JsonResponse(data=Error(description=f'Service {service_name} not found',
                                       user_description=f'Service {service_name} not found').json,
                            status=404)

    session = ServiceSession.objects\
        .filter(service=service,
                authentication_token=request.authentication_token)\
        .first()

    if session is None or session.expires_at < timezone.now():
        return JsonResponse(data=Error(description='Unauthorized',
                                       user_description='Unauthorized').json,
                            status=403)

    session.service.delete()

    return JsonResponse(data=Result(description='Service deleted',
                                    user_description='Service deleted',
                                    data={'uuid': service.uuid,
                                          'name': service.name,
                                          'type': service.type,
                                          'client_redirection_uri': service.client_redirection_uri,
                                          'secret': service.secret }).json,
                        status=200)
