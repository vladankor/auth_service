from django.urls import path

from .views import *

urlpatterns = [
    path('v1/register/', register),
    path('v1/authenticate/', authenticate),
    path('v1/refresh_token/', refresh_token),
    path('v1/information/<str:service_name>', information),
    path('v1/update/<str:service_name>', update),
    path('v1/delete/<str:service_name>', delete),
]