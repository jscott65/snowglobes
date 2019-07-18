#!/bin/python3

import numpy as np


def oscillate(flux, th12, osc, path):
    s2th12   = pow((np.sin(th12)),2)
    c2th12   = 1-s2th12

    if osc==1:
        nue = flux[:,3]
        numu = (flux[:,1]+flux[:,3])/2
        nutau = (flux[:,1]+flux[:,3])/2

        nuebar = c2th12*flux[:,2]+s2th12*flux[:,3]
        numubar = ((1-c2th12)*flux[:,2]+(1+c2th12)*flux[:,4])/2
        nutaubar = ((1-c2th12)*flux[:,2]+(1+c2th12)*flux[:,4])/2

        path = path[1:-4] + '_normal.dat'

    elif osc==-1:
        nue = s2th12*flux[:,1]+c2th12*flux[:,3]
        numu = ((1-s2th12)*flux[:,1]+(1+s2th12)*flux[:,3])/2
        nutau = ((1-s2th12)*flux[:,1]+(1+s2th12)*flux[:,3])/2

        nuebar = flux[:,4]
        numubar = (flux[:,2]+flux[:,4])/2
        nutaubar = (flux[:,2]+flux[:,4])/2

        path = path[1:-4] + '_inverted.dat'

    out = np.array([nue, numu, nutau, nuebar, numubar, nutaubar])
    flux[:,1::] = out.T
    #with open('/'+path, mode='w+') as f_out:
    #    f_out.write(flux)
    np.savetxt('/' + path, flux, fmt='%16.6e', delimiter='\t')
    #return(out)
