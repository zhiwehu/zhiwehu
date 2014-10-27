# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import zhiwehu
version = zhiwehu.__version__

setup(
    name='zhiwehu',
    version=version,
    author='',
    author_email='zhiwehu@gmail.com',
    packages=[
        'zhiwehu',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.6.5',
    ],
    zip_safe=False,
    scripts=['zhiwehu/manage.py'],
)