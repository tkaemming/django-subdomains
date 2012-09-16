from django.conf.urls import patterns, url

from subdomains.tests.urls.default import urlpatterns as default_patterns
from subdomains.tests.views import view


urlpatterns = default_patterns + patterns('',
    url(regex=r'^$', view=view, name='home'),
    url(regex=r'^view/$', view=view, name='view'),
)
