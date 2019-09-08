"""
Flasik
"""

import os
from setuptools import setup, find_packages

base_dir = os.path.dirname(__file__)


__about__ = {}
with open(os.path.join(base_dir, "flasik", "__about__.py")) as f:
    exec(f.read(), __about__)

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name=__about__["__title__"],
    version=__about__["__version__"],
    license=__about__["__license__"],
    author=__about__["__author__"],
    author_email=__about__["__email__"],
    description=__about__["__summary__"],
    url=__about__["__uri__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['flasik'],
    entry_points=dict(console_scripts=[
        'flasik=flasik.cli:cmd',
        'flasik-admin=flasik.cli:cmd',
    ]),
    include_package_data=True,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=install_requires,
    keywords=['flask',
              'flasik',
              'templates',
              'views',
              'classy',
              'framework',
              "mvc",
              "blueprint"],
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False
)

