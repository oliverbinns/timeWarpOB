from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
	name='timeWarpOB',
	version='1.0.0',
	description='A Dynamic Time Warping implementation',
	long_description=long_description,
	url='https://github.com/oliverbinns/timeWarpOB',
    author='Oliver Binns',
    author_email='coontact@oliverbinns.com',
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3'
    ],
    keywords='time warp algorithm timeseries',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['matplotlib','numpy'],
	)