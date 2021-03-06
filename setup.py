#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

# FIXME: keep an eye on pip to see if this is eventually
# aliased as an external feature
from pip._internal.req import parse_requirements
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# nice parse_requirements idea taken from freelaw project
requirements = [
    str(r.req) for r in
    parse_requirements('requirements.txt', session=False)
]


setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Joseph Rawson",
    author_email='joseph.rawson.works@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="scrape miss cases from miss college",
    install_requires=requirements,
    license="UNLICENSED",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='mcjudicial',
    name='mcjudicial',
    packages=find_packages(include=['mcjudicial']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/umeboshi2/mcjudicial',
    version='0.1.0',
    zip_safe=False,
)
