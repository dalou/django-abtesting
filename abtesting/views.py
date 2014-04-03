# encoding: utf-8

import logging 

from django.conf import settings
from django.views import generic
from django.db.models import Count, get_model
from django.template import loader
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import RedirectView
from django.shortcuts import redirect

logger = logging.getLogger(__name__)


class ABTestingSwitchVersionView(RedirectView):

	session_key = 'version'
	permanent = True
	query_string = True
	redirect_url = None

	def dispatch(self, request, version, *args, **kwargs):

		for name, config in settings.ABTESTING_VERSIONS.items():
			url_prefix = config['URL_PREFIX']

			if version == url_prefix:
				url_prefix = config['URL_PREFIX']
				request.session[self.session_key] = name
				version_prefix = '%s/' % url_prefix
				unversionned_path = request.path[0] + request.path[1:].lstrip(version_prefix)
				self.redirect_url = unversionned_path
				return redirect(unversionned_path)
		raise Http404


class ABTestingViewMixin(object):

	session_key = 'version'
	force_change_ctx_template_name = False
	version = None
	version_template_prefix = None

	def dispatch(self, request, *args, **kwargs):

		self.version = None
		self.version_template_prefix = None

		if self.session_key in request.session:	
			version = request.session[self.session_key]	
			if version in settings.ABTESTING_VERSIONS:
				self.version = version
				template_prefix = settings.ABTESTING_VERSIONS[version]['TEMPLATES_PREFIX']
				if template_prefix and template_prefix.strip() != '':	
					self.version_template_prefix = template_prefix

		print self.version_template_prefix

		self.template_name = self.abtesting_process_template(self.template_name)

		return super(ABTestingViewMixin, self).dispatch(request, *args, **kwargs)

	def is_version(self, version):
		return self.version

	def abtesting_process_template(self, template):
		if self.version_template_prefix:
			template = ("/%s/" % self.version_template_prefix).join(template.split('/', 1))
		return template


