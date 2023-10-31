from django.template import Library
from django.urls.exceptions import NoReverseMatch

from subdomains.tag_helpers import silly_tag
from subdomains.utils import reverse


register = Library()

UNSET = object()


@silly_tag(register, takes_context=True)
def url(context, view, *args, **kwargs):
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
    subdomain = kwargs.pop('subdomain', UNSET)
    if subdomain is UNSET:
        request = context.get('request')
        if request is not None:
            subdomain = getattr(request, 'subdomain', None)
        else:
            subdomain = None
    elif subdomain == '':
        subdomain = None

    scheme = kwargs.pop('scheme', UNSET)
    if scheme is UNSET:
        scheme = None

    asvar = kwargs.pop('_asvar', False)

    try:
        return reverse(view, scheme=scheme, subdomain=subdomain, args=args, kwargs=kwargs)
    except NoReverseMatch:
        if asvar:
            return ''
        else:
            raise
