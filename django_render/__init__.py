"""
Django render provides a template tag that works similar to an inclusion tag, 
however it will attempt to use a custom template for each model. This is useful 
when iterating over a list of heterogeneous model instances or a queryset with 
generic relationships.

"""
__title__ = 'django-render'
__version__ = '0.1.2'
__author__ = 'Peter Baumgartner, Hugo Geoffroy'
__license__ = 'See LICENSE file'
__copyright__ = """Copyright (c) Lincoln Loop, LLC and individual contributors.
All rights reserved."""
