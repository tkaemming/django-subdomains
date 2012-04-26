from django.core.exceptions import ImproperlyConfigured


class IncorrectSiteException(ImproperlyConfigured):
    """
    Raised when the request domain name does not match the domain name of the
    Site specified in the Django settings file as SITE_ID.
    """
    pass
