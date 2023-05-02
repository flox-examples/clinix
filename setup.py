#!/usr/bin/python

from setuptools import setup, find_packages
import clinix

setup(
    name="clinix",
    version=clinix.__version__,
    description='Clinix Demo Scripts',
    author='flox fan',
    author_email='floxfan@floxdev.com',
    include_package_data=True,
    packages=find_packages(),
    scripts=[ "clinix-demo" ]
)
