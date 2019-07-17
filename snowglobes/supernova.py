#!/usr/bin/env python
import os

from pyglobes._pyglobes import ffi, lib

from snowglobes.globes import GLB

from snowglobes.helper import get_abs_path

def supernova(fluxname, chan, expt_config):

    glb = GLB()

    channel_file_name = chan.chan_file_name

    if os.path.exists(channel_file_name):
        print("Channels from {}".format(channel_file_name))
        print("Number of channels found: {}".format(len(chan.name)))

    else:
        print("Cannot open channel file")

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
