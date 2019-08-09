import functools

try:
    from urlparse import urlunparse
except ImportError:
    from urllib.parse import urlunparse

from django.conf import settings
from django.urls import reverse as simple_reverse


def current_site_object(request=None):
    from django.conf import settings
    from django.contrib.sites.models import Site
    from django.contrib.sites.models import SITE_CACHE
    from django.core.exceptions import ImproperlyConfigured
    from django.http.request import split_domain_port

    if getattr(settings, 'SITE_ID', ''):
        site_id = settings.SITE_ID
        if site_id not in SITE_CACHE:
            site = Site.objects.get(pk=site_id)
            SITE_CACHE[site_id] = site
        return SITE_CACHE[site_id]
    elif request:
        host = request.get_host()
        try:
            # First attempt to look up the site by host with or without port.
            if host not in SITE_CACHE:
                SITE_CACHE[host] = Site.objects.get(domain__iexact=host)
            return SITE_CACHE[host]
        except Site.DoesNotExist:
            try:
                # Fallback to looking up site after stripping port from the host.
                domain, port = split_domain_port(host)
                if domain not in SITE_CACHE:
                    SITE_CACHE[domain] = Site.objects.get(
                        domain__iexact=domain)
            except Site.DoesNotExist:
                domain, port = split_domain_port(host)
                for i in range(1, len(domain.split('.'))):
                    sbd = ".".join(domain.split('.')[i:])
                    if sbd not in SITE_CACHE:
                        site = Site.objects.filter(
                            domain__iexact=sbd).first()
                        if site:
                            domain = sbd
                            SITE_CACHE[domain] = site
                            break
                    else:
                        domain = sbd
                        break
                else:
                    raise ImproperlyConfigured(
                        "You're using the Django \"sites framework\" without having "
                        "set the SITE_ID setting. Create a site in your database and "
                        "set the SITE_ID setting or pass a request to "
                        "Site.objects.get_current() to fix this error."
                    )

            return SITE_CACHE[domain]


def current_site_domain(request=None):
    from django.conf import settings
    domain = current_site_object(request=request).domain
    prefix = 'www.'
    if getattr(settings, 'REMOVE_WWW_FROM_DOMAIN', False) \
            and domain.startswith(prefix):
        domain = domain.replace(prefix, '', 1)

    return domain


get_domain = current_site_domain


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


def reverse(viewname, subdomain=None, scheme=None, args=None, kwargs=None,
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
    urlconf = settings.SUBDOMAIN_URLCONFS.get(subdomain, settings.ROOT_URLCONF)

    domain = get_domain()
    if subdomain is not None:
        domain = '%s.%s' % (subdomain, domain)

    path = simple_reverse(viewname, urlconf=urlconf, args=args, kwargs=kwargs,
                          current_app=current_app)
    return urljoin(domain, path, scheme=scheme)


#: :func:`reverse` bound to insecure (non-HTTPS) URLs scheme
insecure_reverse = functools.partial(reverse, scheme='http')

#: :func:`reverse` bound to secure (HTTPS) URLs scheme
secure_reverse = functools.partial(reverse, scheme='https')

#: :func:`reverse` bound to be relative to the current scheme
relative_reverse = functools.partial(reverse, scheme='')
