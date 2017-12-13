description = 'STRESS-SPEC setup with Newport Eulerian cradle'

group = 'basic'

includes = [
    'aliases_chiphi', 'system', 'mux', 'monochromator', 'detector',
    'sampletable', 'primaryslit', 'slits', 'reactor'
]

excludes = ['eulerian_huber', 'eulerian_tensile', 'robot']

sysconfig = dict(
    datasinks = ['caresssink'],
)

servername = 'VME'

nameservice = 'stressictrl.stressi.frm2'

devices = dict(
    chis_n = device('nicos.devices.vendor.caress.EKFMotor',
        description = 'HWB CHIN',
        fmtstr = '%.2f',
        unit = 'deg',
        coderoffset = -808.11,
        abslimits = (-1, 91),
        nameserver = '%s' % nameservice,
        objname = '%s' % servername,
        config = 'CHIN 114 11 0x00f1e000 3 20480 8000 800 2 24 50 '
                 '-1 0 1 5000 1 10 0 0 0',
        # config = 'CHIN 115 11 0x00f1e000 3 500 500 50 1 0 0 '
        #          '0 0 1 5000 1 10 0 0 0',
        lowlevel = True,
    ),
    phis_n = device('nicos.devices.vendor.caress.EKFMotor',
        description = 'HWB PHIN',
        fmtstr = '%.2f',
        unit = 'deg',
        coderoffset = 0,
        abslimits = (-720, 720),
        nameserver = '%s' % nameservice,
        objname = '%s' % servername,
        # config = 'PHIN 114 11 0x00f1c000 2 50 200 20 2 24 50 1 0 '
        #          '1 5000 1 10 0 0 0',
        config = 'PHIN 115 11 0x00f1f000 3 25 100 10 1 0 0 0 0 '
                 '1 5000 1 10 0 0 0',
        lowlevel = True,
    ),
    # phis = device('nicos.devices.vendor.caress.EKFMotor',
    #    description = 'HWB PHIS',
    #    fmtstr = '%.2f',
    #    unit = 'deg',
    #    coderoffset = 0,
    #    abslimits = (-720, 720),
    #    nameserver = '%s' % nameservice,
    #    objname = '%s' % servername,
    #    config = 'PHIS 115 11 0x00f1d000 2 100 200 20 1 0 0 0 0 '
    #             '1 5000 1 10 0 0 0',
    # ),
)

alias_config = {
    'chis': {'chis_n': 200,},
    'phis': {'phis_n': 200,},
}
