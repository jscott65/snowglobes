# SNOwGLoBES: SuperNova Observations w/ GLoBES

Infrastructure for the Analysis of Neutrino Signatures in Core-Collapse Supernovae

## Getting Started

The snowglobes package can be downloaded directly from pip. However, there are several prerequisites.


### Prerequisites

Currently, the GLoBES library must be installed, made, and added to PATH prior to any attempt to install snowglobes.


[GLoBES: General Long Baseline Experiment Simulator](https://www.mpi-hd.mpg.de/personalhomes/globes/download/globes-3.2.17.tar.gz) - Download the source files here

To install the library, you must have gcc and gsl installed. Then follow the steps in the INSTALL file, or as follows:

```
cd to GLOBES source directory
```

```
./configure
```

```
make
```

```
make install
```

We made a library, so don't forget to run:

```
ldconfig
```

If you don't have root access, use

```
./configure --prefix=GLB_DIR
```
 to direct where to save the library.

 Then, the remaining steps are the same as above.
 REMEMBER to set the LD_LIBRARY_PATH environment variable to include GLB_DIR, otherwise the globes lib will not be found at runtime.


### Installing

Now that we have the globes library installed. We can install the snowglobes package.

```
pip install snowglobes
```
or, if you don't have root access

```
pip install --user snowglobes
```

After installation, verify that the directory the package is saved in is on the PATH and PYTHON_PATH by


```
echo $PATH
```

or

```
echo $PYTHON_PATH
```

If it is not on your paths, add it as so

```
export PYTHON_PATH=$PYTHON_PATH:/path/to/snowglobes/
```

and

```
export PATH=$PATH:/path/to/snowglobes/
```

## Running the experiment

There are three different modes of using the snowglobes package.

The first method is the simplest and the main mode of usage.

During installation, the script supernova.py is saved to the python scripts directory.

It can be executed via the command line from any directory.

```
supernova.py livermore lead halo1
```
or
```
supernova.py <fluxname> <channel> <expt_config>
```

The output files are stored in the directory containing the snowglobes package under the out/ directory.

The second method, involves creating a script from the available functions to generate your own AEDL file. Then, using that file to run the supernova function. The previous method automatically creates the AEDL file for you, so you can customize the experiment setup if needed. (i.e. adding/changing oscillation params) These functions can also be accessed to help build scripts for plotting and analysis.

Finally, there will soon be a Jupyter notebook that allows for the selection of data files and output locations.


## Authors

* **Justin Scott**


## License

This project is licensed under the IDK License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* old SNOwGLoBES software
