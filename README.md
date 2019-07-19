# SNOwGLoBES: SuperNova Observations w/ GLoBES

Infrastructure for the Analysis of Neutrino Signatures in Core-Collapse Supernovae

## Getting Started

The snowglobes package can be downloaded directly from pip.

## Prerequisites

The GLoBES library is required for snowglobes. This is taken care of by including the globes binary into the wheel binary files. Thus, snowglobes can be installed from Pip and immediately ran with no need for compilation.

### GLoBES
Installing from the source distribution requires that the GLoBES library be installed, made, and added to PATH prior to any attempt to install snowglobes.


[GLoBES: General Long Baseline Experiment Simulator](https://www.mpi-hd.mpg.de/personalhomes/globes/download/globes-3.2.17.tar.gz) - Download the source files here

To install the library, you must have gcc and gsl installed.
Then, follow the steps in the INSTALL file, or as follows:

```
cd to GLOBES source directory
```

```
./configure
make
make install
```

We made a library, so don't forget to run:

```
ldconfig
```

If you don't have root access, use

```
./configure --prefix=GLB_DIR
make
make install
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:GLB_DIR
```
 to direct where to save the library.

 REMEMBER to set LD_LIBRARY_PATH  to include GLB_DIR, otherwise the globes lib will not be found at runtime.

### Other dependencies
* cffi
* numpy

Include these in an anaconda env or a virtenv to pip install into.

## Installing

Typically, there will be a built wheel for your specific system and python version.

Before installing snowglobes via pip, create a virtual environment through anaconda or virtenv. Make sure to include numpy and cffi modules. (You may be able to download without this step, but it typically results in errors.)

We install it as follows:

```
pip install snowglobes
```
or, if you don't have root access

```
pip install --user snowglobes
```

## Running the experiment

There are three different modes of using the snowglobes package. The first method is the simplest and the main mode of usage.

To run an experiment with snowglobes,

```
python -m snowglobes <fluxname> <channel> <expt_config>
```

There are optional arguments that can be added:

```
python -m snowglobes <fluxname> <channel> <expt_config> --td --weight --osc
```
The '--td' command tells snowglobes it's looking for time-dependent fluence files.
The '--weight' command applies weighting factors.
The '--osc' command applies msw oscillations to the fluence files factors. Default is normal hierarchy. (--osc 1 : normal, --osc -1 : inverted)

PAST HERE DOESNT WORK ATM.
During installation, the script supernova.py is saved to the python scripts directory. It can be executed via the command line from any directory.

```
supernova.py <fluxname> <channel> <expt_config> --weight
```
or, as example
```
supernova.py livermore lead halo1
```

By adding the '--weight' command, the weighting factors will be applied to the output files.

The output files are stored in the directory containing the snowglobes package under the out/ directory.

The second method, involves creating a script from the available functions to generate your own AEDL file. Then, using that file to run the supernova function. The previous method automatically creates the AEDL file for you, so you can customize the experiment setup if needed. (i.e. adding/changing oscillation params) These functions can also be accessed to help build scripts for plotting and analysis.

Finally, there will soon be a Jupyter notebook that allows for the selection of data files and output locations.


## Authors

* **Justin Scott**


## License

This project is licensed under the IDK License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* old SNOwGLoBES software
