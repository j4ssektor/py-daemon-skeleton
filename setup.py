from setuptools import setup, find_packages
from skeleton import __version__


setup(
    name='py-daemon-skeleton',
    version=__version__,
    packages=find_packages(),
    author='Nikolai Nozhenko',
    author_email='j4ssektor@gmail.com',
    license='MIT',
    description='Python daemon skeleton',
    scripts=['bin/py-daemon-skeleton',],
    data_files=[('/etc/init.d', ['etc/init/py-daemon-skeleton']),
                ('/etc/py-daemon-skeleton', ['etc/skeleton.yaml',
                                             'etc/logging.conf',]),],
    classifiers=[
        'Development Status :: 3 - Alpha', # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 2.7',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
    ]
)
