from setuptools import setup, find_packages
from pyskeleton import __version__


setup(
    name='pyskeleton',
    version=__version__,
    packages=find_packages(),
    author='Nikolai Nozhenko',
    author_email='j4ssektor@gmail.com',
    license='MIT',
    description='Python daemon skeleton',
    entry_points={
        'console_scripts': [
        'py-daemon-skeleton=skeleton.skeleton:run',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha', # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 2.7',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
    ]
)
