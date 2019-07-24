import os

from pyglobes._pyglobes import ffi, lib
from snowglobes.helper import get_abs_path


class GLB():

    __slots__ = ()

    def __init__(self):
        arg = ffi.new("char[]", b"snowglobes.py")
        lib.glbInit(arg)
        lib.PInit(b"supernova.glb")

    def AllocParams(self):
        return(lib.glbAllocParams())

    def DefineParams(self, true_values, theta12, theta13, theta23, deltacp, sdm, ldm):
        lib.glbDefineParams(true_values, theta12, theta13, theta23, deltacp, sdm, ldm)

    def SetDensityParams(self, true_values, density, which):
        lib.glbSetDensityParams(true_values, density, which)

    def SetOscillationParams(self, true_values):
        lib.glbSetOscillationParameters(true_values)

    def SetRates(self):
        lib.glbSetRates()

    def ShowChannelRates(self, f_out, exp, channel, smearing, effi, bgi):
        lib.glbShowChannelRates(f_out, exp, channel, smearing, effi, bgi)

    def PrintChannelRates(self, fluxname, chan, expt_config, *bgfile):
        for i, chan_name in enumerate(chan.name):
            if bgfile:
                outfile = get_abs_path(
                    "out/{}_bg_chan_{}_events_unweighted.dat".format(fluxname, expt_config))
            else:
                outfile = get_abs_path(
                    "out/{}_{}_{}_events_unweighted.dat".format(fluxname, chan_name, expt_config))
            print(i, outfile)
            # Add new directory if it doesnt exist
            os.makedirs(os.path.dirname(outfile), exist_ok=True)

            with open(outfile, 'w+') as f_out:
                ret = self.ShowChannelRates(
                    f_out, 0, chan.num[i], lib.GLB_PRE, lib.GLB_WO_EFF, lib.GLB_WO_BG)
            if bgfile:
                outfile_smeared = get_abs_path(
                    "out/{}_bg_chan_{}_events_smeared_unweighted.dat".format(fluxname, expt_config))
            else:
                outfile_smeared = get_abs_path(
                    "out/{}_{}_{}_events_smeared_unweighted.dat".format(fluxname, chan_name, expt_config))
            print(i, outfile_smeared)
            with open(outfile_smeared, 'w+') as f_out_smeared:
                ret = self.ShowChannelRates(
                    f_out_smeared, 0, chan.num[i], lib.GLB_POST, lib.GLB_W_EFF, lib.GLB_W_BG)

    def FreeParams(self, true_values):
        lib.glbFreeParams(true_values)
