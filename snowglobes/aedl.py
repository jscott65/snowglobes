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
        fluxfilename = get_abs_path(f"fluxes/{fluxname}.dat")
        if not os.path.exists(fluxfilename):
            print(f"Flux file name {fluxfilename} not found")
        with open(self.flux) as f_in:
            flux_contents = f_in.read()
            flux_contents1 = re.sub('{flux}', fluxfilename, flux_contents)
        self.file_obj.write(flux_contents1)

    def SetSmearing(self, chan, expt_config):
        for chan_name in chan.name:
            output_line = "include \"{}\"\n".format(get_abs_path(
                f'smear/smear_{chan_name}_{expt_config}.dat'))
            self.file_obj.write(output_line)

    def SetBackground(self, expt_config):
        self.do_bg = False
        self.bg_chan_name = "bg_chan"
        self.bg_filename = get_abs_path(
            f"backgrounds/{self.bg_chan_name}_{expt_config}.dat")
        if os.path.exists(self.bg_filename):
            self.do_bg = True
            print(f"Using background file {self.bg_filename}")
        else:
            print("No background file for this configuration")
        if self.do_bg == True:
            self.file_obj.write("include \"{}\"\n".format(get_abs_path(
                f'smear/smear_{self.bg_chan_name}_{expt_config}.dat')))

    def SetTargetMass(self, det, expt_config):
        target_mass_raw = det.get_target_mass(expt_config)
        target_mass = '{:13.6f}'.format(target_mass_raw)
        print(f"Experiment config: {expt_config} Mass: {det.mass[det.get_index(expt_config)]} kton")
        self.file_obj.write("\n/* ####### Detector settings ####### */\n\n")
        self.file_obj.write(f"$target_mass= {target_mass}\n\n")

    def SetCrossSections(self, chan):
        self.file_obj.write("\n /******** Cross-sections ********/\n\n")
        for chan_name in chan.name:
            self.file_obj.write(f"cross(#{chan_name})<\n")
            self.file_obj.write("      @cross_file= \"{}\"\n".format(
                get_abs_path(f'xscns/xs_{chan_name}.dat')))
            self.file_obj.write(">\n")
        if self.do_bg == True:
            self.file_obj.write(f"cross(#{self.bg_chan_name})<\n")
            self.file_obj.write("     @cross_file= \"{}\"\n".format(
                get_abs_path('xscns/xs_zero.dat')))
            self.file_obj.write(">\n")

    def SetChannels(self, chan, expt_config):
        self.file_obj.write("\n /********* Channels ********/\n\n")
        if not os.path.exists(chan.chan_file_name):
            print("Channel file name {} not found".format(chan.chan_file_name))
        for i, chan_name in enumerate(chan.name):
            self.file_obj.write(f"channel(#{chan_name}_signal)<\n")
            self.file_obj.write(f"      @channel= #supernova_flux:  {chan.cp[i]}:    {chan.flav[i]}:     {chan.flav[i]}:    #{chan_name}:    #{chan_name}_smear\n")
            eff_file = get_abs_path(f"effic/effic_{chan_name}_{expt_config}.dat")
            with open(eff_file) as f_in:
                eff_file_contents = f_in.read()
                self.file_obj.write(f"       @post_smearing_efficiencies = {eff_file_contents}\n")
                self.file_obj.write(">\n\n")

    def MakeBackgroundChannel(self, expt_config):
        if self.do_bg == True:
            cpstate = "-"
            inflav = "e"
            self.file_obj.write(f"channel(#{self.bg_chan_name}_signal)<\n")
            self.file_obj.write(f"      @channel= #supernova_flux:  {cpstate}:    {inflav}:     {inflav}:    #{self.bg_chan_name}:    #{self.bg_chan_name}_smear\n")
            print(self.bg_filename, "\n")

            with open(self.bg_filename) as f_in:
                bgfilecontents = f_in.read()
                self.file_obj.write(f"       @pre_smearing_background = {bgfilecontents}\n")
                self.file_obj.write("\n>\n\n")

    def Postamble(self):
        # with open(get_abs_path("glb/postamble.glb")) as f_in:
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

#    def SetParam(self, infile, params):
#        for i, param in enumerate(params):
#            with open(infile, mode='r') as f_in:
#                 self.file_obj.write(f_in.read().format(**param))
#
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


if __name__ == '__main__':
    print("add aedl file test")
