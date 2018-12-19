#!/usr/bin/env python

from os import path

dir_setup = path.dirname(path.realpath(__file__))
requires = [];

from setuptools import setup, Command

modules = [
      'quantpy.sympy'
    , 'quantpy.sympy.executor'
    , 'quantpy.sympy.executor.simulator'
    , 'quantpy.ising'
]

tests = [
]

long_description = '''QuantPy is a Python library for quantum computing. It aims
to become basic library set of quantum computer system.'''

with open(path.join(dir_setup, 'quantpy', 'release.py')) as f:
    # Defines __version__
    exec(f.read())

def _requirements():
    return [name.rstrip() for name in open(path.join(dir_setup, 'requirements.txt')).readlines()]

def _test_requirements():
    return [name.rstrip() for name in open(path.join(dir_setup, 'test-requirements.txt')).readlines()]

if __name__ == '__main__':
    setup(name='quantpy',
          version=__version__,
          description='Quantum Computer system in Python',
          long_description=long_description,
          author='QuantPy development team',
          author_email='quantpy@openql.org',
          license='BSD-3-Clause',
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
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3.6',
          ],
          python_requires=">=3.5",
          install_requires=_requirements(),
          tests_require=_test_requirements(),
          setup_requires=['pytest-runner']
          )
