# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from subprocess import check_output, CalledProcessError

version_file = os.path.join(
    os.path.dirname(__file__),
    'lawnboy', '_version.py'
)

try:
    version = check_output(
        'git describe --tags', shell=True).decode('utf-8').strip()
    with open(version_file, 'w+') as f:
        f.write("version = '%s'\n" % version)
except CalledProcessError:
    # Source tree (no git)
    # Load version from file
    from lawnboy._version import version

setup(
    name='lawnboy',
    version=version,
    author='Anthony Bescond',
    packages=find_packages(),
    license='Apache License 2.0',
    description='Mower movement plan.',
    install_requires=[
        'argparse',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries'
    ],
    entry_points={'console_scripts': ['lawnboy=lawnboy:main']},
)
