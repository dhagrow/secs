#!/usr/bin/env python

import os
from setuptools import setup

import secs

BASE_DIR = os.path.dirname(__file__)
README_PATH = os.path.join(BASE_DIR, 'README.rst')
DESCRIPTION = open(README_PATH).read()

setup(
    name='secs',
    version=secs.__version__,
    description='Simple encrypted containers',
    long_description=DESCRIPTION,
    author=secs.__author__,
    author_email='cymrow@gmail.com',
    url='https://github.com/dhagrow/secs',
    py_modules=['secs'],
    entry_points={'console_scripts': ['secs=secs:main']},
    license=secs.__license__,
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
