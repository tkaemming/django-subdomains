try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url  # noqa

try:
    from django.conf.urls import patterns
except ImportError:
    try:
        from django.conf.urls.defaults import patterns  # noqa
    except ImportError:
        def patterns(*args):
            new_patterns = []
            for a in args:
                if a:
                    new_patterns.append(a)
            return new_patterns

from subdomains.tests.views import view


urlpatterns = patterns('',
    url(regex=r'^$', view=view, name='home'),
    url(regex=r'^example/$', view=view, name='example'),
)
