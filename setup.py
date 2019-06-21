#/usr/bin/python3

import os
import subprocess
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

#Set GLB_DIR and SNOWGLOBES global variables for installation

#GLB_DIR = subprocess.check_output('globes-config --prefix', shell=True)
#GLB_DIR = str(GLB_DIR, 'utf-8')
#SNOWGLOBES = here

#os.environ["GLB_DIR"]= GLB_DIR
#os.environ["SNOWGLOBES"] = SNOWGLOBES


setup(
    name = 'SNOwGLoBES',
    version = '2.0.13',

    author = 'Justin Scott',
    author_email = 'jscott65@vols.utk.edu',
    url = 'https://github.com/jscott65/snowglobes',
    license = 'LICENSE.txt',

    description = 'SNOwGLoBES: Infrastructure for the Analysis of Neutrino Signatures in Core-Collapse Supernovae',
    long_description = open('README.txt').read(),
    classifiers=["Programming Language :: Python :: 3"],

    #packages = ['supernova'],
    py_modules = ['snowglobes.snowglobes', 'pyglobes', 'pyglobes_build'],
    #packages = find_packages('snowglobes'),
    #ext_package = 'pyglobes',

    scripts = ['supernova.py'],

    include_package_data = True,

    setup_requires = ["cffi>=1.0.0"],
    install_requires = ["cffi>=1.0.0"],

    cffi_modules = ["pyglobes_build.py:FFI_BUILDER"]
)
