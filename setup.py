from __future__ import with_statement
from os.path import dirname, join
from setuptools import setup, find_packages
from sys import version_info

__version__ = '0.2.1'

def read(name, *args):
    try:
        with open(join(dirname(__file__), name)) as read_obj:
            return read_obj.read(*args)
    except Exception:
        return ''

extra_setup = {}

test_requirements = ['nose']
if version_info < (2, 7):
    test_requirements.append('unittest2')

setup(
    name='logging_unterpolation',
    version=__version__,
    description='patch logging module to accept PEP-3101 formatting syntax',
    long_description=read('README.md'),
    author='Rob Dennis',
    author_email='rdennis+unterpolation@gmail.com',
    tests_require=test_requirements,
    test_suite='nose.collector',
    url='https://github.com/robdennis/logging_unterpolation',
    packages=find_packages(exclude=['ez_setup']),
    classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.0',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Operating System :: OS Independent',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: System :: Logging',
    'Development Status :: 5 - Production/Stable'],
    **extra_setup
)
