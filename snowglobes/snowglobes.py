#!/usr/bin/python
import os
import subprocess

import numpy as np
from snowglobes.aedl import create_AEDL_file
from snowglobes.helper import get_abs_path
from snowglobes.supernova import supernova

here = os.path.dirname(os.path.abspath(__file__))


class Channel():

    __slots__ = ('channel', 'chan_file_name', 'name', 'num', 'cp', 'flav', 'factor')

    def __init__(self, channame):
        self.channel = channame
        self.chan_file_name = get_abs_path(f"channels/channels_{self.channel}.dat")
        data = np.genfromtxt(self.chan_file_name, dtype=None, encoding=None)
        self.name = [i[0] for i in data]
        self.num = [i[1] for i in data]
        self.cp = [i[2] for i in data]
        self.flav = [i[3] for i in data]
        self.factor = [i[4] for i in data]


class Detector():

    def __init__(self):

        __slots__ = ('filename', 'config', 'mass', 'norm')

        self.filename = get_abs_path("detector_configurations.dat")

        if not os.path.exists(self.filename):
            print(f"Detector file name {self.filename} not found")

        data = np.genfromtxt(self.filename, dtype=None, encoding=None)
        self.config = [i[0] for i in data]
        self.mass = [i[1] for i in data]
        self.norm = [i[2] for i in data]

    def get_index(self, expt_config):
        return(self.config.index(expt_config))

    def get_target_mass(self, expt_config):
        # Compute the target mass by mult. the mass and normalization factor
        return(self.mass[self.get_index(expt_config)]*self.norm[self.get_index(expt_config)])


def apply_weights(filename, fluxname, chan, expt_config):
    for i, chan_name in enumerate(chan.name):
        unweightedfilename = get_abs_path(
            f"out/{fluxname}_{chan_name}_{expt_config}_events{filename}_unweighted.dat")
        weightedfilename = get_abs_path(
            f"out/{fluxname}_{chan_name}_{expt_config}_events{filename}.dat")
        data = np.genfromtxt(unweightedfilename, comments="--", dtype=float, encoding=None)
        data[:, 1] *= chan.factor[i]
        footer = "-------------------------\nTotal:          {:f}".format(data[-1, 1])
        np.savetxt(weightedfilename, data[:][:-1], fmt=['%1.6f'] +
                   ['%16.6e'], footer=footer, comments='')


def main(fluxname, channame, expt_config, weight=False, use_exe=None):
    # This function defines and runs the experiment.

    # Set the channel.
    chan = Channel(channame)

    # Grab detector attributes.
    det = Detector()

    # Create supernova.glb defining experiment params.
    t = create_AEDL_file(fluxname, chan, det, expt_config)

    # Run the experiment using params in supernova.glb .
    s = supernova(fluxname, chan, expt_config)

    # If set, then we run on the old executable
    if use_exe:

        # Set path/name for executable (pass this as an option in the future)
        exename = f"{here}/bin/supernova"

        # Pass chanfilename to executable
        chanfilename = f"{here}/channels/channels_{channame}.dat"

        # Useful prints for debugging
        print('Running SNOwGLoBES with executable.')
        subprocess.run([exename, fluxname, chanfilename, expt_config],
                       input=None, timeout=None, check=False)
        print('Exiting SNOwGLoBES executable')

    # If --weight is set then weighting factors are applied to event rates
    if weight:
        print("Applying channel weighting factors to output")

        # Apply weighting factors to both smeared and unsmeared event rates
        apply_weights("", fluxname, chan, expt_config)
        apply_weights("_smeared", fluxname, chan, expt_config)

    else:
        print("No weighting factors applied to output")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='SNOwGLoBES: public software for computing interaction rates and distributions of observed quantities for supernova burst neutrinos in common detector materials.')
    parser.add_argument('fluxname', type=str, help='Name of flux. \n (eg. livermore)')
    parser.add_argument('channelname', type=str, help='Name of channel. \n (eg. argon)')
    parser.add_argument('experimentname', type=str, help='Name of experiment. \n (eg. ar17kt)')
    parser.add_argument('--weight', action='store_true', help='Apply weighting factor. \n')

    # e.g. python supernova.py livermore argon ar17kt
    args = parser.parse_args()

    fluxname = args.fluxname
    channame = args.channelname
    expt_config = args.experimentname
    weight = args.weight

    main(fluxname, channame, expt_config, weight)
