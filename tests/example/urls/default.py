from django.conf.urls import patterns, url

from example.views import view


urlpatterns = patterns('',
    url(regex=r'^$', view=view),
    url(regex=r'^example/$', view=view, name='example'),
)
