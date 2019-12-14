"""
Assembly
"""

import os
from setuptools import setup, find_packages

base_dir = os.path.dirname(__file__)


__about__ = {}
with open(os.path.join(base_dir, "assembly", "about.py")) as f:
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
    py_modules=['assembly'],
    entry_points=dict(console_scripts=[
        'asm=assembly.scripts:cmd',
    ]),
    include_package_data=True,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=install_requires,
    keywords=['flask',
              'assembly',
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
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False
)

