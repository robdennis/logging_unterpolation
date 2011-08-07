from os.path import dirname, join
from setuptools import setup

__version__ = '0.0.1dev'

def read(name, *args):
    try:
        with open(join(dirname(__file__), name)) as read_obj:
            return read_obj.read(*args)
    except Exception:
        return ''

setup(
    name='logging_unterpolator',
    version=__version__,
    description='patch logging module to accept PEP-3101 formatting syntax',
    long_description=read('README.rst'),
    author='Rob Dennis',
    author_email='rdennis+unterpolation@gmail.com',
    url='http://arclite-emp.com/',
    classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.0',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.2',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Operating System :: Microsoft :: Windows',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: System :: Logging',
    'Development Status :: 1 - Planning'])
