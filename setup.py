#!/usr/bin/env python

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import luks

BASE_DIR = os.path.dirname(__file__)
README_PATH = os.path.join(BASE_DIR, 'README.md')
DESCRIPTION = open(README_PATH).read()

setup(
    name='pyluks',
    version=luks.__version__,
    description='A utility for managing LUKS encrypted containers.',
    long_description=DESCRIPTION,
    author=luks.__author__,
    author_email='cymrow@gmail.com',
    url='https://github.com/dhagrow/pyluks/',
    py_modules=['luks'],
    scripts=['luks.py'],
    license=luks.__license__,
    keywords=['luks', 'container', 'encryption', 'crypto', 'crytography'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Security :: Cryptography',
        'Topic :: System :: Filesystems',
        'Topic :: Utilities',
        ],
    )
