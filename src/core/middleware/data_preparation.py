from typing import Callable, Any, Type, Optional

from django.http import HttpRequest, HttpResponse

from core.utilities.headers import XHTTPRequestHeaders, HTTPRequestHeaders


class DataPreparationMiddleware:
    def __init__(self, get_response: Callable[[...], Any]):
        self.get_response = get_response

    def __call__(self, request: Type[HttpRequest]) -> Type[HttpResponse]:
        # UserAgentMiddleware adds field user_agent
        request.user_agent.device.id = request.META.get(XHTTPRequestHeaders.X_DEVICE_ID.value, None)
        request.authentication_token = self.__extract_authentication_token(request)
        return self.get_response(request)

    @classmethod
    def __extract_authentication_token(cls, request: Type[HttpRequest]) -> Optional[str]:
        # Try get from authorization with bearer type
        authentication_token = cls.__extract_authentication_token_token_from_authorization_header(request)
        if authentication_token is None:
            # Try get from custom header
            authentication_token = cls.__extract_authentication_token_token_from_authentication_token_token_header(request)
        return authentication_token

    @classmethod
    def __extract_authentication_token_token_from_authorization_header(cls, request) -> Optional[str]:
        authentication_token = None
        try:
            authorization_header = request.META.get(HTTPRequestHeaders.AUTHORIZATION.value).decode('utf-8')
            if not authorization_header:
                return None
            params = authorization_header.split()
            if len(params) != 2:
                return None
            authentication_scheme, authentication_token = params
            if authentication_scheme != 'bearer':
                return None
        except AttributeError as e:
            # TODO: Add error message
            pass
        return authentication_token

    @classmethod
    def __extract_authentication_token_token_from_authentication_token_header(cls, request) -> str:
        return request.META.get(XHTTPRequestHeaders.X_AUTHENTICATION_TOKEN.value)




