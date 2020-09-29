#  -*- coding: utf-8 -*-

description = 'New phytron based slits'
group = 'optional'
display_order = 6

devices = dict(
    slit1_top_mot = device('nicos.devices.generic.VirtualMotor',
        description = 'Slit 1 top blade',
        abslimits = (-26, 26),
        unit = 'mm',
        lowlevel = True,
    ),
    slit1_top = device('nicos.devices.generic.Axis',
        description = 'Slit 1 top blade',
        motor = 'slit1_top_mot',
        fmtstr = '%.3f',
        precision = 0.1,
        maxage = 119,
        pollinterval = 60,
    ),
    slit1_bottom_mot = device('nicos.devices.generic.VirtualMotor',
        description = 'Slit 1 bottom blade',
        abslimits = (-26, 26),
        unit = 'mm',
        lowlevel = True,
    ),
    slit1_bottom = device('nicos.devices.generic.Axis',
        description = 'Slit 1 bottom blade',
        motor = 'slit1_bottom_mot',
        fmtstr = '%.3f',
        precision = 0.1,
        maxage = 119,
        pollinterval = 60,
    ),
    slit1_left_mot = device('nicos.devices.generic.VirtualMotor',
        description = 'Slit 1 left blade',
        abslimits = (-26, 26),
        unit = 'mm',
        lowlevel = True,
    ),
    slit1_left = device('nicos.devices.generic.Axis',
        description = 'Slit 1 left blade',
        motor = 'slit1_left_mot',
        fmtstr = '%.3f',
        precision = 0.1,
        maxage = 119,
        pollinterval = 60,
    ),
    slit1_right_mot = device('nicos.devices.generic.VirtualMotor',
        description = 'Slit 1 right blade',
        abslimits = (-26, 26),
        unit = 'mm',
        lowlevel = True,
    ),
    slit1_right = device('nicos.devices.generic.Axis',
        description = 'Slit 1 right blade',
        motor = 'slit1_right_mot',
        fmtstr = '%.3f',
        precision = 0.1,
        maxage = 119,
        pollinterval = 60,
    ),
    slit1 = device('nicos.devices.generic.Slit',
        description = 'Slit 1',
        top = 'slit1_top',
        bottom = 'slit1_bottom',
        left = 'slit1_left',
        right = 'slit1_right',
        opmode = 'offcentered',
        coordinates = 'opposite',
        maxage = 119,
        pollinterval = 60,
    ),
    slit2_top_mot = device('nicos.devices.generic.VirtualMotor',
        description = 'Slit 2 top blade',
        abslimits = (-26, 26),
        unit = 'mm',
        lowlevel = True,
    ),
    slit2_top = device('nicos.devices.generic.Axis',
        description = 'Slit 2 top blade',
        motor = 'slit2_top_mot',
        fmtstr = '%.3f',
        precision = 0.1,
        maxage = 119,
        pollinterval = 60,
    ),
    slit2_bottom_mot = device('nicos.devices.generic.VirtualMotor',
        description = 'Slit 2 bottom blade',
        abslimits = (-26, 26),
        unit = 'mm',
        lowlevel = True,
    ),
    slit2_bottom = device('nicos.devices.generic.Axis',
        description = 'Slit 2 bottom blade',
        motor = 'slit2_bottom_mot',
        fmtstr = '%.3f',
        precision = 0.1,
        maxage = 119,
        pollinterval = 60,
    ),
    slit2_left_mot = device('nicos.devices.generic.VirtualMotor',
        description = 'Slit 2 left blade',
        abslimits = (-26, 26),
        unit = 'mm',
        lowlevel = True,
    ),
    slit2_left = device('nicos.devices.generic.Axis',
        description = 'Slit 2 left blade',
        motor = 'slit2_left_mot',
        fmtstr = '%.3f',
        precision = 0.1,
        maxage = 119,
        pollinterval = 60,
    ),
    slit2_right_mot = device('nicos.devices.generic.VirtualMotor',
        description = 'Slit 2 right blade',
        abslimits = (-26, 26),
        unit = 'mm',
        lowlevel = True,
    ),
    slit2_right = device('nicos.devices.generic.Axis',
        description = 'Slit 2 right blade',
        motor = 'slit2_right_mot',
        fmtstr = '%.3f',
        precision = 0.1,
        maxage = 119,
        pollinterval = 60,
    ),
    slit2 = device('nicos.devices.generic.Slit',
        description = 'Slit 2',
        top = 'slit2_top',
        bottom = 'slit2_bottom',
        left = 'slit2_left',
        right = 'slit2_right',
        opmode = 'offcentered',
        coordinates = 'opposite',
        maxage = 119,
        pollinterval = 60,
    ),
)
