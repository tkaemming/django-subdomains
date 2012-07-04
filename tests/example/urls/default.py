from django.conf.urls import patterns, url

from example.views import view


urlpatterns = patterns('',
    url(regex=r'^$', view=view, name='home'),
)
