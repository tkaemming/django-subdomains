import functools
import threading
try:
    from urlparse import urlunparse
except ImportError:
    from urllib.parse import urlunparse

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse as simple_reverse
from django.core.urlresolvers import NoReverseMatch

subdomain_globals = threading.local()
UNSET = object()


def current_site_domain():
    domain = Site.objects.get_current().domain

    prefix = 'www.'
    if getattr(settings, 'REMOVE_WWW_FROM_DOMAIN', False) \
            and domain.startswith(prefix):
        domain = domain.replace(prefix, '', 1)

    return domain


def get_domain():
    domain = getattr(subdomain_globals, 'domain', None)
    if not domain:
        return current_site_domain()
    else:
        return domain


def urljoin(domain, path=None, scheme=None):
    """
    Joins a domain, path and scheme part together, returning a full URL.

    :param domain: the domain, e.g. ``example.com``
    :param path: the path part of the URL, e.g. ``/example/``
    :param scheme: the scheme part of the URL, e.g. ``http``, defaulting to the
        value of ``settings.DEFAULT_URL_SCHEME``
    :returns: a full URL
    """
    if scheme is None:
        scheme = getattr(settings, 'DEFAULT_URL_SCHEME', 'http')

    return urlunparse((scheme, domain, path or '', None, None, None))


def reverse(viewname, subdomain=UNSET, scheme=None, args=None, kwargs=None,
        current_app=None):
    """
    Reverses a URL from the given parameters, in a similar fashion to
    :meth:`django.core.urlresolvers.reverse`.

    :param viewname: the name of URL
    :param subdomain: the subdomain to use for URL reversing
    :param scheme: the scheme to use when generating the full URL
    :param args: positional arguments used for URL reversing
    :param kwargs: named arguments used for URL reversing
    :param current_app: hint for the currently executing application
    """

    if subdomain is not UNSET:
        urlconf = settings.SUBDOMAIN_URLCONFS.get(subdomain, settings.ROOT_URLCONF)
        path = simple_reverse(viewname, urlconf=urlconf, args=args, kwargs=kwargs,
                              current_app=current_app)
    else:
        path = None
        for subdomain, urlconf in settings.SUBDOMAIN_URLCONFS.items():
            try:
                path = simple_reverse(viewname, urlconf=urlconf, args=args, kwargs=kwargs,
                                      current_app=current_app)
            except NoReverseMatch:
                path = None
            else:
                break
        if not path:
            raise NoReverseMatch("Reverse for '%s' with arguments '%s' and keyword "
                                 "arguments '%s' not found." % (viewname, args, kwargs))

    domain = get_domain()
    if subdomain is not None:
        domain = '%s.%s' % (subdomain, domain)

    return urljoin(domain, path, scheme=scheme)


#: :func:`reverse` bound to insecure (non-HTTPS) URLs scheme
insecure_reverse = functools.partial(reverse, scheme='http')

#: :func:`reverse` bound to secure (HTTPS) URLs scheme
secure_reverse = functools.partial(reverse, scheme='https')

#: :func:`reverse` bound to be relative to the current scheme
relative_reverse = functools.partial(reverse, scheme='')
