#!/usr/bin/env python

from os import path

dir_setup = path.dirname(path.realpath(__file__))
requires = [];

from setuptools import setup, Command

modules = [
    ]

tests = [
    ]

long_description = '''QuantPy is a Python library for quantum computing. It aims
to become basic library set of quantum computer system.'''

with open(path.join(dir_setup, 'quantpy', 'release.py')) as f:
    # Defines __version__
    exec(f.read())


if __name__ == '__main__':
    setup(name='quantpy',
        version=__version__,
        description='Quantum Computer system in Python',
        long_description=long_description,
        author='QuantPy development team',
        author_email='quantpy@openql.org',
        license='BSD',
        keywords="Math Physics",
        url='http://quantpy.org',
        packages=['quantpy'] + modules + tests,
        ext_modules=[],
        classifiers=[
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Mathematics',
            'Topic :: Scientific/Engineering :: Physics',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            ],
        install_requires=requires,
        )
