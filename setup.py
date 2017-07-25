#!/usr/bin/python2.7

from setuptools import setup, find_packages

from pyx import __version__

setup(
    name='pyx',
    version=__version__,
    description='Personal Python lib',
    author='lycheng',
    author_email='lycheng997@gmail.com',
    url='https://github.com/lycheng/pyx',
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ]
)
