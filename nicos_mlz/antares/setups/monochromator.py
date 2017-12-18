description = 'Double Crystal Monochromator'

group = 'optional'

includes = []

tango_base = 'tango://antareshw.antares.frm2:10000/antares/'

devices = dict(
    mono = device('nicos_mlz.antares.devices.monochromator.Monochromator',
        description = 'ANTARES PG Double Crystal Monochromator',
        dvalue1 = 3.354,
        dvalue2 = 3.354,
        distance = 97,
        phi1 = 'mr1',
        phi2 = 'mr2',
        translation = 'mtz',
        inout = 'mono_inout',
        abslimits = (1.4, 6.5),
        userlimits = (1.4, 6.5),
        maxage = 5,
        pollinterval = 3,
        parkingpos = {
            'phi1': 12,
            'phi2': 12,
            'translation': -50,
            'inout': 'out'
        },
    ),
    mr1 = device('nicos.devices.taco.Motor',
        description = 'Rotation of first monochromator crystal',
        tacodevice = 'antares/copley/m11',
        speed = 5,
        unit = 'deg',
        abslimits = (12, 66),
        maxage = 5,
        pollinterval = 3,
        lowlevel = True,
        precision = 0.01
    ),
    mr2 = device('nicos.devices.taco.Motor',
        description = 'Rotation of second monochromator crystal',
        tacodevice = 'antares/copley/m12',
        speed = 5,
        unit = 'deg',
        abslimits = (12, 66),
        maxage = 5,
        pollinterval = 3,
        lowlevel = True,
        precision = 0.01
    ),
    mtz = device('nicos.devices.taco.Motor',
        description = 'Translation of second monochromator crystal',
        tacodevice = 'antares/copley/m13',
        speed = 5,
        unit = 'mm',
        abslimits = (-120, 260),
        userlimits = (-120, 260),
        maxage = 5,
        pollinterval = 3,
        lowlevel = True,
        precision = 0.01
    ),
    mono_io = device('nicos.devices.tango.DigitalOutput',
        description = 'Moves Monochromator in and out of beam',
        tangodevice = tango_base + 'fzjdp_digital/Monochromator',
        unit = '',
        maxage = 5,
        pollinterval = 3,
        lowlevel = True,
    ),
    mono_inout = device('nicos.devices.generic.Switcher',
        description = 'Moves Monochromator in and out of beam',
        moveable = 'mono_io',
        mapping = {'in': 1,
                   'out': 2},
        fallback = '<undefined>',
        unit = '',
        maxage = 5,
        pollinterval = 3,
        precision = 0,
        lowlevel = True,
    ),
    monoswitch_io = device('nicos.devices.tango.DigitalOutput',
        description = 'Tango device for Monoswitch in/out',
        tangodevice = tango_base + 'fzjdp_digital/Monochromator',
        lowlevel = True,
    ),
    monoswitch = device('nicos.devices.generic.Switcher',
        description = 'Monochromator switch in/out',
        moveable = 'monoswitch_io',
        mapping = {'in': 1,
                   'out': 2},
        fallback = '<undefined>',
        precision = 0,
    ),
)
