import os
import re
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


rootpath = os.path.abspath(os.path.dirname(__file__))
with open('README.rst') as f:
    # use README for long description but don't include the link to travis-ci;
    # it seems a bit out of place on pypi since it applies to the development
    # version
    long_description = ''.join([
        line for line in f.readlines()
        ])


# this sets __version__
def version():
    """Get the version number."""
    with open(os.path.join(rootpath, "VERSION.txt")) as v:
        _version = v.read()
    return _version.strip()


__version__ = version()


def parse_requirement(requirement, excludes):
    lib = requirement.strip().split('#')[0]  # strip new lines and comments
    if lib:
        lib_name = re.split(r'[[<>=! ]+', lib)[0]
        if lib_name in excludes:
            return ''
        return lib.strip()
    return ''


def load_requirements(excludes=None):
    if excludes is None:
      excludes = []
    requirements = []
    with open('requirements.txt') as requirements_file:
        line = requirements_file.readline()
        while line:
            line = line.strip()
            while line.endswith('\\'):
                line += requirements_file.readline().strip()
            line = ' '.join(line.split('\\'))
            requirement = parse_requirement(line, excludes)
            if requirement:
                requirements.append(requirement)
            line = requirements_file.readline()
    return requirements


excludes = ['pytest']
required = load_requirements(excludes)


setup(
    name='ulmo',
    version=__version__,
    license='BSD',
    author='Dharhas Pothina',
    author_email='dharhas@gmail.com',
    description='clean, simple and fast access to public hydrology and climatology data',
    long_description=long_description,
    url='https://github.com/ulmo-dev/ulmo/',
    keywords='his pyhis ulmo water waterml cuahsi wateroneflow usgs ned',
    packages=find_packages(),
    platforms='any',
    install_requires=required,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    tests_require=[
        'mock',
        'freezegun',
        'pytest',
        'httpretty',
        'html5lib<=0.9999999',
    ],
    cmdclass={'test': PyTest},
)
