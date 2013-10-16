#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from setuptools import setup, find_packages
from faitout import __version__

setup(
    name="faitout",
    version=__version__,
    description="A service to generate on-the-fly temporary "
                "PostgreSQL databases",
    long_description=open('README.rst').read(),
    author='Fedora Infrastructure',
    author_email='infrastructure@lists.fedoraproject.org',
    url="https://github.com/fedora-infra/faitout",
    license="GPLv3",
    classifiers=[
        "Topic :: Database",
        "Framework :: Flask",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 2",
        ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=open("requirements.txt").read().splitlines(),
    )

