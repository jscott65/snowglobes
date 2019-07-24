#!/usr/bin/env python
import argparse
import os
import numpy as np

from .snowglobes import main, Channel
from .helper import get_abs_path
from .osc import oscillate
from .interp import interpolate
from .plot import plotflux, plot_rate_vs_time

here = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='SNOwGLoBES: public software for computing interaction rates and distributions of observed quantities for supernova burst neutrinos in common detector materials.')
    parser.add_argument('fluxname', type=str, help='Name of flux. \n (eg. livermore)')
    parser.add_argument('channelname', type=str, help='Name of channel. \n (eg. argon)')
    parser.add_argument('experimentname', type=str, help='Name of experiment. \n (eg. ar17kt)')
    parser.add_argument('--weight', action='store_true', help='Apply weighting factor. \n')
    parser.add_argument('--td', action='store_true', help='Use time-dependent fluxes.\n')
    parser.add_argument('--osc', type=int, nargs='?', default=None, choices=[1, -1],
                        const=1, help='Oscillate fluxes. Normal:1, Inverted:-1 Default is NH. (eg. --osc -1)\n')
    parser.add_argument('--interp', metavar='PATH', type=str,
                        help='Interpolate time-dependent fluxes. Pass it the path to raw files. (eg. --interp "/path/to/raw/flux/files/")\n')
    parser.add_argument('--exit', action='store_true',
                        help='Flag to exit after interpolation or oscillation of fluxes.\n')
    parser.add_argument('--clean', action='store_true',
                        help='Flag to remove oscillated and interpolated fluence files.\n')
    parser.add_argument('--plot_flux', action='store_true', help='Plot fluence files.\n')
    parser.add_argument('--plot_rates', action='store_true', help='Plot rate vs times.\n')

    # e.g. python supernova.py livermore argon ar17kt (optional: --weight --td --osc 1)
    args = parser.parse_args()

    fluxname = args.fluxname
    channame = args.channelname
    expt_config = args.experimentname
    weight = args.weight
    td = args.td
    osc = args.osc
    interp = args.interp
    exit = args.exit
    clean = args.clean
    plot_flux = args.plot_flux
    plot_rates = args.plot_rates

    path = get_abs_path('/fluxes/' + fluxname)

    if plot_flux:

        plotflux(fluxname, td)

        raise SystemExit

    if plot_rates:

        chan = Channel(channame)

        plot_rate_vs_time(fluxname, chan.name, expt_config,
                          cumulative=False, log=False, interactive=False)

        raise SystemExit

    if clean:
        # implement some logic to delete all fluxes that are install with snowglobes.
        files = os.listdir(here + '/out')
        for file in files:
            if file.endswith('.dat'):
                os.remove(file)
            elif os.path.isdir(file):
                td_files = os.listdir(here + '/out/' + file)
                for td_file in td_files:
                    os.remove(here + '/out/' + file + '/' + td_file)
                os.rmdir(file)
        print('mister clean')

        raise SystemExit

    if interp:
        print('Interpolating data')
        if not td:
            print('Must provide --td argument and time dependent flux files. Cannot interpolate a single file.')
        raw_flux_path = interp
        interpolate(fluxname, raw_flux_path)
        if exit:
            raise SystemExit

    if osc:
        print('Oscillating data')
        oscillate(fluxname, osc, td)
        if osc == -1:
            fluxname = fluxname + '_inverted'
        elif osc == 1:
            fluxname = fluxname + '_normal'
        if exit:
            raise SystemExit

    if td:
        files = [os.path.splitext(filename)[0] for filename in os.listdir(path)]
        files.sort()
        for flux in files:
            if osc == -1:
                flux = flux + '_inverted'
            elif osc == 1:
                flux = flux + '_normal'
            tdfluxname = fluxname + '/' + flux
            main(tdfluxname, channame, expt_config, weight)
    else:
        main(fluxname, channame, expt_config, weight)
