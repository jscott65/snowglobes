#!/bin/python3

import sys
import os
import numpy as np
import re
import subprocess

from pyglobes._pyglobes import ffi, lib

def supernova(flux_file_name, channame, expt_config_name):

    channel_file_name = "channels/channels_{}.dat".format(channame)
    print("Channels from {}".format(channel_file_name))

    if not os.path.exists(channel_file_name):
        print("Cannot open file")

    chans = np.genfromtxt(channel_file_name, dtype=None, encoding=None)
    chan_name = [i[0] for i in chans]
    chan_num = [i[1] for i in chans]
    cp = [i[2] for i in chans]
    flav = [i[3] for i in chans]
    num_target_factor = [i[4] for i in chans]

    print("Number of channels found: {}".format(len(chan_num)))

    arg = ffi.new("char[]", b"snowglobes.py")

    lib.glbInit(arg)
    lib.PInit(b"supernova.glb")

    true_values = lib.glbAllocParams()
    test_values = lib.glbAllocParams()

    theta12 = 0
    theta13 = 0
    theta23 = 0
    deltacp = 0
    sdm = 0
    ldm = 0

    lib.glbDefineParams(true_values, theta12, theta13, theta23, deltacp, sdm, ldm)
    lib.glbSetDensityParams(true_values, 1.0, lib.GLB_ALL)
    lib.glbDefineParams(test_values, theta12, theta13, theta23, deltacp, sdm, ldm)
    lib.glbSetDensityParams(test_values, 1.0, lib.GLB_ALL)

    lib.glbSetOscillationParameters(true_values)
    lib.glbSetRates()


    for i, chan in enumerate(chan_name):

        outfile = "out/{}_{}_{}_events_unweighted.dat".format(flux_file_name, chan, expt_config_name)
        print(i, outfile)
        with open(outfile, 'w+') as f_out:
            ret = lib.glbShowChannelRates(f_out, 0, chan_num[i], lib.GLB_PRE, lib.GLB_WO_EFF, lib.GLB_WO_BG)

        outfile_smeared = "out/{}_{}_{}_events_smeared_unweighted.dat".format(flux_file_name, chan, expt_config_name)
        print(i, outfile_smeared)
        with open(outfile_smeared, 'w+') as f_out_smeared:
            ret = lib.glbShowChannelRates(f_out_smeared, 0, chan_num[i], lib.GLB_POST, lib.GLB_W_EFF, lib.GLB_W_BG)

    bgfile = 'backgrounds/bg_chan_{}.dat'.format(expt_config_name)

    if os.path.exists(bgfile):

        outfile = "out/{}_bg_chan_{}_events_unweighted.dat".format(flux_file_name, expt_config_name)
        with open(outfile, 'w+') as f_out:
            ret = lib.glbShowChannelRates(f_out, 0, chan_num[i], lib.GLB_PRE, lib.GLB_WO_EFF, lib.GLB_W_BG)

        outfile_smeared = "out/{}_bg_chan_{}_events_smeared_unweighted.dat".format(flux_file_name, expt_config_name)
        with open(outfile_smeared, 'w+') as f_out_smeared:
            ret = lib.glbShowChannelRates(f_out_smeared, 0, chan_num[i], lib.GLB_POST, lib.GLB_W_EFF, lib.GLB_W_BG)
    else:
        print("No background file")

    lib.glbFreeParams(true_values)
    lib.glbFreeParams(test_values)

    return(0)


def create_AEDL_file(fluxname, channame, expt_config):

    exename = "bin/supernova"

    chanfilename = "channels/channels_{}.dat".format(channame)

    #Create the GLOBES file
    globesfilename = "supernova.glb"

    GLOBESFILE = open(globesfilename, 'w')

    #Open the preamble, read contents and print to GLOBES file
    with open("glb/preamble.glb") as PREAMBLE:
        preamble_contents = PREAMBLE.read()
        print(preamble_contents, file = GLOBESFILE)

    #Create the corresponding flux file name
    fluxfilename = "fluxes/{}.dat".format(fluxname)
    if not os.path.exists(fluxfilename):
        print("Flux file name {} not found".format(fluxfilename))

    #Open the flux globes file, read contents and replace supernova_flux.dat with the fluxfilename
    with open("glb/flux.glb") as FLUX:
        flux_contents = FLUX.read()
        flux_contents1 = re.sub('supernova_flux.dat', fluxfilename, flux_contents)
        print(flux_contents1, end = '', file = GLOBESFILE)

    if not os.path.exists(chanfilename):
        print("Flux file name {} not found".format(chanfilename))

    #Channel data
    #start with smearing
    #Open the channel file and grab the channel name.
    with open(chanfilename) as CHANFILE:
        stuff = [i.split() for i in CHANFILE]
        chan_names = [item[0] for item in stuff]
    #Print the smearing data file name for each channel in the channel file to the GLOBES file
        for chan_name in chan_names:
            output_line = "include \"smear/smear_{}_{}.dat\"".format(chan_name, expt_config)
            print(output_line, file = GLOBESFILE)

    #Define the detector configurations file name
    detfilename = "detector_configurations.dat"

    #include error essage if wrong input
    if not os.path.exists(detfilename):
        print("Detector file name {} not found".format(detfilename))

    #Open the detector configurations file
    with open(detfilename) as DETFILENAME:
        for line in DETFILENAME:
            #skip any leading comments
            if line.startswith('#'):
                pass
            p = re.compile("\s+")
            formatted_line=p.sub(" ", line)
            #Grab the detector names, masses, and normalization factors
            stuff = [i.split() for i in DETFILENAME]
            detname = [item[0] for item in stuff]
            masses =  [item[1] for item in stuff]
            normfactor = [item[2] for item in stuff]
            index = detname.index(expt_config)
            #Convert the lists into arrays, in order to do math
            masses_array = np.array(masses, dtype = float)
            normfactor_array = np.array(normfactor, dtype = float)

            #Skip any blank lines
            if ((detname == "") or (masses == "") or (normfactor == "")):
                pass

    #Calculate the target mass in ktons of free particles
    target_mass_raw = masses_array[index] * normfactor_array[index]
    #Format the target mass for output. (13 total spaces, with 6 trailing decimals?)
    target_mass = '{:13.6f}'.format(target_mass_raw)

    #Print the experiment configuration and corresponding mass to the terminal
    print("Experiment config: {} Mass: {} kton ".format(expt_config, masses[index]))

    #ADD the background smearing here, for the given detector configuration
    #There are not yet background channels for all detectors.

    do_bg = 0
    bg_chan_name = "bg_chan"

    #Determine the background file name
    bg_filename = "backgrounds/{}_{}.dat".format(bg_chan_name, expt_config)

    #Check whether the file exists
    if os.path.exists(bg_filename):
        do_bg = 1
        print("Using background file {}".format(bg_filename))
    else:
        print("No background file for this configuration")

    #If the file exists, print the background smearing file for each channel to the GLOBES file
    if do_bg == 1 :
        output_line = "include \"smear/smear_{}_{}.dat\"".format(bg_chan_name, expt_config)
        print(output_line, file = GLOBESFILE)

    print("\n/* ####### Detector settings ####### */\n", file = GLOBESFILE)
    print("$target_mass= {}\n".format(target_mass), file = GLOBESFILE)

    print("\n /******** Cross-sections ********/\n", file = GLOBESFILE)

    #Open the channel file and grab the channel names
    with open(chanfilename) as CHANFILE:
        stuff = [i.split() for i in CHANFILE]
        chan_names = [item[0] for item in stuff]
        #For each of the channels, print the cross-sections file name to GLOBES file
        for chan in chan_names:
            print("cross(#{})<".format(chan), file = GLOBESFILE)
            print("      @cross_file= \"xscns/xs_{}.dat\"".format(chan), file = GLOBESFILE)
            print(">", file = GLOBESFILE)

    #Add the fake bg channel cross section, if it exists for this configuration
    if do_bg == 1 :
        print("cross(#{})<".format(bg_chan_name), file = GLOBESFILE)

        print("     @cross_file= \"xscns/xs_zero.dat\"", file = GLOBESFILE)

        print(">", file = GLOBESFILE)


    print("\n /********* Channels ********/\n", file = GLOBESFILE)

    #NOW the channel definitions...
    #INCLUDE ERROR message
    if not os.path.exists(chanfilename):
        print("Channel file name {} not found".format(chanfilename))

    #Open the channel file and grab the channel names, index, cpstate, and inflav
    with open(chanfilename) as CHANFILE:
        stuff = [i.split() for i in CHANFILE]
        chan_name = [item[0] for item in stuff]
        index = [item[1] for item in stuff]
        index = np.array(index, dtype = int)
        cpstate =  [item[2] for item in stuff]
        inflav = [item[3] for item in stuff]

        #Iterating over each channel by using the index, we print the channel name, cpstate, and inflav to GLOBES file
        for i in index:

            print("channel(#{}_signal)<".format(chan_name[i]), file = GLOBESFILE)

            print("      @channel= #supernova_flux:  {}:    {}:     {}:    #{}:    #{}_smear".format(cpstate[i], inflav[i], inflav[i], chan_name[i], chan_name[i]), file = GLOBESFILE)


            #Get the post-smearing efficiency file names for each channel
            eff_file = "effic/effic_{}_{}.dat".format(chan_name[i], expt_config)
            #Now open the efficiency files, read the contents, the print the efficiency matrices to the GLOBES file
            with open(eff_file) as EFF_FILE:
                eff_file_contents = EFF_FILE.read()
                print("       @post_smearing_efficiencies = {}".format(eff_file_contents) , file = GLOBESFILE)

            print(">\n", file = GLOBESFILE)

    #NOW make a fake channel background... There is only one bgfile for now
    if do_bg == 1:

        #this is dummy info... NOT SURE WHAT TO DO WITH THIS
        cpstate = "-"
        inflav = "e"
        output_line = "channel(#{}_signal)<".format(bg_chan_name)
        print(output_line, file = GLOBESFILE)

        output_line = "      @channel= #supernova_flux:  {}:    {}:     {}:    #{}:    #{}_smear".format(cpstate, inflav, inflav, bg_chan_name, bg_chan_name)
        print(output_line, file = GLOBESFILE)

        #get the pre smearing backgrounds by channels
        bg_file = "backgrounds/{}_{}.dat".format(bg_chan_name, expt_config)
        print(bg_file, "\n")

        #Open the background file and output the file name to the GLOBES file
        with open(bg_file) as BG_FILE:
            bgfilecontents = BG_FILE.read()
            output_line = "       @pre_smearing_background = {}".format(bgfilecontents)
            print(output_line, file = GLOBESFILE)

        print("\n>\n", file = GLOBESFILE)

    #END-MATTER

    #Open the postamble, read contents, and print them to the Globes file
    with open("glb/postamble.glb") as POSTAMBLE:
        postamble_contents = POSTAMBLE.read()
        print(postamble_contents, end = '', file = GLOBESFILE)

    #Close the Globes file
    GLOBESFILE.close()
    return(0)

#Define the function that will apply the channel weighting factors
def apply_weights(filename):
    #Open the channel file and grab all the info
    with open(chanfilename) as CHANFILE:
        stuff = [i.split() for i in CHANFILE]
        chan_names = [item[0] for item in stuff]
        index = [item[1] for item in stuff]
        index = np.array(index, dtype = int)
        cpstate =  [item[2] for item in stuff]
        inflav = [item[3] for item in stuff]
        num_target_factor = [item[4] for item in stuff]
        num_target_factor_array = np.array(num_target_factor, dtype = float)

        #OPEN the unweighted output file as input and the weighted file as output
        #essentially we begin with the unweighted file that is made by globes then we weight it
        #and then we weight the smeared one resulting in a total of 3 files per config setup

        #Iterating over the channels by using the index, we create the unweighted and weighted file names for each channel
        for i in index:
            unweightedfilename = "out/{}_{}_{}_events{}_unweighted.dat".format(fluxname, chan_names[i], expt_config, filename)

            weightedfilename = "out/{}_{}_{}_events{}.dat".format(fluxname, chan_names[i], expt_config, filename)

            #Using the index, we select the num_target_factor for the corresponding channel
            num = num_target_factor_array[i]

            #Open both files
            with open(unweightedfilename, 'r') as UNWEIGHTED:
                with open(weightedfilename, 'w') as WEIGHTED:
                    for line in UNWEIGHTED:

                        line = line.strip()
                        #Replace any contiguous whitespace with a single space
                        p = re.compile("\s+")
                        formatted_line=p.sub(" ", line)
                        #Skip any blank lines
                        if not line:
                            continue
                        #Skip any lines that begin with comments
                        if line.startswith("#"):
                            continue

                        #Match the end of the data, and print the bar
                        if line == "----------------------":
                            print("----------------------", file = WEIGHTED)
                        else:
                            np.set_printoptions(precision=6)
                            #If we're not at the end of the file, save each line into stuff2
                            #Split stuff2 into enbin and evrate
                            stuff2 = formatted_line.split()
                            enbin = stuff2[0]
                            evrate = stuff2[1]
                            #If there is a value for enbin, then we print the weighted info into the weighted file
                            if enbin != "" :
                                #Convert the evrate into an array
                                evrate_array = np.array(evrate, dtype = float)
                                #Calculate the new evrate, by multiplying the evrate with the num_target_factor for the specific channel as given by num
                                new_evrate = np.dot(evrate_array, num)

                                #Print the weighted data to the weighted file
                                output = "{} {}".format(enbin, new_evrate)
                                print(output, file = WEIGHTED)
