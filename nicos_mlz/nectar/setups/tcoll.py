description = 'Thermal collimator'

group = 'optional'

tango_base = 'tango://phytron02.nectar.frm2.tum.de:10000/'

devices = dict(
    drum_c = device('nicos.devices.tango.Sensor',
        tangodevice = tango_base + 'box/channel7/enc',
        lowlevel = True,
    ),
    drum_m = device('nicos.devices.tango.Motor',
        tangodevice = tango_base + 'box/channel7/mot',
        abslimits = (-10, 370),
        precision = 0.05,
        unit = 'deg',
        lowlevel = True,
    ),
    drum = device('nicos_mlz.nectar.devices.ThermalCollimatorAxis',
        motor = 'drum_m',
        # coder = 'drum_c',  # coder not working for multiturns (Resolver)
        precision = 0.05,
        lowlevel = True,
    ),
    tcoll = device('nicos.devices.generic.Switcher',
        description = 'Thermal collimator',
        precision = 0.01,
        moveable = 'drum',
        mapping = {
            '800': 0,
            '400': 90,
            '600': 180,
            '200': 270,
        },
        fallback = '-',
        unit = 'L/D',
    ),
)
