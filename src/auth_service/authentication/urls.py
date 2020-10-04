from django.urls import path

from authentication.views import (
    register,
    authenticate,
)

urlpatterns = [
    path('/register/', register),
    path('/authorize/', authenticate),
]