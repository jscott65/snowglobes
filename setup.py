# /usr/bin/python3

import os
import subprocess
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Set GLB_DIR and SNOWGLOBES global variables for installation

#GLB_DIR = subprocess.check_output('globes-config --prefix', shell=True)
#GLB_DIR = str(GLB_DIR, 'utf-8')
#SNOWGLOBES = here

#os.environ["GLB_DIR"]= GLB_DIR
#os.environ["SNOWGLOBES"] = SNOWGLOBES

setup(
    name='SNOwGLoBES',
    version='2.0.23',

    author='Justin Scott',
    author_email='jscott65@vols.utk.edu',
    url='https://github.com/jscott65/snowglobes',
    license='LICENSE.txt',

    description='SNOwGLoBES: Infrastructure for the Analysis of Neutrino Signatures in Core-Collapse Supernovae',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=["Programming Language :: Python :: 3"],

    #packages = ['supernova'],
    #py_modules = ['aedl', 'globes', 'snowglobes', 'helper', 'supernova'],
    packages=find_packages(),
    #ext_package = 'pyglobes',
    # ADD ENTRY POINT SUPERNOVA:MAIN
    zip_safe=False,
    scripts=['snowglobes/snowglobes.py'],
    entry_points={
        'console_scripts': [
            'supernova = snowglobes.snowglobes:main'
        ],
    },
    include_package_data=True,

    setup_requires=["cffi>=1.0.0"],
    install_requires=["cffi>=1.0.0"],

    cffi_modules=["pyglobes_build.py:FFI_BUILDER"]
)
