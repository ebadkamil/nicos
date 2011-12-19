#  -*- coding: utf-8 -*-

name = 'Monoturm, everything inside the Monochromator housing'

#~ includes = ['system','panda_s7']
includes = ['system']
 
 # 5,mfh,mgx,mtx,mtx,mth,mtt,-,mfv

devices = dict(
    bus5 = device('nicos.ipc.IPCModBusTaco',
            tacodevice='//pandasrv/panda/moxa/port5',
            loglevel='info',
            timeout=0.5,
    ),
    
    # MFH is first device and has 1 stepper, 0 poti, 0 coder and maybe 1 something else (resolver)
    mfh_step = device('nicos.ipc.Motor',
            bus = 'bus5',
            addr = 0x51,
            slope = 1000,
            unit = 'deg',
            abslimits = (-400,400),
            offset = 500000,
            confbyte = 8,
            speed = 50,
            accel = 50,
            microstep = 2,
            startdelay = 0,
            stopdelay = 0,
            ramptype = 1,
            #~ current = 0.2,
    ),
    mfh_poti = device('nicos.ipc.Coder',
            bus = 'bus5',
            addr = 0x61,
            slope = 1,
            offset = 0,
            unit = 'deg',
    ),
    mfh = device('nicos.axis.Axis',
            motor = 'mfh_step',
            coder = 'mfh_step',
            obs = [],
            precision = 1,
            #~ rotary = True,
    ),
    
    #
    # MGX is second device and has 1 stepper, 1 poti, 0 coder
    # endschalter+=599620 steps,poti=852 ca. 3.1 deg
    # 0 = 500000 steps, poti=2259
    # endschalter-=398852, poti=3727 ca 3.16 deg
    mgx_step = device('nicos.ipc.Motor',
            bus = 'bus5',
            addr = 0x52,
            slope = 32000,
            unit = 'deg',
            abslimits = (-3,3),
            offset = 500000,
            speed = 200,
            accel = 50,
            microstep = 16,
            divider = 4,
            #~ current = 1.5,
    ),
    mgx_poti = device('nicos.ipc.Coder',
            bus = 'bus5',
            addr = 0x62,
            slope = -459.16,
            offset = 2259,
            unit = 'deg',
    ),
    mgx = device('nicos.axis.Axis',
            motor = 'mgx_step',
            coder = 'mgx_poti',
            obs = [],
            precision = 0.01,
    ),
    
    #
    # MTX is third device and has 1 stepper, 1 poti, 0 coder
    # endschalter- =248643 steps, poti=0, ca 15.7mm
    # 0 = 500000 steps, poti=3910
    # endschalter+ 553200= steps, poti=4790, ca -3.3mm
    mtx_step = device('nicos.ipc.Motor',
            bus = 'bus5',
            addr = 0x53,
            slope = 1000,
            unit = 'mm',
            abslimits = (-15,3),
            offset = 500000,
            speed = 200,
            accel = 50,
            microstep = 16,
            divider = 4,
            #~ current = 1.5,
    ),
    mtx_poti = device('nicos.ipc.Coder',
            bus = 'bus5',
            addr = 0x63,
            slope = 265.25,
            offset = 3910,
            unit = 'mm',
    ),
    mtx = device('nicos.axis.Axis',
            motor = 'mtx_step',
            coder = 'mtx_poti',
            precision = 0.1,
            obs = [],
            loopdelay=1,
            fmtstr='%.1f',
    ),
    
    #
    # MTY is fourth device and has 1 stepper, 1 poti, 0 coder
    # endschalter- steps=684692, poti= 862, 11.5mm
    # 0 500000 steps, poti=3940
    # endschalter+ = 294059, poti=7436, -12.8mm
    mty_step = device('nicos.ipc.Motor',
            bus = 'bus5',
            addr = 0x54,
            slope = -16000,
            unit = 'mm',
            abslimits = (-11,11),
            offset = 500000,
            speed = 200,
            accel = 50,
            microstep = 16,
            divider = 4,
            #~ current = 1.5,
    ),
    mty_poti = device('nicos.ipc.Coder',
            bus = 'bus5',
            addr = 0x64,
            slope = 269.2655,
            offset = 3940,
            unit = 'mm',
    ),
    mty = device('nicos.axis.Axis',
            motor = 'mty_step',
            coder = 'mty_poti',
            obs = [],
            precision = 0.1,
            loopdelay=1,
            fmtstr='%.1f',
    ),
    
    #
    # MTH is fith device and has 1 stepper, 0 poti, 1 coder
    mth_step = device('nicos.ipc.Motor',
            bus = 'bus5',
            addr = 0x55,
            slope = 8000,
            unit = 'deg',
            abslimits = (-30,130),
            offset = 500000,
            speed = 200,
            accel = 80,
            microstep = 8,
            divider = 4,
            #~ current = 1.5,
    ),
    mth_enc = device('nicos.ipc.Coder',
            bus = 'bus5',
            addr = 0x75,
            slope = (2**26)/360.0,
            offset = 35200000,
            confbyte = 154,
            unit = 'deg',
    ),
    mth = device('nicos.axis.Axis',
            motor = 'mth_step',
            coder = 'mth_enc',
            obs = [],
            precision = 0.01,
            offset = 0.0,
    ),

    #
    # MTT is sixth device and has 0 stepper, 0 poti, 1 coder
    mtt_enc = device('nicos.ipc.Coder',
            bus = 'bus5',
            addr = 0x76,
            slope = (2**26)/360.0,
            offset = 0,
            confbyte = 154,
            unit = 'deg',
    ),
    #~ mtt = device('nicos.axis.Axis',
            #~ motor = 'mtt_step',
            #~ coder = 'mtt_enc',
            #~ precision = 0.01,
    #~ ),
    
    #
    # MS1 is seventh device and has 1 stepper, 0 poti, 0 coder
    ms1_step = device('nicos.ipc.Motor',
            bus = 'bus5',
            addr = 0x57,
            slope = -200/3.0,
            unit = 'steps',
            abslimits = (0.0, 50.0),
            offset = 500000,
            #~ refpos = 496587,
            #~ refswitch = 'low',
    ),
    ms1 = device('nicos.axis.Axis',
            motor = 'ms1_step',
            coder = 'ms1_step',
            obs = [],
            precision = 0.1,
    ),
    
    #
    # MFV is eigth device and has 1 stepper, 0 poti, 0 coder and maybe 1 something else (resolver)
    mfv_step = device('nicos.ipc.Motor',
            bus = 'bus5',
            addr = 0x58,
            slope = 1000,
            unit = 'deg',
            abslimits = (-400,400),
            offset = 500000,
            confbyte=8,
            #~ current = 0.2,
    ),
    mfv_poti = device('nicos.ipc.Coder',
            bus = 'bus5',
            addr = 0x68,
            slope = 1,
            offset = 0,
            unit = 'deg',
    ),
    mfv = device('nicos.axis.Axis',
            motor = 'mfv_step',
            coder = 'mfv_step',
            obs = [],
            precision = 1,
            #~ rotary = True,
    ),
    
)
