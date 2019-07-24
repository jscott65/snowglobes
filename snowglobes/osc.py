#!/bin/python3

import numpy as np
import os

#from snowglobes.helper import get_abs_path

#os.makedirs(os.path.dirname(outfile), exist_ok=True)
here = os.path.dirname(os.path.abspath(__file__))
# print(here)


def msw(flux, osc):

    th12 = 0.588366
    s2th12 = pow((np.sin(th12)), 2)
    c2th12 = 1-s2th12

    if osc == 1:
        nue = flux[:, 3]
        numu = (flux[:, 1]+flux[:, 3])/2
        nutau = (flux[:, 1]+flux[:, 3])/2

        nuebar = c2th12*flux[:, 2]+s2th12*flux[:, 3]
        numubar = ((1-c2th12)*flux[:, 2]+(1+c2th12)*flux[:, 4])/2
        nutaubar = ((1-c2th12)*flux[:, 2]+(1+c2th12)*flux[:, 4])/2

    elif osc == -1:
        nue = s2th12*flux[:, 1]+c2th12*flux[:, 3]
        numu = ((1-s2th12)*flux[:, 1]+(1+s2th12)*flux[:, 3])/2
        nutau = ((1-s2th12)*flux[:, 1]+(1+s2th12)*flux[:, 3])/2

        nuebar = flux[:, 4]
        numubar = (flux[:, 2]+flux[:, 4])/2
        nutaubar = (flux[:, 2]+flux[:, 4])/2

    out = np.array([nue, numu, nutau, nuebar, numubar, nutaubar])
    flux[:, 1::] = out.T

    return(flux)


def oscillate(fluxname, osc, td):
    if td:
        path = here + '/fluxes/' + fluxname
        files = [os.path.splitext(filename)[0] for filename in os.listdir(path)]
        files.sort()

        for fluxfile in files:
            fluxfilepath = here + '/fluxes/' + fluxname + '/' + fluxfile + '.dat'
            flux = np.genfromtxt(fluxfilepath, dtype=None, encoding=None)
            flux = msw(flux, osc)
            if osc == 1:
                outfilepath = here + '/fluxes/' + fluxname + '_normal/' + fluxfile + '_normal.dat'
            elif osc == -1:
                outfilepath = here + '/fluxes/' + fluxname + '_inverted/' + fluxfile + '_inverted.dat'
            else:
                print('Error: Invalid value for osc.')
                print('Must be either -1 or 1 for inverted and normal hierachies, repsectively.')

            os.makedirs(os.path.dirname(outfilepath), exist_ok=True)
            np.savetxt(outfilepath, flux, fmt=' '.join(['%1.4f'] + ['%16.6e']*6), delimiter='\t')

    else:
        fluxfilepath = here + '/fluxes/' + fluxname + '.dat'
        # try-except error?? id td flux but no --td flag
        flux = np.genfromtxt(fluxfilepath, dtype=None, encoding=None)
        flux = msw(flux, osc)
        if osc == 1:
            outfilepath = here + '/fluxes/' + fluxname + '_normal.dat'
        elif osc == -1:
            outfilepath = here + '/fluxes/' + fluxname + '_inverted.dat'
        os.makedirs(os.path.dirname(outfilepath), exist_ok=True)
        np.savetxt(outfilepath, flux, fmt=' '.join(['%1.4f'] + ['%16.6e']*6), delimiter='\t')
