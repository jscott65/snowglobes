#!/usr/bin/env python

import argparse


from snowglobes.snowglobes import Channel, Detector, apply_weights, supernova
from snowglobes.aedl import create_AEDL_file


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
