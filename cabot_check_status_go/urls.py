from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from cabot.rest_urls import create_viewset, status_check_fields

from .views import (StatusGoCheckCreateView, StatusGoCheckUpdateView, duplicate_check)
from .models import StatusGoStatusCheck

api_router = DefaultRouter()
api_router.register(r'status_go_checks', create_viewset(
    arg_model=StatusGoStatusCheck,
    arg_fields=status_check_fields + (
        'node_type',
        'enode',
    ),
))

urlpatterns = [

    url(r'^statusgocheck/create/',
        view=StatusGoCheckCreateView.as_view(),
        name='create-status-go-check'),

    url(r'^statusgocheck/update/(?P<pk>\d+)/',
        view=StatusGoCheckUpdateView.as_view(),
        name='update-status-go-check'),

    url(r'^statusgocheck/duplicate/(?P<pk>\d+)/',
        view=duplicate_check,
        name='duplicate-status-go-check'),

    url(r'^api/', include(api_router.urls)),
]
