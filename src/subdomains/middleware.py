import re
import warnings
from django.utils.cache import patch_vary_headers
from django.conf import settings
from django.contrib.sites.models import Site
from subdomains.exceptions import IncorrectSiteException
from subdomains.settings import USE_SUBDOMAIN_EXCEPTION, REMOVE_WWW_FROM_SUBDOMAIN, USE_FULLY_QUALIFIED_DOMAINS


class SubdomainMiddleware(object):
    def process_request(self, request):
        """
        Adds a `subdomain` attribute to the request object, which corresponds
        to the portion of the URL before the current Site object's `domain`
        attribute.
        """
        site = Site.objects.get_current()
        domain = site.domain
        if REMOVE_WWW_FROM_SUBDOMAIN and domain.startswith("www."):
            domain = domain.replace("www.", "", 1)

        if USE_FULLY_QUALIFIED_DOMAINS:
            request.subdomain = request.get_host()
        else:
            pattern = r'^(?:(?P<subdomain>.*?)\.)?%s(?::.*)?$' % re.escape(domain)
            matches = re.match(pattern, request.get_host())

            request.subdomain = None

            if matches:
                request.subdomain = matches.group('subdomain')
            else:
                error = 'The current host, %s, does not match the Site instance ' \
                    'specified by SITE_ID.' % request.get_host()

                if USE_SUBDOMAIN_EXCEPTION:
                    raise IncorrectSiteException(error)
                else:
                    warnings.warn('%s The URLconf for this host will fall back to '
                        'the ROOT_URLCONF.' % error, UserWarning)

            # Continue processing the request as normal.
            return None


class SubdomainURLRoutingMiddleware(SubdomainMiddleware):
    def process_request(self, request):
        """
        Sets the current request's `urlconf` attribute to the URL conf
        associated with the subdomain, if listed in `SUBDOMAIN_URLCONFS`.
        """
        super(SubdomainURLRoutingMiddleware, self).process_request(request)

        subdomain = getattr(request, 'subdomain', False)
        if subdomain is not False:
            try:
                request.urlconf = settings.SUBDOMAIN_URLCONFS[subdomain]
            except KeyError:
                # There was no match in the SUBDOMAIN_URLCONFS setting, so let the
                # ROOT_URLCONF handle the URL routing for this request.
                pass

        # Continue processing the request as normal.
        return None

    def process_response(self, request, response):
        """
        Forces the HTTP Vary header onto requests to avoid having responses
        cached from incorrect urlconfs.

        If you'd like to disable this for some reason, set `FORCE_VARY_ON_HOST`
        in your Django settings file to `False`.
        """
        if getattr(settings, 'FORCE_VARY_ON_HOST', True):
            patch_vary_headers(response, ('Host',))

        return response
