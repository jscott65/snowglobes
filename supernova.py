#/usr/bin/python3

import argparse
import os
import re
import subprocess
import sys

import numpy as np
from src.snowglobes import supernova, create_AEDL_file, apply_weights

def main(fluxname, channame, expt_config, *weight):

    t = create_AEDL_file(fluxname, channame, expt_config)

    s = supernova(fluxname, channame, expt_config)

    if weight:
        print("Applying channel weighting factors to output")
        apply_weights("", fluxname, channame, expt_config)
        apply_weights("_smeared", fluxname, channame, expt_config)
    else:
        print("No weighting factors applied to output")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'SNOwGLoBES: public software for computing interaction rates and distributions of observed quantities for supernova burst neutrinos in common detector materials.')
    parser.add_argument('fluxname', type=str, help='Name of flux. \n (eg. livermore)')
    parser.add_argument('channelname', type=str, help='Name of channel. \n (eg. argon)')
    parser.add_argument('experimentname', type=str, help='Name of experiment. \n (eg. ar17kt)')
    parser.add_argument('--weight',action='store_true', help='Apply weighting factor. \n')

    # e.g. python supernova.py livermore argon ar17kt
    #if statement for --td declaring class which is obvis diff
    args = parser.parse_args()

    fluxname = args.fluxname
    channame = args.channelname
    expt_config = args.experimentname
    weight = args.weight

    main(fluxname, channame, expt_config, weight)
else:
    print("supernova.py is being imported into another module")
