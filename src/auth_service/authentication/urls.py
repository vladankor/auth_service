from django.urls import path

from auth_service.authentication.views import (
    register,
    authorize,
)

urlpatterns = [
    path('/register/', register),
    path('/authorize/', authorize),
]