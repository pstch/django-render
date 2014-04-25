from setuptools import setup, find_packages

import django_render

setup(
    name='django-render',
    version=django_render.__version__,
    description='Render unknown Django model instances based on their content type.',
    author='Peter Baumgartner',
    author_email='pete@lincolnloop.com',
    url='http://github.com/lincolnloop/django-render',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
)
