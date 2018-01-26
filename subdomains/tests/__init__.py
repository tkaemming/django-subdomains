from django.conf import settings

if not settings.configured:
    MIDDLEWARES = (
        'django.middleware.common.CommonMiddleware',
        'subdomains.middleware.SubdomainURLRoutingMiddleware',
    )
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
        MIDDLEWARE_CLASSES=MIDDLEWARES,
        MIDDLEWARE=MIDDLEWARES,
        ALLOWED_HOSTS=[
            '.example.com',
        ],
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
            }
        ]
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
