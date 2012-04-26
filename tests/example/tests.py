import warnings

from django.contrib.sites.models import Site
from django.test import TestCase
from django.test.client import RequestFactory

from subdomains.middleware import (SubdomainMiddleware,
    SubdomainURLRoutingMiddleware)


class SubdomainMiddlewareTestCase(TestCase):
    def setUp(self):
        self.site = Site.objects.get_current()
        self.middleware = SubdomainMiddleware()

    def test_subdomain_attribute(self):
        def subdomain(subdomain):
            """
            Returns the request.subdomain for the provided subdomain.
            """
            if subdomain is not None:
                host = '%s.%s' % (subdomain, self.site.domain)
            else:
                host = '%s' % self.site.domain
            request = RequestFactory().get('/', HTTP_HOST=host)
            self.middleware.process_request(request)
            return request.subdomain

        self.assertEqual(subdomain(None), None)
        self.assertEqual(subdomain('www'), 'www')
        self.assertEqual(subdomain('www.subdomain'), 'www.subdomain')
        self.assertEqual(subdomain('subdomain'), 'subdomain')
        self.assertEqual(subdomain('another.subdomain'), 'another.subdomain')

    def test_www_domain(self):
        def host(host):
            """
            Returns the subdomain for the provided HTTP Host.
            """
            request = RequestFactory().get('/', HTTP_HOST=host)
            self.middleware.process_request(request)
            return request.subdomain

        self.site.domain = 'www.example.com'
        self.site.save()

        with self.settings(REMOVE_WWW_FROM_DOMAIN=False):
            self.assertEqual(host('www.example.com'), None)

            # Squelch the subdomain warning for cleaner test output, since we
            # already know that this is an invalid subdomain.
            with warnings.catch_warnings(record=True) as warnlist:
                self.assertEqual(host('www.subdomain.example.com'), None)
                self.assertEqual(host('subdomain.example.com'), None)

            # Trick pyflakes into not warning us about variable usage.
            del warnlist

            self.assertEqual(host('subdomain.www.example.com'), 'subdomain')
            self.assertEqual(host('www.subdomain.www.example.com'),
                'www.subdomain')

        with self.settings(REMOVE_WWW_FROM_DOMAIN=True):
            self.assertEqual(host('www.example.com'), 'www')
            self.assertEqual(host('subdomain.example.com'), 'subdomain')
            self.assertEqual(host('subdomain.www.example.com'),
                'subdomain.www')


class SubdomainURLRoutingTestCase(TestCase):
    def setUp(self):
        self.site = Site.objects.get_current()
        self.middleware = SubdomainURLRoutingMiddleware()

    def test_url_routing(self):
        def urlconf(subdomain):
            """
            Returns the URLconf associated with this request.
            """
            if subdomain is not None:
                host = '%s.%s' % (subdomain, self.site.domain)
            else:
                host = '%s' % self.site.domain
            request = RequestFactory().get('/', HTTP_HOST=host)
            self.middleware.process_request(request)
            return getattr(request, 'urlconf', None)

        self.assertEqual(urlconf(None), 'example.urls.marketing')
        self.assertEqual(urlconf('www'), 'example.urls.marketing')
        self.assertEqual(urlconf('api'), 'example.urls.api')

        # Falls through to the actual ROOT_URLCONF.
        self.assertEqual(urlconf('subdomain'), None)
