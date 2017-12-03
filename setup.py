from setuptools import setup, find_packages

setup(
    name='lawnboy',
    version='0.1',
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
