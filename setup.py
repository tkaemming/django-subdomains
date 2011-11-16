#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = 'django-subdomains',
    version = '1.1.2',
    url = 'http://github.com/tkaemming/django-subdomains/',
    author = 'ted kaemming',
    author_email = 'ted@kaemming.com',
    description = "Subdomain tools for the Django framework, including "
        "subdomain-specific URL routing.",
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    install_requires = ['setuptools'],
    zip_safe = False
)
