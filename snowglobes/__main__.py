#!/usr/bin/env python
import argparse
import os
import numpy as np

from .snowglobes import main
from .helper import get_abs_path
from .osc import oscillate

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='SNOwGLoBES: public software for computing interaction rates and distributions of observed quantities for supernova burst neutrinos in common detector materials.')
    parser.add_argument('fluxname', type=str, help='Name of flux. \n (eg. livermore)')
    parser.add_argument('channelname', type=str, help='Name of channel. \n (eg. argon)')
    parser.add_argument('experimentname', type=str, help='Name of experiment. \n (eg. ar17kt)')
    parser.add_argument('--weight', action='store_true', help='Apply weighting factor. \n')
    parser.add_argument('--td', action='store_true', help='Use time-dependent fluxes.\n')
    parser.add_argument('--osc', type=int, nargs='?', default=None, choices=[1, -1], const=1, help='Oscillate fluxes.\n')


    # e.g. python supernova.py livermore argon ar17kt (optional: --weight --td --osc 1)
    args = parser.parse_args()

    fluxname = args.fluxname
    channame = args.channelname
    expt_config = args.experimentname
    weight = args.weight
    td = args.td
    osc = args.osc

    path = get_abs_path('/fluxes/' + fluxname)

    if osc:
        oscillate(fluxname, osc, td)
        if osc == -1:
            fluxname = fluxname + '_inverted'
        elif osc == 1:
            fluxname = fluxname + '_normal'

    if td:
        files = [os.path.splitext(filename)[0] for filename in os.listdir(path)]
        files.sort()
        for flux in files:
            if osc==-1:
                flux = flux + '_inverted'
            elif osc==1:
                flux = flux + '_normal'
            tdfluxname = fluxname + '/' + flux
            main(tdfluxname, channame, expt_config, weight)
    else:
        main(fluxname, channame, expt_config, weight)
