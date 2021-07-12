description = 'The mini-chopper for YMIR'

pv_root = 'Utg-Ymir:Chop-Drv-0101:'

devices = dict(
    mini_chopper_status=device(
        'nicos.devices.epics.EpicsStringReadable',
        description='The chopper status.',
        readpv='{}Chop_Stat'.format(pv_root),
        lowlevel=True,
    ),
    mini_chopper_control=device(
        'nicos_ess.devices.epics.extensions.EpicsMappedMoveable',
        description='Used to start and stop the chopper.',
        readpv='{}Cmd'.format(pv_root),
        writepv='{}Cmd'.format(pv_root),
        requires={'level': 'admin'},
        lowlevel=True,
        mapping={'Start chopper': 6,
                 'Stop chopper': 3,
                 'Reset chopper': 1,
                 'Clear chopper': 8,
        },
    ),
    mini_chopper_speed=device(
        'nicos_ess.devices.epics.pva.EpicsAnalogMoveable',
        description='The current speed.',
        readpv='{}Spd_Stat'.format(pv_root),
        writepv='{}Spd_SP'.format(pv_root),
        abslimits=(0.0, 14),
    ),
    mini_chopper_delay=device(
        'nicos_ess.devices.epics.pva.EpicsAnalogMoveable',
        description='The current delay.',
        readpv='{}ChopDly-S'.format(pv_root),
        writepv='{}ChopDly-S'.format(pv_root),
        abslimits=(0.0, 71428571.0),
    ),
    mini_chopper=device(
        'nicos_ess.devices.epics.chopper.EssChopperController',
        description='The mini-chopper controller',
        state='mini_chopper_status',
        command='mini_chopper_control',
    ),
)
