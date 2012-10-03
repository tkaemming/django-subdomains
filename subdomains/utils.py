import functools
from urlparse import urlunparse

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse as simple_reverse


def current_site_domain():
    return Site.objects.get_current().domain

get_domain = current_site_domain


def urljoin(domain, path=None, scheme=None):
    """
    Joins a domain, path and scheme part together, returning a full URL.

    :param domain: the domain, e.g. ``example.com``
    :param path: the path part of the URL, e.g. ``/example/``
    :param scheme: the scheme part of the URL
    :returns: a full URL
    """
    return urlunparse((scheme, domain, path or '', None, None, None))


def reverse(viewname, subdomain=None, scheme=None, args=None, kwargs=None,
        current_app=None, request=None):
    """
    Reverses a URL from the given parameters, in a similar fashion to
    :meth:`django.core.urlresolvers.reverse`.

    :param viewname: the name of URL
    :param subdomain: the subdomain to use for URL reversing
    :param scheme: the scheme to use when generating the full URL, defaults to
        the value of ``settings.DEFAULT_URL_SCHEME``
    :param args: positional arguments used for URL reversing
    :param kwargs: named arguments used for URL reversing
    :param current_app: hint for the currently executing application
    """
    urlconf = settings.SUBDOMAIN_URLCONFS.get(subdomain)
    if scheme is None:
        scheme = getattr(settings, 'DEFAULT_URL_SCHEME', 'http')

    domain = get_domain()
    if subdomain is not None:
        domain = '%s.%s' % (subdomain, domain)

    path = simple_reverse(viewname, urlconf=urlconf, args=args, kwargs=kwargs,
        current_app=current_app)

    if request and domain == request.get_host():
        if scheme is '' or (
            (scheme is 'http' and not request.is_secure()) or
            (scheme is 'https' and request.is_secure())):
            return path

    return urljoin(domain, path, scheme=scheme)


#: :func:`reverse` bound to insecure (non-HTTPS) URLs scheme
insecure_reverse = functools.partial(reverse, scheme='http')

#: :func:`reverse` bound to secure (HTTPS) URLs scheme
secure_reverse = functools.partial(reverse, scheme='https')

#: :func:`reverse` bound to be relative to the current scheme
relative_reverse = functools.partial(reverse, scheme='')
