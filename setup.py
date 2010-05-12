#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = 'django-subdomains',
    version = '1.0.0',
    url = 'http://github.com/tkaemming/django-subdomains/',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    install_requires = ['setuptools'],
    zip_safe = False
)