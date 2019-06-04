#/usr/bin/python3

import os
import subprocess
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

os.chdir('./src')

#Set GLB_DIR and SNOWGLOBES global variables for installation

GLB_DIR = subprocess.check_output('globes-config --prefix', shell=True)
SNOWGLOBES = here

os.environ["GLB_DIR"]='/usr/local'
os.environ["SNOWGLOBES"] = SNOWGLOBES

#Make and Make Install the src
os.system('make')
os.system('make install')

os.chdir('..')

setup(
    name = 'SNOwGLoBES',
    version = '0.0.1',

    description = ' ',
    long_description = """ """,
    url = ' github  ',

    author = 'Justin Scott',
    license = 'GNU'

    #setup_requires = [
        #??"cffi>=1.4.0"
    #],
    #install_requires = [
        #??"cffi>=1.4.0"
    #],

    #cffi_modules = ["pyglobes_build.py:FFI_BUILDER"]
)
