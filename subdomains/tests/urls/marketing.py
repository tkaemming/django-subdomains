try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url  # noqa

from subdomains.tests.urls.default import urlpatterns as default_patterns


urlpatterns = default_patterns
