from django.urls import path
from .views import *

urlpatterns = [
    path('',home),
    path('ajax_change_status/',ajax_change_status)
]