#!/usr/bin/env python
from setuptools import setup

setup(
    name='python-localcoinswap',
    version='0.0.1',
    packages=['localcoinswap'],
    description='LocalCoinSwap REST API Client in Python',
    url='https://github.com/LocalCoinSwap/python-localcoinswap',
    author='LocalCoinSwap',
    license='MIT',
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
