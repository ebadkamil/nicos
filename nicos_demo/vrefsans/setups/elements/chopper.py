description = 'Emulation of the hardware chopper'

group = 'optional'

includes = ['shutter']

devices = dict(
    chopper = device('nicos_mlz.refsans.devices.chopper.base.ChopperMaster',
        description = 'Interface',
        fmtstr = '%s',
        unit = '',
        chopper1 = 'chopper_speed',
        chopper2 = 'chopper2',
        chopper3 = 'chopper3',
        chopper4 = 'chopper4',
        chopper5 = 'chopper5',
        chopper6 = 'chopper6',
        shutter = 'shutter',
        wlmin = 3,
        wlmax = 21,
        dist = 22.8,
    ),
    chopper_speed = device('nicos_mlz.refsans.devices.chopper.virtual.ChopperDisc1',
        description = 'MC chopper_disk1',
        chopper = 1,
        edge = 'open',
        gear = 1,  # in REFSANS 0 ??
        discs = ['chopper2', 'chopper3', 'chopper4', 'chopper5', 'chopper6'],
    ),
    chopper2 = device('nicos_mlz.refsans.devices.chopper.virtual.ChopperDisc2',
        description = 'MC chopper_disk2',
        chopper = 2,
        gear = 1,
        edge = 'close',
        translation = 'chopper2_pos',
    ),
    chopper2_pos = device('nicos_mlz.refsans.devices.chopper.virtual.ChopperDiscTranslation',
        description = 'position of chopper disc 2',
        # Normally the chopper1 device of chopper should be used, but this
        # creates cyclic dependencies, which couldn't solved during the
        # shutdown !
        disc = 'chopper3',
        curvalue = 5,
    ),
    chopper3 = device('nicos_mlz.refsans.devices.chopper.virtual.ChopperDisc',
        description = 'MC chopper_disk3',
        chopper = 3,
        gear = 1,
        edge = 'open',
    ),
    chopper4 = device('nicos_mlz.refsans.devices.chopper.virtual.ChopperDisc',
        description = 'MC chopper_disk4',
        chopper = 4,
        gear = 1,
        edge = 'close',
    ),
    chopper5 = device('nicos_mlz.refsans.devices.chopper.virtual.ChopperDisc',
        description = 'sc2 chopper_disk5 gear=2',
        chopper = 5,
        gear = 2,
        edge = 'open',
    ),
    chopper6 = device('nicos_mlz.refsans.devices.chopper.virtual.ChopperDisc',
        description = 'sc2 chopper_disk6 gear=2',
        chopper = 6,
        gear = 2,
        edge = 'close',
    ),
)
