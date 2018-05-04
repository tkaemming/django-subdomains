**Edit** Updated to work with django 1.10 and so on... using this <https://docs.djangoproject.com/en/1.11/topics/http/middleware/#upgrading-middleware> **Edit2** Uploaded it to pypi: under _"subdomains"_ pip install subdomains

I'd recommend for django versions<=1.9 use django-subdomains from op, otherwise for django 1.10, 1.11 etc use my _subdomains_ version

# subdomains

Subdomain helpers for the Django framework, including subdomain-based URL routing and reversing.

Full documentation can be found here: [subdomains](<http://subdomains.readthedocs.org/>)

## Build Status
[![Build Status](https://travis-ci.org/abe312/django-subdomains.svg?branch=master)](https://travis-ci.org/abe312/django-subdomains)

Tested on Python 2.6, 2.7, 3.4, 3.5 and 3.6 on their supported Django versions from 1.4 through 1.11.

Check the following table for reference:

Django version | Python versions
-------------- | -----------------------------------------------
1.8            | 2.7, 3.2 (until the end of 2016), 3.3, 3.4, 3.5
1.9            | 1.10 2.7, 3.4, 3.5
1.11           | 2.7, 3.4, 3.5, 3.6
2.0            | 3.4, 3.5, 3.6
2.1            | 3.5, 3.6, 3.7
