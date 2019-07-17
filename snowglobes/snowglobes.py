import argparse

import os

import numpy as np

from snowglobes.globes import GLB

from snowglobes.helper import get_abs_path

from snowglobes.aedl import create_AEDL_file


class Channel():

    __slots__ = ('channel', 'chan_file_name', 'name', 'num', 'cp', 'flav', 'factor')

    def __init__(self, channame):
        self.channel = channame
        self.chan_file_name = get_abs_path("channels/channels_{}.dat".format(self.channel))
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
            print("Detector file name {} not found".format(self.filename))

        data = np.genfromtxt(self.filename, dtype=None, encoding=None)
        self.config = [i[0] for i in data]
        self.mass = [i[1] for i in data]
        self.norm = [i[2] for i in data]

    def get_index(self, expt_config):
        return(self.config.index(expt_config))

    def get_target_mass(self, expt_config):
        return(self.mass[self.get_index(expt_config)])


def apply_weights(filename, fluxname, chan, expt_config):
    for i, chan_name in enumerate(chan.name):
        unweightedfilename = "out/{}_{}_{}_events{}_unweighted.dat".format(
            fluxname, chan_name, expt_config, filename)
        weightedfilename = "out/{}_{}_{}_events{}.dat".format(
            fluxname, chan_name, expt_config, filename)
        data = np.genfromtxt(unweightedfilename, comments="--", dtype=float, encoding=None)
        data[:, 1] *= chan.num[i]
        footer = "-----------------\nTotal:   {:f}".format(data[-1, 1])
        np.savetxt(weightedfilename, data[:][:-1], fmt='%f', footer=footer, comments='')


def main(fluxname, channame, expt_config, *weight):

    chan = Channel(channame)

    det = Detector()

    t = create_AEDL_file(fluxname, chan, det, expt_config)

    s = supernova(fluxname, chan, expt_config)

    if weight == True:
        print("Applying channel weighting factors to output")
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

else:
    print("supernova.py is being imported into another module, must create the AEDL file before running supernova()")
