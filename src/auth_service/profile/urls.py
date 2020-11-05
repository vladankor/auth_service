from django.urls import path

from .views import *

urlpatterns = [
    path('v1/register/', register),
    path('v1/authenticate/', authenticate),
    path('v1/refresh_token/', refresh_token),
    path('v1/authorize/', authorize),
    path('v1/information/', information),
    path('v1/update/', update),
    path('v1/delete/', delete),
]