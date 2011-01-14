#!/usr/bin/env python
# encoding: utf-8
"""
setup.py
"""

from setuptools import setup, find_packages
import os

execfile(os.path.join('src', 'pyxls', 'version.py'))

setup(
    name = 'pyxls',
    version = VERSION,
    description = 'pyxls makes writing excel spreadsheets suck a little less.',
    author = 'Stephen Altamirano',
    author_email = 'stephen@evilrobotstuff.com',
    url = 'http://www.github.com/alts/pyxls',
    packages = find_packages('src'),
    package_dir = {'':'src'},
    scripts = [],
    classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe = False
)
