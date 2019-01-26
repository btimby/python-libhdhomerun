#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from distutils.core import setup

setup(
    name='libhdhomerun',
    version='0.2.2',
    description='Bindings to libhdhomerun',
    long_description='Bindings to the libhdhomerun shared library',
    author='Gary Buhrmaster',
    author_email='gary.buhrmaster@gmail.com',
    packages=['libhdhomerun'],
    url='https://github.com/garybuhrmaster/python-libhdhomerun',
    license="Apache License 2.0",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Topic :: Software Development :: Libraries'
    ],
)
