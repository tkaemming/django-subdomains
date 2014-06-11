from django.template import Library

from subdomains.compat.template import simple_tag
from subdomains.utils import reverse
from subdomains.utils import UNSET

register = Library()


@simple_tag(register, takes_context=True)
def url(context, view, subdomain=UNSET, *args, **kwargs):
    """
    Resolves a URL in a template, using subdomain-based URL resolution.

    If no subdomain is provided and a ``request`` is in the template context
    when rendering, the URL will be resolved relative to the current request's
    subdomain. If no ``request`` is provided, the URL will be resolved relative
    to current domain with the ``settings.ROOT_URLCONF``.

    Usage::

        {% load subdomainurls %}
        {% url 'view-name' subdomain='subdomain' %}

    .. note:: This tag uses the variable URL syntax introduced in Django
       1.3 as ``{% load url from future %}`` and was made the standard in Django
       1.5. If you are upgrading a legacy application from one of the previous
       template tag formats, make sure to quote your constant string URL names
       to avoid :exc:`~django.core.urlresolver.NoReverseMatch` errors during
       template rendering.

    """
    return reverse(view, subdomain=subdomain, args=args, kwargs=kwargs)
