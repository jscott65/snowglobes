#!/bin/python3

import numpy as np
import os

here = os.path.dirname(os.path.abspath(__file__))


def get_timesteps(fluxname, path, copy):

    files = [os.path.splitext(filename)[0] for filename in os.listdir(path)]
    files.sort()

    time_path = here + '/fluxes/' + fluxname + '_timesteps.dat'
    os.makedirs(os.path.dirname(time_path), exist_ok=True)
    with open(time_path, 'w+') as f_out:
        for flux in files:
            filename = flux + '.dat'
            fluxfilepath = path + '/' + filename
            with open(fluxfilepath, 'r') as f_in:
                for line in f_in:
                    if line.startswith('#'):
                        pass
                    else:
                        f_out.write(line)
                        break
    if copy:
        data = np.genfromtxt(time_path).T
        return(data)


def interpolate(fluxname, path):

    files = [os.path.splitext(filename)[0] for filename in os.listdir(path)]
    files.sort()

    #Read in timesteps
    overall_time, pb_time = get_timesteps(fluxname, path, copy=True)

    # 10 kpc in cm
    R = 3.086*10**22
    # distance modulus
    factor = 1/(4*np.pi*pow(R, 2))

    for i, flux in enumerate(files):
        filename = flux + '.dat'
        fluxfilepath = path + filename
        outfilepath = here + '/fluxes/' + fluxname + '/' + filename

        print(f'Interpolating {filename}')
        print(f'\tinput: {fluxfilepath}')
        print(f'\toutput: {outfilepath}')

        data = np.genfromtxt(fluxfilepath, skip_header=12, max_rows=20, dtype=None, encoding=None)

        energy, nue, nuebar, nux, nuxbar = np.abs(data.T)

        # Convert energy to GeV
        energy *= 0.001

        bins, nue_fluence, nuebar_fluence, nux_fluence, nuxbar_fluence = np.zeros([
                                                                                  501, 5], dtype=float).T

        # Propogate the energy bins
        bins = np.arange(0, .1002, 0.0002)

        # Extrapolate the fluxes for below the first energy
        f = 0
        while bins[f] <= energy[0]:
            alpha = np.abs(1/(1+(energy[0]-bins[f])/(bins[f]-0.0001)))
            nue_fluence[f] = np.exp(alpha * np.log(nue[0]))
            nuebar_fluence[f] = np.exp(alpha * np.log(nuebar[0]))
            nux_fluence[f] = np.exp(alpha * np.log(nux[0]))
            nuxbar_fluence[f] = np.exp(alpha * np.log(nuxbar[0]))
            f += 1

        # Populate the rest of the fluxes
        for p in range(0, 19):
            while f < 501:
                if bins[f] <= energy[p+1]:
                    alpha = np.abs(1/(1+(energy[p+1]-bins[f])/(bins[f]-energy[p])))
                    nue_fluence[f] = np.exp(alpha * np.log(nue[p+1]) + (1-alpha) * np.log(nue[p]))
                    nuebar_fluence[f] = np.exp(
                        alpha * np.log(nuebar[p+1]) + (1-alpha) * np.log(nuebar[p]))
                    nux_fluence[f] = np.exp(alpha * np.log(nux[p+1]) + (1-alpha) * np.log(nux[p]))
                    nuxbar_fluence[f] = np.exp(
                        alpha * np.log(nuxbar[p+1]) + (1-alpha) * np.log(nuxbar[p]))
                    f += 1
                elif bins[f] > energy[p+1]:
                    p += 1
                # print(f)
        # Convert the fluxes into fluences by multiplying by dt
        if i == 0 or i == 1:
            nue_fluence = nue_fluence * factor * (pb_time[1] - pb_time[0])
            nuebar_fluence = nuebar_fluence * factor * (pb_time[1] - pb_time[0])
            nux_fluence = nux_fluence * factor * (pb_time[1] - pb_time[0])
            nuxbar_fluence = nuxbar_fluence * factor * (pb_time[1] - pb_time[0])
        else:
            nue_fluence = nue_fluence * factor * (pb_time[i] - pb_time[i-1])
            nuebar_fluence = nuebar_fluence * factor * (pb_time[i] - pb_time[i-1])
            nux_fluence = nux_fluence * factor * (pb_time[i] - pb_time[i-1])
            nuxbar_fluence = nuxbar_fluence * factor * (pb_time[i] - pb_time[i-1])

        # Prepare data for output

        output = np.array([bins, nue_fluence, nux_fluence, nux_fluence,
                           nuebar_fluence, nuxbar_fluence, nuxbar_fluence]).T

        os.makedirs(os.path.dirname(outfilepath), exist_ok=True)
        np.savetxt(outfilepath, output, fmt=' '.join(['%1.4f'] + ['%16.6e']*6), delimiter='\t')
