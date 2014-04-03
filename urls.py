# encoding: utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import (
    ABTestingSwitchVersionViewMixin
)


urlpatterns = patterns('',
    **( url(r'^(?P<version>%s)/' % version['URL_PREFIX'], views.ABTestingSwitchVersionViewMixin.as_view()) for name, version in settings.ABTESTING_VERSIONS.items() ),
)

