import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from subdomains import __version__

import django
from django.conf import settings

if not settings.configured:
    settings.configure()


extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']

project = u'django-subdomains'
copyright = u'2012, ted kaemming'
version = release = '.'.join(map(str, __version__))

html_static_path = ['_static']
htmlhelp_basename = 'django-subdomainsdoc'

latex_elements = {}
latex_documents = [
  ('index', 'django-subdomains.tex', u'django-subdomains Documentation',
   u'ted kaemming', 'manual'),
]

man_pages = [
    ('index', 'django-subdomains', u'django-subdomains Documentation',
     [u'ted kaemming'], 1)
]

texinfo_documents = [
  ('index', 'django-subdomains', u'django-subdomains Documentation',
   u'ted kaemming', 'django-subdomains', 'One line description of project.',
   'Miscellaneous'),
]

intersphinx_mapping = {
    'python': ('http://docs.python.org/release/%s.%s' % sys.version_info[:2], None),
    'django': ('http://docs.djangoproject.com/en/%s.%s/' % django.VERSION[:2],
        'http://docs.djangoproject.com/en/%s.%s/_objects/' % django.VERSION[:2]),
}

autodoc_member_order = 'bysource'
autodoc_default_flags = ('members',)
