from django.template import Library

from subdomains.utils import reverse


register = Library()

@register.simple_tag
def url(view, subdomain=None, scheme=None, *args, **kwargs):
    return reverse(view, subdomain=subdomain, scheme=scheme, *args, **kwargs)
