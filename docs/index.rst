django-subdomains
=================

Subdomain helpers for the Django framework, including subdomain-based URL
routing and reversing.

Installation
------------

This application is available via the
`Python Package Index <http://pypi.python.org/pypi/django-subdomains>`_ and can
be installed with any Python package manager, such as ``pip`` or ``easy_install``
by running::

    pip install django-subdomains

or::

    easy_install django-subdomains

It is highly recommended to use package version numbers when using this project
as a dependency to ensure API consistency.

To install the latest version from the repository source, clone the repository
and then run ``make install`` in the repository directory.

Quick Start
-----------

To set up subdomain URL routing and reversing in a Django project:

1. Add :class:`subdomains.middleware.SubdomainURLRoutingMiddleware` to your
   ``MIDDLEWARE_CLASSES`` in your Django settings file. If you are using
   :class:`django.middleware.common.CommonMiddleware`, the subdomain middleware
   should come before :class:`~django.middleware.common.CommonMiddleware`.
2. Configure your ``SUBDOMAIN_URLCONFS`` dictionary in your Django settings file.
3. Ensure that you've set up your ``SITE_ID`` in your Django settings file,
   and that the ``Site.domain`` attribute for that site corresponds to the
   domain name where users will be accessing your site at.
4. If you want to use the subdomain-based ``{% url %}`` template tag, add
   ``subdomains`` to your ``INSTALLED_APPS``.

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

::

    # This is the urlconf that will be used for any subdomain that is not
    # listed in ``SUBDOMAIN_URLCONFS``, or if the HTTP ``Host`` header does not
    # contain the correct domain.
    # If you're planning on using wildcard subdomains, this should correspond
    # to the urlconf that will be used for the wildcard subdomain. For example,
    # 'accountname.mysite.com' will load the ROOT_URLCONF, since it is not 
    # defined in ``SUBDOMAIN_URLCONFS``.
    ROOT_URLCONF = 'myproject.urls.account'

    # A dictionary of urlconf module paths, keyed by their subdomain.
    SUBDOMAIN_URLCONFS = {
        None: 'myproject.urls.frontend',  # no subdomain, e.g. ``example.com``
        'www': 'myproject.urls.frontend',
        'api': 'myproject.urls.api',
    }

Basic Usage
-----------

Using Subdomains in Views
~~~~~~~~~~~~~~~~~~~~~~~~~

On each request, a ``subdomain`` attribute will be added to the ``request``
object. You can use this attribute to effect view logic, like in this example::

    def user_profile(request):
        try:
            # Retrieve the user account associated with the current subdomain.
            user = User.objects.get(username=request.subdomain)
        except User.DoesNotExist:
            # No user matches the current subdomain, so return a generic 404.
            raise Http404

Resolving Named URLs by Subdomain
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Included is a :func:`subdomains.utils.reverse` function that responds similarly to
:func:`django.core.urlresolvers.reverse`, but accepts optional ``subdomain``
and ``scheme`` arguments and does not allow a ``urlconf`` parameter.

If no ``subdomain`` argument is provided, the URL will be resolved relative to
the ``SUBDOMAIN_URLCONFS[None]`` or ``ROOT_URLCONF``, in order. The protocol
scheme is the value of ``settings.DEFAULT_URL_SCHEME``, or if unset, ``http``::

    >>> from subdomains.utils import reverse
    >>> reverse('home')
    'http://example.com/'
    >>> reverse('user-profile', kwargs={'username': 'ted'})
    'http://example.com/users/ted/'
    >>> reverse('home', scheme='https')
    'https://example.com/'

For subdomains, the URL will be resolved relative to the
``SUBDOMAIN_URLCONFS[subdomain]`` value if it exists, otherwise falling back to
the ``ROOT_URLCONF``::

    >>> from subdomains.utils import reverse
    >>> reverse('home', subdomain='api')
    'http://api.example.com/'
    >>> reverse('home', subdomain='wildcard')
    'http://wildcard.example.com/'
    >>> reverse('login', subdomain='wildcard')
    'http://wildcard.example.com/login/'

If a URL cannot be resolved, a :exc:`django.core.urlresolvers.NoReverseMatch`
will be raised.

Resolving Named URLs in Templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``subdomainurls`` template tag library contains a ``url`` tag that takes an
optional ``subdomain`` argument as it's first positional argument, or as named
argument. The following are all valid invocations of the tag::

    {% load subdomainurls %}
    {% url 'home' %}
    {% url 'home' 'subdomain' %}
    {% url 'home' subdomain='subdomain' %}
    {% url 'user-profile' username='ted' %}
    {% url 'user-profile' subdomain='subdomain' username='ted' %}

If ``request`` is in the template context when rendering and no subdomain is
provided, the URL will be attempt to be resolved by relative to the current
subdomain. If no request is available, the URL will be resolved using the same
rules as a call to :func:`subdomains.utils.reverse` without a ``subdomain``
argument value. An easy way to ensure this functionality is available is to
add :func:`django.core.context_processors.request` is in your
``settings.TEMPLATE_CONTEXT_PROCESSORS`` list.

.. note:: For implementation simplicity, this template tag only supports the Django 1.5
   ``{% url %}`` syntax with variable URL names. For more information, please see
   the reference documentation for :func:`~subdomains.templatetags.subdomainurls.url`.

API Reference
-------------

.. toctree::
   :maxdepth: 2
   :glob:

   ref/**

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

