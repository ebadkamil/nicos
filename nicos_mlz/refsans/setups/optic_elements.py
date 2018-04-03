description = 'NOK Devices for REFSANS, main file including all'

group = 'lowlevel'

includes = ['nok2', 'nok3', 'nok4',
            'b1',
            'disc3', 'disc4',
            'nok5a', 'zb0',
            'nok5b', 'zb1',
            'nok6', 'zb2',
            'nok7', 'bs1',
            'nok8', 'zb3',
            'nok9',
            'sc2',
            'h2',
            'b2',
            # 'b3',
            ]

devices = dict(
    optic = device('nicos_mlz.refsans.devices.optic.Optic',
        description = 'Beam optic',
        # nok2 = 'nok2',
    ),
)