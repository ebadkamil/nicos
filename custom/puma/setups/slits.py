#  -*- coding: utf-8 -*-

description = 'Sample Slits'

group = 'optional'

includes = ['system', 'motorbus6']



devices = dict(

    ss1_l_mot = device('nicos.devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'motorbus6a',
                       addr = 47,
                       side = 2,
                       slope = -82.3045,
                       zerosteps = 1876.5426,
                       resetpos = -20,
                       abslimits = (-25, 20),
                       timeout = 10,
                      ),
    ss1_r_mot = device('nicos.devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'motorbus6a',
                       addr = 47,
                       side = 3,
                       slope = 82.3045,
                       zerosteps = 1876.5426,
                       resetpos = 20,
                       abslimits = (-20, 25),
                       timeout = 10,
                      ),
    ss1_b_mot = device('nicos.devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'motorbus6a',
                       addr = 47,
                       side = 0,
                       slope = -54.25,
                       zerosteps = 1209.775,
                       resetpos = -40,
                       abslimits = (-50, 20),
                       timeout = 10,
                      ),
    ss1_t_mot = device('nicos.devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'motorbus6a',
                       addr = 47,
                       side = 1,
                       slope = 54.25,
                       zerosteps = 1209.775,
                       resetpos = 40,
                       abslimits = (-40, 50),
                       timeout = 10,
                      ),

    ss1_l     = device('nicos.devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = -2.,
                       motor = 'ss1_l_mot',
                       coder = 'ss1_l_mot',
                       obs = None,
                      ),
    ss1_r     = device('nicos.devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = 2.,
                       motor = 'ss1_r_mot',
                       coder = 'ss1_r_mot',
                       obs = None,
                      ),
    ss1_b     = device('nicos.devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = -2.,
                       motor = 'ss1_b_mot',
                       coder = 'ss1_b_mot',
                       obs = None),
    ss1_t     = device('nicos.devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = 2.,
                       motor = 'ss1_t_mot',
                       coder = 'ss1_t_mot',
                       abslimits = (-40, 50),
                       obs = None,
                      ),

    slit1     = device('nicos.devices.generic.Slit',
                       description = 'sample slit 1',
                       left = 'ss1_l',
                       right = 'ss1_r',
                       bottom = 'ss1_b',
                       top = 'ss1_t',
                       opmode = '4blades',
                       pollinterval = 5,
                       maxage = 10,
                      ),

    ss2_l_mot = device('nicos.devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'motorbus6',
                       addr = 47,
                       side = 2,
                       slope = -82.3045,
                       zerosteps = 1876.5426,
                       resetpos = -20,
                       abslimits = (-25, 20),
                       timeout = 10,
                      ),
    ss2_r_mot = device('nicos.devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'motorbus6',
                       addr = 47,
                       side = 3,
                       slope = 82.3045,
                       zerosteps = 1876.5426,
                       resetpos = 20,
                       abslimits = (-20, 25),
                       timeout = 10,
                      ),
    ss2_b_mot = device('nicos.devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'motorbus6',
                       addr = 47,
                       side = 0,
                       slope = -54.25,
                       zerosteps = 1209.775,
                       resetpos = -40,
                       abslimits = (-50, 20),
                       timeout = 10,
                      ),
    ss2_t_mot = device('nicos.devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'motorbus6',
                       addr = 47,
                       side = 1,
                       slope = 54.25,
                       zerosteps = 1209.775,
                       resetpos = 40,
                       abslimits = (-20, 50),
                       timeout = 10,
                      ),

    ss2_l     = device('nicos.devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = -2.,
                       motor = 'ss2_l_mot',
                       coder = 'ss2_l_mot',
                       obs = None,
                      ),
    ss2_r     = device('nicos.devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = 2.,
                       motor = 'ss2_r_mot',
                       coder = 'ss2_r_mot',
                       obs = None,
                      ),
    ss2_b     = device('nicos.devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = -2.,
                       motor = 'ss2_b_mot',
                       coder = 'ss2_b_mot',
                       obs = None,
                      ),
    ss2_t     = device('nicos.devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = 2.,
                       motor = 'ss2_t_mot',
                       coder = 'ss2_t_mot',
                       obs = None,
                      ),

    slit2     = device('nicos.devices.generic.Slit',
                       description = 'sample slit 2',
                       left = 'ss2_l',
                       right = 'ss2_r',
                       bottom = 'ss2_b',
                       top = 'ss2_t',
                       opmode = '4blades',
                       pollinterval = 5,
                       maxage = 10,
                      ),
)
