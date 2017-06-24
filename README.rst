**Edit** Updated to work with django 1.10 and so on... using this https://docs.djangoproject.com/en/1.11/topics/http/middleware/#upgrading-middleware
**Edit2** Uploaded it to pypi: under *"subdomains"*
    pip install subdomains

I'd recommend for django versions<=1.9 use django-subdomains from op, otherwise for django 1.10, 1.11 etc use my *subdomains* version

django-subdomains
=================

Subdomain helpers for the Django framework, including subdomain-based URL
routing and reversing.

Full documentation can be found here: http://django-subdomains.readthedocs.org/

Build Status
------------

.. image:: https://secure.travis-ci.org/tkaemming/django-subdomains.png?branch=master
   :target: http://travis-ci.org/tkaemming/django-subdomains

Tested on Python 2.6, 2.7, 3.4 and 3.5 on their supported Django versions from
1.4 through 1.9.
