#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from __future__ import absolute_import
from setuptools import find_packages
from setuptools import setup


test_requirements = [
    'pytest',
]

setup(
    # metadata see setup.cfg
    packages=find_packages(include=['plonectl']),
    entry_points={
        'console_scripts': [
            'plonectl=plonectl.cli:cli',
        ],
    },
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Click>=7.0',
    ],
    extras_require={
        'test': test_requirements,
        'dev': [
            'tox',
            'zest.releaser[recommended]',
        ],
    },
    zip_safe=False,
    keywords='plonectl',
    scripts=['plonectl_autocomplete.sh'],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=['pytest-runner'],
)
