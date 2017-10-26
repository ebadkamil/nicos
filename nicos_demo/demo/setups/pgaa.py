description = 'virtual PGAA devices'
group = 'basic'

excludes = ['qmchannel']

sysconfig = dict(
    datasinks = ['sink']
)

devices = dict(
    Sample = device('nicos.devices.sample.Sample',
        description = 'Demo sample',
    ),
    samplerot = device('nicos.devices.generic.VirtualMotor',
        description = 'Motor to change the sample position',
        fmtstr = '%7.1f',
        abslimits = (-5, 365),
        speed = 10,
        unit = 'deg',
        lowlevel = True,
    ),
    samplemotor = device('nicos.devices.generic.MultiSwitcher',
        description = 'Sample switcher',
        moveables = ['samplerot'],
        mapping  = {1: [0.0],
                    2: [22.5],
                    3: [45.0],
                    4: [67.5],
                    5: [90.0],
                    6: [112.5],
                    7: [135.0],
                    8: [157.5],
                    9: [180.0],
                    10: [202.5],
                    11: [225.0],
                    12: [247.5],
                    13: [270.0],
                    14: [292.5],
                    15: [315.0],
                    16: [337.5],
                   },
        precision = [0.1],
        blockingmove = False,
        fmtstr = '%d',
    ),
    push = device('nicos.devices.generic.ManualSwitch',
        description = 'Push sample up and down',
        states = ['up', 'down'],
    ),
    sc = device('nicos_mlz.pgaa.devices.SampleChanger',
        description = 'The sample changer',
        motor = 'samplemotor',
        push = 'push',
    ),
    ellcol = device('nicos_mlz.pgaa.devices.BeamFocus',
        description = 'Switches between focused and collimated Beam',
        ellipse = device('nicos.devices.generic.ManualSwitch',
            states = [0, 1],
        ),
        collimator = device('nicos.devices.generic.ManualSwitch',
            states = [0, 1],
        ),
    ),
    shutter = device('nicos.devices.generic.ManualSwitch',
        description = 'secondary experiment shutter',
        states = ['open', 'closed'],
    ),
    attenuator = device('nicos_demo.demo.devices.attenuator.Attenuator',
        description = 'Attenuator',
        blades = ['att1', 'att2', 'att3'],
    ),
    att1 = device('nicos.devices.generic.ManualSwitch',
        description = 'attenuator 1',
        states = ['in', 'out'],
    ),
    att2 = device('nicos.devices.generic.ManualSwitch',
        description = 'attenuator 2',
        states = ['in', 'out'],
    ),
    att3 = device('nicos.devices.generic.ManualSwitch',
        description = 'attenuator 3',
        states = ['in', 'out'],
    ),
    att = device('nicos_mlz.pgaa.devices.Attenuator',
        description = 'Attenuator device',
        moveables = ['att1', 'att2', 'att3'],
        readables = None,
        precision = None,
        unit = '%',
        fmtstr = '%.1f',
        mapping = {100.: ('out', 'out', 'out'),
                   47.: ('out', 'in', 'out'),
                   16.: ('in', 'out', 'out'),
                   7.5: ('in', 'in', 'out'),
                   5.9: ('out', 'out', 'in'),
                   3.5: ('out', 'in', 'in'),
                   2.7: ('in', 'out', 'in'),
                   1.6: ('in', 'in', 'in'),
                  },
    ),
    chamber_pressure = device('nicos.devices.generic.VirtualMotor',
        description = 'Chamber pressure',
        jitter = 1.0,
        abslimits = (0, 1000),
        unit = 'mbar',
    ),
    truetim = device('nicos.devices.generic.VirtualTimer',
        description = 'True time timer',
        fmtstr = '%.2f',
        unit = 's',
        # lowlevel = True,
    ),
    livetim = device('nicos.devices.generic.VirtualTimer',
        description = 'Live time timer',
        fmtstr = '%.2f',
        unit = 's',
        # lowlevel = True,
    ),
    image = device('nicos_mlz.pgaa.devices.dspecdemo.Spectrum',
        description = 'Image data device',
        fmtstr = '%d',
        pollinterval = 86400,
        # lowlevel = True,
        sizes = (1, 16384),
    ),
    det = device('nicos_mlz.pgaa.devices.dspecdemo.DSPec',
        description = 'DSpec detector for high energy gamma x-rays ',
        timers = ['truetim', 'livetim'],
        monitors = [],
        counters = [],
        images = ['image'],
        pollinterval = None,
        liveinterval = 0.5,
        prefix = 'P'
    ),
    detLEGe = device('nicos_mlz.pgaa.devices.dspecdemo.DSPec',
        description = 'DSpec detector for low energy gamma x-rays',
        timers = ['truetim', 'livetim'],
        monitors = [],
        counters = [],
        images = ['image'],
        pollinterval = None,
        liveinterval = 0.5,
        prefix = 'L'
    ),
    sink = device('nicos_mlz.pgaa.devices.PGAASink',
        lowlevel = True,
        det1 = 'det',
        det2 = 'detLEGe',
        vac = 'chamber_pressure',
    ),
)

startupcode = '''
# SetDetectors(det)
SetEnvironment()
printinfo("============================================================")
printinfo("Welcome to the NICOS PGAA demo setup.")
printinfo("============================================================")
'''
