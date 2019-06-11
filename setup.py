#/usr/bin/python3

import os
import subprocess
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

#Set GLB_DIR and SNOWGLOBES global variables for installation

GLB_DIR = subprocess.check_output('globes-config --prefix', shell=True)
GLB_DIR = str(GLB_DIR, 'utf-8')
SNOWGLOBES = here

os.environ["GLB_DIR"]= GLB_DIR
os.environ["SNOWGLOBES"] = SNOWGLOBES


setup(
    name = 'SNOwGLoBES',
    version = '2.0.0',

    description = ' ',
    long_description = """ """,
    url = ' github  ',

    author = 'Justin Scott',
    license = 'GNU',
    py_modules = ['supernova', 'src.snowglobes'],
    #packages = find_packages('snowglobes'),

    setup_requires = ["cffi>=1.0.0"],
    install_requires = ["cffi>=1.0.0"],

    cffi_modules = ["pyglobes_build.py:FFI_BUILDER"]
)
