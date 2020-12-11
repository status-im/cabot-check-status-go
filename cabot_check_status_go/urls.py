from django.conf.urls import url

from .views import (StatusGoCheckCreateView, StatusGoCheckUpdateView, duplicate_check)

urlpatterns = [

    url(r'^statusgocheck/create/',
        view=StatusGoCheckCreateView.as_view(),
        name='create-status-go-check'),

    url(r'^statusgocheck/update/(?P<pk>\d+)/',
        view=StatusGoCheckUpdateView.as_view(),
        name='update-status-go-check'),

    url(r'^statusgocheck/duplicate/(?P<pk>\d+)/',
        view=duplicate_check,
        name='duplicate-status-go-check')

]
