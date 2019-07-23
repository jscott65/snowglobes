import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np

here = os.path.dirname(os.path.abspath(__file__))

def get_totals(fluxname, chan, expt_config):

    totals = np.zeros(len(chan.name))
    for i, channel in enumerate(chan.name):
        filepath = here + '/out/' + fluxname + '_' + channel + '_' + expt_config + '_events_smeared.dat'

        data = np.genfromtxt(filepath, skip_header=201)
        totals[i] = data[1]
    return(totals)


def plotflux(fluxname, td=False, output_name=False, interactive=False):

    print(f'Plotting {fluxname}.')

    if td:
        path = here + '/fluxes/' + fluxname

        files = os.listdir(path)
        files.sort()

        df = pd.DataFrame(data=np.zeros((501,7)))
        df.columns = ['energy', 'nue', 'numu', 'nutau', 'nuebar', 'numubar', 'nutaubar']

        for i, file in enumerate(files):
            filepath = path + '/' + file

            d = np.genfromtxt(filepath)

            df_step = pd.DataFrame(data=d)

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

    ax = plt.gca()
    plt.style.use('ggplot')

    #add some logic for osc
    if df['numu'].values[3]==df['nutau'].values[3]:
        if df['numubar'].values[3]==df['nutaubar'].values[3]:
            if df['nue'].values[3]==df['nuebar'].values[3]:
                flavs = ['nu', 'nux', 'nuxbar']
                df['nu'] = df['nue'] * 2
                df['nux'] = df['numu'] * 2
                df['nuxbar'] = df['numubar'] * 2
                labels = [r'$\nu=\nu_{e}+\bar{\nu_{e}}$', r'$\nu_{x}=\nu_{\mu}+\bar{\nu_{\mu}}$', r'$\bar{\nu_{x}}=\bar{\nu_{\mu}}+\bar{\nu_{\tau}}$']
            elif df['numu'].values[3]==df['nutaubar'].values[3]:
                flavs = ['nue', 'nuebar', 'nux']
                df['nux'] = df['numu'] * 4
                labels = [r'$\nu_{e}$', r'$\bar{\nu_{e}}$', r'$\nu_{x}=\nu_{\mu}+\bar{\nu_{\mu}}+\nu_{\tau}+\bar{\nu_{\tau}}$']
            else:
                flavs = ['nue', 'nuebar', 'nux', 'nuxbar']
                df['nux'] = df['numu'] * 2
                df['nuxbar'] = df['numubar'] * 2
                labels = [r'$\nu_{e}$', r'$\bar{\nu_{e}}$', r'$\nu_{x}=\nu_{\mu}+\nu_{\tau}$', r'$\bar{\nu_{x}}=\bar{\nu_{\mu}}+\bar{\nu_{\tau}}$']
    else:
        flavs = ['nue', 'numu', 'nutau', 'nuebar', 'numubar', 'nutaubar']
        labels = [r'$\nu_{e}$', r'$\bar{\nu_{e}}$', r'$\nu_{\mu}$', r'$\bar{\nu_{\mu}}$', r'$\nu_{\tau}$', r'$\bar{\nu_{\tau}}$']

    for i, flav in enumerate(flavs):

        subplot = df.plot(kind='line',x='energy',y=flav,ax=ax)

    ax.legend(labels)

    ax.set(xlabel='Neutrino Energy (MeV)', ylabel=r'Fluence (neutrinos per 0.2 MeV per $cm^2$)', title='Fluence vs Energy')
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


def plot_rate_vs_time(fluxname, chan):

    path = here + '/fluxes/' + fluxname

    files = [os.path.splitext(filename)[0] for filename in os.listdir(path)]
    files.sort()

    df_tot = pd.DataFrame(data=np.zeros((len(files),len(chan.name)+1)))
    df_tot.columns = ['pb_time'] + chan.name

    for i, file in enumerate(files):
        #fluxname = fluxname + '/' + file

        d = get_totals(fluxname + '/' + file, chan, expt_config)

        df = pd.DataFrame(data=d)

        df = df.T

        df.columns = chan.name

        df

        #Sum values from each value into a single dataframe
        df_tot.at[i, chan.name] =  df