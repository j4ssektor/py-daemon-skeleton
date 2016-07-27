from setuptools import setup, find_packages
from puppetdiff import __version__


setup(
    name='puppetdiff',
    version=__version__,
    packages=find_packages(),
    author='Nikolai Nozhenko',
    author_email='n.nozhenko@i-free.com',
    license='MIT',
    description='Python daemon skeleton',
    entry_points={
        'console_scripts': [
        'puppetdiff=puppetdiff.puppetdiff:run',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha', # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3.4',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
    ]
)
