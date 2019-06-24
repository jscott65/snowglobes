import re
import os

from snowglobes.helper import get_abs_path

class AEDL():

    def __init__(self):
        self.filename = "supernova.glb"
        self.file_obj = open(self.filename, mode='a')
        self.file_obj.truncate(0)

    def __enter__(self):
        return(self.file_obj)

    def Preamble(self):
        self.preamble = get_abs_path("glb/preamble.glb")
        with open(self.preamble) as f_in:
            preamble_contents = f_in.read()
        self.file_obj.write(preamble_contents)

    def SetFlux(self, fluxname):
        self.flux = get_abs_path("glb/flux.glb")
        fluxfilename = get_abs_path("fluxes/{}.dat".format(fluxname))
        if not os.path.exists(fluxfilename):
            print("Flux file name {} not found".format(fluxfilename))
        with open(self.flux) as f_in:
            flux_contents = f_in.read()
            flux_contents1 = re.sub('supernova_flux.dat', fluxfilename, flux_contents)
        self.file_obj.write(flux_contents1)

    def SetSmearing(self, chan, expt_config):
        for chan_name in chan.name:
            output_line = "include \"{}\"\n".format(get_abs_path('smear/smear_{}_{}.dat').format(chan_name, expt_config))
            self.file_obj.write(output_line)

    def SetBackground(self, expt_config):
        self.do_bg = False
        self.bg_chan_name = "bg_chan"
        self.bg_filename = get_abs_path("backgrounds/{}_{}.dat".format(self.bg_chan_name, expt_config))
        if os.path.exists(self.bg_filename):
            self.do_bg = True
            print("Using background file {}".format(self.bg_filename))
        else:
            print("No background file for this configuration")
        if self.do_bg == True:
            self.file_obj.write("include \"{}\"\n".format(get_abs_path('smear/smear_{}_{}.dat').format(self.bg_chan_name, expt_config)))

    def SetTargetMass(self, det, expt_config):
        target_mass_raw = det.get_target_mass(expt_config)
        target_mass = '{:13.6f}'.format(target_mass_raw)
        print("Experiment config: {} Mass: {} kton ".format(expt_config, det.mass[det.get_index(expt_config)]))
        self.file_obj.write("\n/* ####### Detector settings ####### */\n\n")
        self.file_obj.write("$target_mass= {}\n\n".format(target_mass))

    def SetCrossSections(self, chan):
        self.file_obj.write("\n /******** Cross-sections ********/\n\n")
        for chan_name in chan.name:
            self.file_obj.write("cross(#{})<\n".format(chan_name))
            self.file_obj.write("      @cross_file= \"{}\"\n".format(get_abs_path('xscns/xs_{}.dat'.format(chan_name))))
            self.file_obj.write(">\n")
        if self.do_bg == True:
            self.file_obj.write("cross(#{})<\n".format(self.bg_chan_name))
            self.file_obj.write("     @cross_file= \"{}\"\n".format(get_abs_path('xscns/xs_zero.dat')))
            self.file_obj.write(">\n")

    def SetChannels(self, chan, expt_config):
        self.file_obj.write("\n /********* Channels ********/\n\n")
        if not os.path.exists(chan.chan_file_name):
            print("Channel file name {} not found".format(chan.chan_file_name))
        for i, chan_name in enumerate(chan.name):
            self.file_obj.write("channel(#{}_signal)<\n".format(chan_name))
            self.file_obj.write("      @channel= #supernova_flux:  {}:    {}:     {}:    #{}:    #{}_smear\n".format(chan.cp[i], chan.flav[i], chan.flav[i], chan_name, chan_name))
            eff_file = get_abs_path("effic/effic_{}_{}.dat".format(chan_name, expt_config))
            with open(eff_file) as f_in:
                eff_file_contents = f_in.read()
                self.file_obj.write("       @post_smearing_efficiencies = {}\n".format(eff_file_contents))
                self.file_obj.write(">\n\n")

    def MakeBackgroundChannel(self, expt_config):
        if self.do_bg == True:
            cpstate = "-"
            inflav = "e"
            self.file_obj.write("channel(#{}_signal)<\n".format(self.bg_chan_name))
            self.file_obj.write("      @channel= #supernova_flux:  {}:    {}:     {}:    #{}:    #{}_smear\n".format(cpstate, inflav, inflav, self.bg_chan_name, self.bg_chan_name))
            print(self.bg_filename, "\n")

            with open(self.bg_filename) as f_in:
                bgfilecontents = f_in.read()
                self.file_obj.write("       @pre_smearing_background = {}\n".format(bgfilecontents))
                self.file_obj.write("\n>\n\n")

    def Postamble(self):
        #with open(get_abs_path("glb/postamble.glb")) as f_in:
        #    postamble_contents = f_in.read()
        #    self.file_obj.write(postamble_contents)

        rule = """
        /*  Need at least one rule although osc code not used.  This signal will be present in any configuration */

        rule(#nue_e_events)<
                @signal = 1.0@#nue_e_signal
                @signalerror = 0.011 : 0.00005
                @background = 0.0@#nue_e_signal
                @backgrounderror = 0.011 : 0.00005
                @sys_on_function = "chiSpectrumTilt"
        	@sys_off_function = "chiNoSysSpectrum"
        	@energy_window = 0.0005 : 0.100          /* Range of analysis: 5 MeV < E_vis < 55 MeV */
        >



        /**********************END**********************/
        """
        self.file_obj.write(rule)

    def Close(self):
        self.file_obj.close()

    def __exit__(self, type, value, traceback):
        self.file_obj.close()
        return True


def create_AEDL_file(fluxname, chan, det, expt_config):

    aedl = AEDL()
    aedl.Preamble()
    aedl.SetFlux(fluxname)
    aedl.SetSmearing(chan, expt_config)
    aedl.SetBackground(expt_config)
    aedl.SetTargetMass(det, expt_config)
    aedl.SetCrossSections(chan)
    aedl.SetChannels(chan, expt_config)
    aedl.MakeBackgroundChannel(expt_config)
    aedl.Postamble()
    aedl.Close()
