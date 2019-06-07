#/usr/bin/python3

import os
import subprocess
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

#os.chdir('./src')

#Set GLB_DIR and SNOWGLOBES global variables for installation

GLB_DIR = subprocess.check_output('globes-config --prefix', shell=True)
GLB_DIR = str(GLB_DIR, 'utf-8')
SNOWGLOBES = here

#print(GLB_DIR)

os.environ["GLB_DIR"]= GLB_DIR
os.environ["SNOWGLOBES"] = SNOWGLOBES

#Make and Make Install the src
#os.system('make')
#os.system('make install')

#os.chdir('..')
#
setup(
    name = 'SNOwGLoBES',
    version = '0.0.1',

    description = ' ',
    long_description = """ """,
    url = ' github  ',

    author = 'Justin Scott',
    license = 'GNU',
    packages = find_packages(),

    setup_requires = [
        "cffi>=1.0.0"
    ],
    
    install_requires = [
        "cffi>=1.0.0"
    ],

    cffi_modules = ["pyglobes_build.py:FFI_BUILDER"]
)
