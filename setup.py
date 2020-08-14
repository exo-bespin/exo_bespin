#!/usr/bin/env python
import os
from setuptools import setup, find_packages

REQUIRES = ['boto3',
            'numpy',
            'paramiko',
            'platon',
            'scp']

setup(name='exo_bespin',
      version='0.0.0',
      description='',
      packages=find_packages(".", exclude=["*.tests"]),
      install_requires=REQUIRES,
      author='Matthew Bourque, Rachel Cooper, Néstor Espinoza',
      license='BSD 3',
      url='https://github.com/exo-bespin/exo_bespin'
)
