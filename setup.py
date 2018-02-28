from setuptools import setup, find_packages
from codecs import open
from os import path
from zenoss_client import VERSION

here = path.abspath(path.dirname(__file__))


# Get requirements from requirements.txt file
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='python-zenoss-client',
    version=VERSION,
    description='Zenoss API client for python',
    long_description=long_description,
    url='https://github.com/sayanarijit/python-zenoss-client',
    download_url='https://github.com/sayanarijit/python-zenoss-client/archive/{}.tar.gz'.format(VERSION),
    author='Arijit Basu',
    author_email='sayanarijit@gmail.com',
    license='MIT',
    py_modules=['zenoss_client'],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'Operating System :: MacOS',
        'Operating System :: POSIX'
    ],
    keywords='zenoss json api client',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'zenoss-client = zenoss_client:cli',
        ]
    }
)
