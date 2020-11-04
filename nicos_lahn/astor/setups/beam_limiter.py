description = 'beam limiter setup'

group = 'lowlevel'

devices = dict(
    slit_top = device('nicos.devices.generic.VirtualMotor',
        description = 'slit Y axis',
        lowlevel = True,
        abslimits = (0, 150),
        unit = 'mm',
        precision = 1,
    ),
    slit_bottom = device('nicos.devices.generic.VirtualMotor',
        description = 'slit Y axis',
        lowlevel = True,
        abslimits = (0, 150),
        unit = 'mm',
        precision = 1,
    ),
    slit_left = device('nicos.devices.generic.VirtualMotor',
        description = 'slit X axis',
        lowlevel = True,
        abslimits = (0, 150),
        unit = 'mm',
        precision = 1,
    ),
    slit_right = device('nicos.devices.generic.VirtualMotor',
        description = 'slit X axis',
        lowlevel = True,
        abslimits = (0, 150),
        unit = 'mm',
        precision = 1,
    ),
    slit = device('nicos.devices.generic.Slit',
        description = 'Beam Limiter',
        top = 'slit_top',
        bottom = 'slit_bottom',
        left = 'slit_left',
        right = 'slit_right',
        opmode = 'centered',
        coordinates = 'opposite',
    ),
)
