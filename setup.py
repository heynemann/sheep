#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from sheep import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'factory_boy',
]

setup(
    name='sheep',
    version=__version__,
    description='Sheep is a console worker generator.',
    long_description='''
Sheep is a console worker generator.
''',
    keywords='worker console',
    author='Bernardo Heynemann',
    author_email='heynemann@gmail.com',
    url='https://github.com/heynemann/sheep',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'derpconf',
        'colorama',
        'psutil',
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
