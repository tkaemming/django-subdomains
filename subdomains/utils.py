from urlparse import urlunparse

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse as simple_reverse


def urljoin(domain, path=None, scheme=None):
    if path is None:
        path = ''

    if scheme is None:
        scheme = getattr(settings, 'DEFAULT_URL_SCHEME', 'http')

    return urlunparse((scheme, domain, path, None, None, None))


def reverse(viewname, subdomain=None, scheme=None, urlconf=None,
        *args, **kwargs):
    # We imply the urlconf from the `subdomain` argument -- providing the
    # urlconf is a violation of this logic.
    if urlconf is not None:
        raise ValueError('`subdomains.utils.reverse` does not accept the '
            '`urlconf` argument.')

    site = Site.objects.get_current()
    urlconf = settings.SUBDOMAIN_URLCONFS.get(subdomain)
    if subdomain:
        domain = '%s.%s' % (subdomain, site.domain)
    else:
        domain = site.domain

    path = simple_reverse(viewname, urlconf=urlconf, *args, **kwargs)
    return urljoin(domain, path, scheme=scheme)
