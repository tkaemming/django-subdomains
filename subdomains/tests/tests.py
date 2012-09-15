import contextlib
import mock
import warnings

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.contrib.sites.models import Site

from subdomains.middleware import (SubdomainMiddleware,
    SubdomainURLRoutingMiddleware)


def prefix_values(dictionary, prefix):
    return dict((key, '%s.%s' % (prefix, value))
        for key, value in dictionary.iteritems())


class SubdomainTestMixin(object):
    DOMAIN = 'example.com'
    URL_MODULE_PATH = 'subdomains.tests.urls'

    def setUp(self):
        super(SubdomainTestMixin, self).setUp()
        self.site = Site.objects.get_current()
        self.site.domain = self.DOMAIN
        self.site.save()

    @override_settings(ROOT_URLCONF='%s.application' % URL_MODULE_PATH,
        SUBDOMAIN_URLCONFS=prefix_values({
            None: 'marketing',
            'api': 'api',
            'www': 'marketing',
        }, prefix=URL_MODULE_PATH),
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'subdomains.middleware.SubdomainURLRoutingMiddleware',
        ))
    def run(self, *args, **kwargs):
        super(SubdomainTestMixin, self).run(*args, **kwargs)

    def get_path_to_urlconf(self, name):
        """
        Returns the full path to the given urlconf.
        """
        return '.'.join((self.URL_MODULE_PATH, name))

    def get_host_for_subdomain(self, subdomain=None):
        """
        Returns the hostname for the provided subdomain.
        """
        if subdomain is not None:
            host = '%s.%s' % (subdomain, self.site.domain)
        else:
            host = '%s' % self.site.domain
        return host


class SubdomainMiddlewareTestCase(SubdomainTestMixin, TestCase):
    def setUp(self):
        super(SubdomainMiddlewareTestCase, self).setUp()
        self.middleware = SubdomainMiddleware()

    def test_subdomain_attribute(self):
        def subdomain(subdomain):
            """
            Returns the subdomain associated with the request by the middleware
            for the given subdomain.
            """
            host = self.get_host_for_subdomain(subdomain)
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

        self.site.domain = 'www.%s' % self.DOMAIN
        self.site.save()

        with self.settings(REMOVE_WWW_FROM_DOMAIN=False):
            self.assertEqual(host('www.%s' % self.DOMAIN), None)

            # Squelch the subdomain warning for cleaner test output, since we
            # already know that this is an invalid subdomain.
            with warnings.catch_warnings(record=True) as warnlist:
                self.assertEqual(host('www.subdomain.%s' % self.DOMAIN), None)
                self.assertEqual(host('subdomain.%s' % self.DOMAIN), None)

            # Trick pyflakes into not warning us about variable usage.
            del warnlist

            self.assertEqual(host('subdomain.www.%s' % self.DOMAIN),
                'subdomain')
            self.assertEqual(host('www.subdomain.www.%s' % self.DOMAIN),
                'www.subdomain')

        with self.settings(REMOVE_WWW_FROM_DOMAIN=True):
            self.assertEqual(host('www.%s' % self.DOMAIN), 'www')
            self.assertEqual(host('subdomain.%s' % self.DOMAIN), 'subdomain')
            self.assertEqual(host('subdomain.www.%s' % self.DOMAIN),
                'subdomain.www')

    def test_case_insensitive_subdomain(self):
        host = 'WWW.%s' % self.DOMAIN
        request = RequestFactory().get('/', HTTP_HOST=host)
        self.middleware.process_request(request)
        self.assertEqual(request.subdomain, 'www')

        host = 'www.%s' % self.DOMAIN.upper()
        request = RequestFactory().get('/', HTTP_HOST=host)
        self.middleware.process_request(request)
        self.assertEqual(request.subdomain, 'www')


class SubdomainURLRoutingTestCase(SubdomainTestMixin, TestCase):
    def setUp(self):
        super(SubdomainURLRoutingTestCase, self).setUp()
        self.middleware = SubdomainURLRoutingMiddleware()

    def test_url_routing(self):
        def urlconf(subdomain):
            """
            Returns the URLconf associated with this request.
            """
            host = self.get_host_for_subdomain(subdomain)
            request = RequestFactory().get('/', HTTP_HOST=host)
            self.middleware.process_request(request)
            return getattr(request, 'urlconf', None)

        self.assertEqual(urlconf(None), self.get_path_to_urlconf('marketing'))
        self.assertEqual(urlconf('www'), self.get_path_to_urlconf('marketing'))
        self.assertEqual(urlconf('api'), self.get_path_to_urlconf('api'))

        # Falls through to the actual ROOT_URLCONF.
        self.assertEqual(urlconf('subdomain'), None)

    def test_appends_slash(self):
        for subdomain in (None, 'api', 'wildcard'):
            host = self.get_host_for_subdomain(subdomain)
            response = self.client.get('/example', HTTP_HOST=host)
            self.assertEqual(response.status_code, 301)
            self.assertEqual(response['Location'], 'http://%s/example/' % host)
