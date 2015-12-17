from django.conf import settings

if not settings.configured:
    settings.configure(
        INSTALLED_APPS=(
            'django.contrib.sites',
            'subdomains',
        ),
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        SITE_ID=1,
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'subdomains.middleware.SubdomainURLRoutingMiddleware',
        ),
    )


from subdomains.tests.tests import *  # NOQA


def run():
    import sys

    import django
    from django.test.utils import get_runner

    if django.VERSION >= (1, 7):
        django.setup()

    runner = get_runner(settings)()
    failures = runner.run_tests(('subdomains',))
    sys.exit(failures)
