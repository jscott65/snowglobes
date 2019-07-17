#!/usr/bin/env python
import argparse

from .snowglobes import main

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
