from django.conf import settings

USE_SUBDOMAIN_EXCEPTION = getattr(settings, 'USE_SUBDOMAIN_EXCEPTION', False)
REMOVE_WWW_FROM_SUBDOMAIN = getattr(settings, 'REMOVE_WWW_FROM_SUBDOMAIN', False)