import os

import numpy as np
from pyglobes._pyglobes import ffi, lib

from snowglobes.globes import GLB

from snowglobes.helper import get_abs_path


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


def supernova(fluxname, chan, expt_config):

    glb = GLB()

    channel_file_name = chan.chan_file_name

    if os.path.exists(channel_file_name):
        print("Channels from {}".format(channel_file_name))
        print("Number of channels found: {}".format(len(chan.name)))

    else:
        print("Cannot open file")

    true_values = glb.AllocParams()
    test_values = glb.AllocParams()

    theta12 = 0
    theta13 = 0
    theta23 = 0
    deltacp = 0
    sdm = 0
    ldm = 0

    glb.DefineParams(true_values, theta12, theta13, theta23, deltacp, sdm, ldm)
    glb.SetDensityParams(true_values, 1.0, lib.GLB_ALL)
    glb.DefineParams(test_values, theta12, theta13, theta23, deltacp, sdm, ldm)
    glb.SetDensityParams(test_values, 1.0, lib.GLB_ALL)

    glb.SetOscillationParams(true_values)
    glb.SetRates()

    glb.PrintChannelRates(fluxname, chan, expt_config)

    bgfile = get_abs_path('backgrounds/bg_chan_{}.dat'.format(expt_config))

    if os.path.exists(bgfile):
        bg_file = True
        glb.PrintChannelRates(fluxname, chan, expt_config, bg_file)
    else:
        print("No background file")

    glb.FreeParams(true_values)
    glb.FreeParams(test_values)

    return(0)


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
