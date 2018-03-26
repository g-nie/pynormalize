#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=E0602,W0122

from setuptools import find_packages, setup


with open('README.rst', encoding='utf-8') as readme_file:
    long_description = '\n' + readme_file.read()

requirements = [
    'pydub>=0.21.0',
    'mutagen>=1.40.0'
]

# Get the data from pynormalize/version.py without importing the package
exec(compile(open('pynormalize/version.py').read(), 'version.py', 'exec'))

setup(
    name='pynormalize',
    version=VERSION,
    description='Audio normalization for Python',
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url='https://github.com/giannisterzopoulos/pynormalize',
    packages=find_packages(exclude=("tests", "tests.*")),
    install_requires=requirements,
    license='MIT',
    entry_points={
        'console_scripts': ['pynormalize = pynormalize.pynormalize:main']
    },
    classifiers=[
        STATUS,
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
