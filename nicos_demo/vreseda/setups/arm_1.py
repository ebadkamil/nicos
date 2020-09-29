description = 'Reseda arm 1 (NRSE)'

group = 'optional'

devices = dict(
    arm1_rot = device('nicos.devices.generic.Axis',
        description = 'Rotation arm 1',
        motor = device('nicos.devices.generic.VirtualMotor',
            abslimits = (-90, 5),
            unit = 'deg',
            speed = 5,
            curvalue = -10,
        ),
        fmtstr = '%.3f',
        precision = 0.01,
    ),
    T_arm1_coil1 = device('nicos.devices.generic.virtual.VirtualTemperature',
        description = 'Arm 1 coil 1 temperature',
        curvalue = 22,
        abslimits = (0, 60),
        unit = 'degC',
    ),
    T_arm1_coil2 = device('nicos.devices.generic.virtual.VirtualTemperature',
        description = 'Arm 1 coil 2 temperature',
        abslimits = (0, 60),
        curvalue = 22,
        unit = 'degC',
    ),
    T_arm1_coil3 = device('nicos.devices.generic.virtual.VirtualTemperature',
        description = 'Arm 1 coil 3 temperature',
        abslimits = (0, 60),
        curvalue = 22,
        unit = 'degC',
    ),
    T_arm1_coil4 = device('nicos.devices.generic.virtual.VirtualTemperature',
        description = 'Arm 1 coil 4 temperature',
        abslimits = (0, 60),
        curvalue = 22,
        unit = 'degC',
    ),
)
