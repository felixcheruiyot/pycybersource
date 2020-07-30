#!/usr/bin/env python
from distutils.core import setup
import cybersource

LONG_DESCRIPTION = open('README.md').read()

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

KEYWORDS = 'cybersource soap suds wrapper'

setup(name='python3-cybersource',
      version=cybersource.VERSION,
      description='Cyber Source API wrapper for Python3.',
      long_description=LONG_DESCRIPTION,
      author='Felix Cheruiyot',
      author_email='felix@intasend.com',
      url='https://github.com/felixcheruiyot/pycybersource/',
      download_url='http://pypi.python.org/pypi/python3-cybersource/',
      packages=['cybersource'],
      package_dir={'cybersource': 'cybersource'},
      platforms=['Platform Independent'],
      license='BSD',
      classifiers=CLASSIFIERS,
      keywords=KEYWORDS,
      requires=['client', "suds-py3"],
      install_requires=['client', "suds-py3"],
      )
