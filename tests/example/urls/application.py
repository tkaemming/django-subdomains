from django.conf.urls import patterns, url

from example.urls.default import urlpatterns as default_patterns
from example.views import view


urlpatterns = default_patterns + patterns('',
    url(regex=r'^view/$', view=view, name='view'),
)
