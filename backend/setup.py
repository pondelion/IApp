from distutils.core import setup
from setuptools import setup, find_packages


# with open('requirements.txt') as requirements_file:
#     install_requirements = requirements_file.read().splitlines()


setup(
  name         = 'iapp',
  description  = 'iapp',
  url          = 'https://github.com/pondelion/IApp',
  packages     = ['iapp'],
  # install_requires = install_requirements,
)
