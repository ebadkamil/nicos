#  -*- coding: utf-8 -*-

description = 'Capacity box %s' % setupname
group = 'optional'

devices = {
    '%s_fg_freq' % setupname:
        device('nicos.devices.generic.ManualMove',
            description = 'Frequency generator frequency',
            pollinterval = 30,
            fmtstr = '%.3g',
            unit = 'Hz',
            abslimits = (35000, 4000000),
            default = 35000,
        ),
    '%s_reg_amp' % setupname:
        device('nicos.devices.generic.ManualMove',
        # device('nicos_mlz.reseda.devices.rte1104.RTE1104YScaleSetting',
            description = 'amplitude setting chain of subdevices: setting channel 3',
            # io = 'rte1104_io',
            # channel = 3,
            # regulator = device('nicos_mlz.reseda.devices.rte1104.RTE1104YScaleSetting',
            #     description = 'amplitude setting chain of subdevices: setting channel 4',
            #     io = 'rte1104_io',
            #     channel = 4,
            #     regulator = device('nicos_mlz.reseda.devices.regulator.Regulator',
            #         description = 'Auto regulating amplitude',
            #         sensor = '%s_coil1_rms' % setupname,
            #         moveable = '%s_fg_amp' % setupname,
            #         loopdelay = 1.0,
            #         maxage = 10.0,
            #         maxstep = 0.1,
            #         minstep = 0.005,
            #         pollinterval = 1.0,
            #         stepfactor = 0.3,
            #         unit = 'V',
            #     ),
            # ),
            unit = 'V',
            abslimits = (0, 10),
        ),
    # '%s_fg_amp' % setupname:
    #     device('nicos.devices.tango.AnalogOutput',
    #         description = 'Frequency generator amplitude',
    #         tangodevice = '%s/%s/fg_amplitude' % (tango_base, setupname),
    #         pollinterval = 30,
    #         # precision = 0.01,
    #         unit = 'V',
    #     ),
    # '%s_fwdp' % setupname:
    #     device('nicos.devices.tango.AnalogInput',
    #         description = 'Power amplifier forward power',
    #         tangodevice = '%s/%s/pa_fwdp' % (tango_base, setupname),
    #         pollinterval = 10,
    #         unit = 'W',
    #     ),
    # '%s_revp' % setupname:
    #     device('nicos.devices.tango.AnalogInput',
    #         description = 'Power amplifier reverse power',
    #         tangodevice = '%s/%s/pa_revp' % (tango_base, setupname),
    #         pollinterval = 10,
    #         unit = 'W',
    #     ),
    '%s' % setupname:
        device('nicos_mlz.reseda.devices.cbox.CBoxResonanceFrequency',
            pollinterval = 30,
            description = 'CBox',
            unit = 'Hz',
            power_divider = device('nicos.devices.generic.ManualSwitch',
                description = 'Power divider to split the power for both coils',
                lowlevel = False,  # temporary due to inaccurate auto tune
                states = [0, 1],
                unit = '',
                fmtstr = '%d',
            ),
            highpass = device('nicos.devices.generic.ManualSwitch',
                description = 'Highpass filter to smooth the signal',
                lowlevel = False,  # temporary due to inaccurate auto tune
                states = [0, 1],
                unit = '',
                fmtstr = '%d',
            ),
            # pa_fwdp = '%s_fwdp' % setupname,
            # pa_revp = '%s_revp' % setupname,
            fg = '%s_fg_freq' % setupname,
            # coil_amp = '%s_coil1_rms' % setupname,
            diplexer = device('nicos.devices.generic.ManualSwitch',
                description = 'Lowpass filter to smooth the signal (enable for low frequency, disable for high frequency)',
                lowlevel = False,  # temporary due to inaccurate auto tune
                states = [0, 1],
                unit = '',
                fmtstr = '%d',
            ),
            coil1_c1 = device('nicos.devices.generic.ManualSwitch',
                description = 'Coil 1: Capacitor bank 1',
                lowlevel = False,  # temporary due to inaccurate auto tune
                states = [0, 1],
                unit = '',
                fmtstr = '%d',
            ),
            coil1_c2 = device('nicos.devices.generic.ManualSwitch',
                description = 'Coil 1: Capacitor bank 2',
                lowlevel = False,  # temporary due to inaccurate auto tune
                states = [0, 1],
                unit = '',
                fmtstr = '%d',
            ),
            coil1_c3 = device('nicos.devices.generic.ManualSwitch',
                description = 'Coil 1: Capacitor bank 3',
                lowlevel = False,  # temporary due to inaccurate auto tune
                states = [0, 1],
                unit = '',
                fmtstr = '%d',
            ),
            coil1_c1c2serial = device('nicos.devices.generic.ManualSwitch',
                description = 'Coil 1: Use c1 and c2 in serial instead of parallel',
                lowlevel = False,  # temporary due to inaccurate auto tune
                states = [0, 1],
                unit = '',
                fmtstr = '%d',
            ),
            coil1_transformer = device('nicos.devices.generic.ManualSwitch',
                description = 'Coil 1: Used to manipulate the coil resistance to match the power amplifier resistance',
                lowlevel = False,  # temporary due to inaccurate auto tune
                states = [0, 1],
                unit = '',
                fmtstr = '%d',
            ),
            coil2_c1 = device('nicos.devices.generic.ManualSwitch',
                description = 'Coil 2: Capacitor bank 1',
                lowlevel = False,  # temporary due to inaccurate auto tune
                states = [0, 1],
                unit = '',
                fmtstr = '%d',
            ),
            coil2_c2 = device('nicos.devices.generic.ManualSwitch',
                description = 'Coil 2: Capacitor bank 2',
                lowlevel = False,  # temporary due to inaccurate auto tune
                states = [0, 1],
                unit = '',
                fmtstr = '%d',
            ),
            coil2_c3 = device('nicos.devices.generic.ManualSwitch',
                description = 'Coil 2: Capacitor bank 3',
                lowlevel = False,  # temporary due to inaccurate auto tune
                states = [0, 1],
                unit = '',
                fmtstr = '%d',
            ),
            coil2_c1c2serial = device('nicos.devices.generic.ManualSwitch',
                description = 'Coil 2: Use c1 and c2 in serial instead of parallel',
                lowlevel = False,  # temporary due to inaccurate auto tune
                states = [0, 1],
                unit = '',
                fmtstr = '%d',
            ),
            coil2_transformer = device('nicos.devices.generic.ManualSwitch',
                description = 'Coil 2: Used to manipulate the coil resistance to match the power amplifier resistance',
                lowlevel = False,  # temporary due to inaccurate auto tune
                states = [0, 1],
                unit = '',
                fmtstr = '%d',
            ),
        ),
    # '%s_coil1_rms' % setupname:
    #     device('nicos_mlz.reseda.devices.rte1104.RTE1104',
    #     description = 'rms Coil1 (Input channel 3)',
    #     io = 'rte1104_io',
    #     channel = 3,
    #     unit = 'V',
    # ),
    # '%s_coil2_rms' % setupname:
    #     device('nicos_mlz.reseda.devices.rte1104.RTE1104',
    #     description = 'rms Coil2 (Input channel 4)',
    #     io = 'rte1104_io',
    #     channel = 4,
    #     unit = 'V',
    # ),
}