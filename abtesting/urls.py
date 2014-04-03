# encoding: utf-8
from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import (
    ABTestingSwitchVersionView
)

if hasattr(settings, 'ABTESTING_VERSIONS'):

	urlpatterns = patterns('',
	    *( url(r'^(?P<version>%s)/' % version['URL_PREFIX'], ABTestingSwitchVersionView.as_view()) for name, version in settings.ABTESTING_VERSIONS.items() )
	)

