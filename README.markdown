# django-subdomains

## Installation

1. Add `subdomains.middleware.SubdomainURLRoutingMiddleware` to your
`MIDDLEWARE_CLASSES` in your Django settings file.
2. Set up your `SUBDOMAIN_URLCONFS` dictionary in your Django settings file.
(See the example below.)
3. Make sure that you've set up your `SITE_ID` in your Django settings file, 
and that the `domain` attribute corresponds to the proper domain name.
4. ???
5. Profit!

## Example Configuration

    # This is the URL that will be loaded for any subdomain that is not listed
    # in SUBDOMAIN_URLCONFS. If you're going use wildcard subdomains, this will
    # correspond to the wildcarded subdomain. 
    # For example, 'accountname.mysite.com' will load the ROOT_URLCONF, since 
    # it is not defined in SUBDOMAIN_URLCONFS.
    ROOT_URLCONF = 'myproject.urls.account'
    
    SUBDOMAIN_URLCONFS = {
        # The format for these is 'subdomain': 'urlconf'
        None: 'myproject.urls.frontend',
        'www': 'myproject.urls.frontend',
        'api': 'myproject.urls.api',
    }

## Usage Notes

The subdomain is also added to the request, so you can change view logic, 
depending on it's value, like so:

    def user_profile(request):
        try:
            # Retrieve the user account associated with the current subdomain.
            user = User.objects.get(username=request.subdomain)
        except User.DoesNotExist:
            # No user matches the current subdomain, so return a generic 404.
            raise Http404

### Adding Functionality

You can also subclass `SubdomainURLRoutingMiddleware` if you'd like, to 
associate requests with user accounts based on subdomain, etc.