import io
import os
from setuptools import find_packages, setup


requires = [
    'pydub>=0.21.0',
    'mutagen>=1.40.0'
]

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


setup(
    name='pynormalize',
    version='0.1.3',
    description='Audio normalization for Python',
    long_description=long_description,
    author='Giannis Terzopoulos',
    author_email='terzo.giannis@gmail.com',
    url='https://github.com/giannisterzopoulos/pynormalize',
    packages=find_packages(exclude=("tests", "tests.*")),
    install_requires=requires,
    license='MIT',
    entry_points={
        'console_scripts': ['pynormalize = pynormalize.pynormalize:run']
    },
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
