from django.urls import path
from .views import *

urlpatterns = [
    path('',home),
    path('ajax_change_status/',ajax_change_status),
    path('reset/', ResetView, name="reset"),
    path('password-reset/<uidb64>/<token>', passwordResetView, name="template"),
    path('result/approve/<pk>', approve_group, name="approve_group"),
    path('result/reject/<pk>', reject_group, name="approve_group"),
]