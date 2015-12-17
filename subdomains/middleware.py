import operator
import logging
import re

from django.conf import settings
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured
from django.utils.cache import patch_vary_headers

from subdomains.utils import UNSET
from subdomains.utils import current_site_domain
from subdomains.utils import subdomain_globals

logger = logging.getLogger(__name__)
lower = operator.methodcaller('lower')


class SubdomainMiddleware(object):
    """
    A middleware class that adds a ``subdomain`` attribute to the
    current request, and a thread local ``domain`` attribute.
    """

    def get_domain_for_request(self, request):
        """
        Returns the domain that will be used to identify the subdomain part
        for this request.
        """

        fn_path = getattr(settings, 'SUBDOMAIN_GET_DOMAIN')
        if not fn_path:
            get_domain_for_request = lambda request: current_site_domain()
        else:
            module_name, fn_name = fn_path.rsplit('.', 1)
            try:
                module = import_module(module_name)
                fn = getattr(module, fn_name)
                assert callable(fn)
            except (ImportError, AttributeError, AssertionError):
                raise ImproperlyConfigured('SUBDOMAIN_GET_DOMAIN doesn\'t exist or'
                                           ' isn\'t a callable.')
            else:
                get_domain_for_request = fn

        return get_domain_for_request(request)


    def process_request(self, request):
        """
        Adds a ``subdomain`` attribute to the ``request`` parameter, and
        a ``domain`` attribute to thread.local.
        """

        domain, host = map(lower,
            (self.get_domain_for_request(request), request.get_host()))

        subdomain_globals.domain = domain

        pattern = r'^(?:(?P<subdomain>.*?)\.)?%s(?::.*)?$' % re.escape(domain)
        matches = re.match(pattern, host)

        if matches:
            request.subdomain = matches.group('subdomain')
        else:
            request.subdomain = None
            logger.warning('The host %s does not belong to the domain %s, '
                'unable to identify the subdomain for this request',
                request.get_host(), domain)


class SubdomainURLRoutingMiddleware(SubdomainMiddleware):
    """
    A middleware class that allows for subdomain-based URL routing.
    """
    def process_request(self, request):
        """
        Sets the current request's ``urlconf`` attribute to the urlconf
        associated with the subdomain, if it is listed in
        ``settings.SUBDOMAIN_URLCONFS``.
        """
        super(SubdomainURLRoutingMiddleware, self).process_request(request)

        subdomain = getattr(request, 'subdomain', UNSET)

        if subdomain is not UNSET:
            urlconf = settings.SUBDOMAIN_URLCONFS.get(subdomain)
            if urlconf is not None:
                logger.debug("Using urlconf %s for subdomain: %s",
                    repr(urlconf), repr(subdomain))
                request.urlconf = urlconf

    def process_response(self, request, response):
        """
        Forces the HTTP ``Vary`` header onto requests to avoid having responses
        cached across subdomains.
        """
        if getattr(settings, 'FORCE_VARY_ON_HOST', True):
            patch_vary_headers(response, ('Host',))

        return response
