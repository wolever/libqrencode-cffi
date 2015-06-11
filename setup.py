#!/usr/bin/env python

import os
import sys

from setuptools import setup, find_packages

os.chdir(os.path.dirname(sys.argv[0]) or ".")

setup(
    name="libqrencode",
    version="0.1",
    description="Fast, robust, and less incomplete cffi-based bindings for libqrencode",
    long_description=open("README.rst", "rt").read(),
    url="https://github.com/wolever/libqrencode",
    author="David Wolever",
    author_email="david@wolever.net",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: PyPy",
        "License :: OSI Approved :: BSD License",
    ],
    packages=find_packages(),
    install_requires=["cffi>=1.0.0"],
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["./libqrencode/ffi_build.py:ffi"],
)
