import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np

from .interp import get_timesteps

here = os.path.dirname(os.path.abspath(__file__))

def get_totals(fluxname, channels, expt_config):

    totals = np.zeros(len(channels))
    for i, channel in enumerate(channels):
        filepath = here + '/out/' + fluxname + '_' + channel + '_' + expt_config + '_events_smeared.dat'

        data = np.genfromtxt(filepath, skip_header=201)
        totals[i] = data[1]
    return(totals)


def plotflux(fluxname, td=False, output_name=False, interactive=False):

    print(f'Plotting {fluxname}.')

    if td:
        path = here + '/fluxes/' + fluxname
        print(path)
        files = os.listdir(path)
        files.sort()

        df = pd.DataFrame(data=np.zeros((501,7)))
        df.columns = ['energy', 'nue', 'numu', 'nutau', 'nuebar', 'numubar', 'nutaubar']

        for i, file in enumerate(files):
            filepath = path + '/' + file
            print(filepath)
            d = np.genfromtxt(filepath)

            df_step = pd.DataFrame(data=d)

            #print(df_step)

            df_step.columns = ['energy', 'nue', 'numu', 'nutau', 'nuebar', 'numubar', 'nutaubar']

            #Sum values from each value into a single dataframe
            df[['nue', 'numu', 'nutau', 'nuebar', 'numubar', 'nutaubar']] = df[['nue', 'numu', 'nutau', 'nuebar', 'numubar', 'nutaubar']] + df_step[['nue', 'numu', 'nutau', 'nuebar', 'numubar', 'nutaubar']]

        #Set energy bin values
        df['energy'] = df_step['energy']


    else:

        path = here + '/fluxes/' + fluxname +'.dat'

        d = np.genfromtxt(path)

        df = pd.DataFrame(data=d)

        df.columns = ['energy', 'nue', 'numu', 'nutau', 'nuebar', 'numubar', 'nutaubar']

    #print(df)

    ax = plt.gca()
    plt.style.use('ggplot')

    #add some logic for osc
    if df['numu'].values[3]==df['nutau'].values[3]:
        if df['numubar'].values[3]==df['nutaubar'].values[3]:
            if df['nue'].values[3]==df['nuebar'].values[3]:
                flavs = ['nu', 'nux', 'nuxbar']
                df['nu'] = df['nue']
                df['nux'] = df['numu']
                df['nuxbar'] = df['numubar']
                labels = [r'$\nu=\nu_{e}=\bar{\nu_{e}}$', r'$\nu_{x}=\nu_{\mu}=\bar{\nu_{\mu}}$', r'$\bar{\nu_{x}}=\bar{\nu_{\mu}}=\bar{\nu_{\tau}}$']
            elif df['numu'].values[3]==df['nutaubar'].values[3]:
                flavs = ['nue', 'nuebar', 'nux']
                df['nux'] = df['numu']
                labels = [r'$\nu_{e}$', r'$\bar{\nu_{e}}$', r'$\nu_{x}=\nu_{\mu}=\bar{\nu_{\mu}}=\nu_{\tau}=\bar{\nu_{\tau}}$']
            else:
                flavs = ['nue', 'nuebar', 'nux', 'nuxbar']
                df['nux'] = df['numu']
                df['nuxbar'] = df['numubar']
                labels = [r'$\nu_{e}$', r'$\bar{\nu_{e}}$', r'$\nu_{x}=\nu_{\mu}=\nu_{\tau}$', r'$\bar{\nu_{x}}=\bar{\nu_{\mu}}=\bar{\nu_{\tau}}$']
    else:
        flavs = ['nue', 'numu', 'nutau', 'nuebar', 'numubar', 'nutaubar']
    #labels = ['nue', 'numu', 'nutau', 'nuebar', 'numubar', 'nutaubar']
        labels = [r'$\nu_{e}$', r'$\bar{\nu_{e}}$', r'$\nu_{\mu}$', r'$\bar{\nu_{\mu}}$', r'$\nu_{\tau}$', r'$\bar{\nu_{\tau}}$']

    for i, flav in enumerate(flavs):

        subplot = df.plot(kind='line',x='energy',y=flav,ax=ax)

    ax.legend(labels)

    ax.set(xlabel='Neutrino Energy (MeV)', ylabel=r'Fluence (neutrinos per 0.2 MeV per $cm^2$)', title='Fluence vs Energy')

    caption = f'{fluxname} fluence.'

    plt.figtext(.02, .02, caption, size='x-small')

    ax.grid()


    #plt.style.use('seaborn-bright')
    #print(plt.style.available)
    if interactive:
        plt.show()

    if output_name:
        if not output_name.endswith('.png'):
            print('Enter .png file')
        else:
            f_out = output_name
    else:
        f_out = fluxname + "_flux_plot.png"

    plt.savefig(f_out)

    print(f'Saved as {f_out}')

    plt.clf()


def plot_rate_vs_time(fluxname, channels, expt_config, cumulative=False, log=False, interactive=False):

    path = here + '/fluxes/' + fluxname

    print(f'Plotting {path}')

    files = [os.path.splitext(filename)[0] for filename in os.listdir(path)]
    files.sort()

    data=np.zeros((len(files),len(channels)))


    for i, file in enumerate(files):
        #fluxname = fluxname + '/' + file

        d = get_totals(fluxname + '/' + file, channels, expt_config)
        data[i] = d

    df = pd.DataFrame(data)

    if cumulative:
        df = df.cumsum()

    df.columns = channels

    timepath = path + '_timesteps.dat'

    overall_time, pb_time = np.genfromtxt(timepath).T

    df.insert(loc=0, column='pb_time', value=pb_time.tolist())

    #print(df)

    ax = plt.gca()
    plt.style.use('ggplot')

    for i, chan in enumerate(channels):

        subplot = df.plot(kind='line',x='pb_time',y=chan,ax=ax)

    ax.legend(channels, loc='upper right')

    ax.set(xlabel='Post Bounce Time (s)', ylabel='Total Events Detected', title='Events vs Time')

    caption = f'{fluxname} events_smeared.'

    plt.figtext(.02, .02, caption, size='x-small')
    if log:
        plt.yscale('log')

    ax.grid()

    if interactive:
        plt.show()

    f_out = fluxname + "_events_vs_time_plot.png"
    plt.savefig(f_out)

    print(f'Saved as {f_out}')
