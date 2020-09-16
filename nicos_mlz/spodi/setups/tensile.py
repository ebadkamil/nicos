description = 'Tensile machine (CORBA) setup'

group = 'optional'

nameservice = 'spodictrl.spodi.frm2'

devices = dict(
    tepos = device('nicos.devices.vendor.caress.Motor',
        description = 'HWB TEPOS',
        fmtstr = '%.2f',
        unit = 'mm',
        coderoffset = 0,
        abslimits = (-20, 50),
        nameserver = '%s' % nameservice,
        config = 'TEPOS 500 TensilePos.ControllableDevice',
        absdev = False,
    ),
    teload = device('nicos.devices.vendor.caress.Motor',
        description = 'HWB TELOAD',
        fmtstr = '%.2f',
        unit = 'kN',
        coderoffset = 0,
        abslimits = (-50000, 50000),
        nameserver = '%s' % nameservice,
        config = 'TELOAD 500 TensileLoad.ControllableDevice',
        absdev = False,
    ),
    teext = device('nicos.devices.vendor.caress.Motor',
        description = 'HWB TEEXT',
        fmtstr = '%.2f',
        unit = 'um',
        coderoffset = 0,
        abslimits = (-1000, 3000),
        nameserver = '%s' % nameservice,
        config = 'TEEXT 500 TensileExt.ControllableDevice',
        absdev = False,
    ),
    topos = device('nicos.devices.vendor.caress.Motor',
        description = 'HWB TOPOS',
        fmtstr = '%.2f',
        unit = 'deg',
        coderoffset = 0,
        abslimits = (-360, 360),
        nameserver = '%s' % nameservice,
        config = 'TOPOS 500 TorsionPos.ControllableDevice',
        absdev = False,
    ),
    tomom = device('nicos.devices.vendor.caress.Motor',
        description = 'HWB TOMOM',
        fmtstr = '%.2f',
        unit = 'kNm',
        coderoffset = 0,
        abslimits = (1000, 1000),
        nameserver = '%s' % nameservice,
        config = 'TOMOM 500 TorsionMom.ControllableDevice',
        absdev = False,
    ),
    chit = device('nicos.devices.vendor.caress.EKFMotor',
        description = 'HWB CHIT',
        fmtstr = '%.2f',
        unit = 'deg',
        coderoffset = 0,
        abslimits = (-180, 180),
        nameserver = '%s' % nameservice,
        objname = 'VMESPODI',
        config = 'CHIT 115 11 0x00f1d000 1 22500 6000 50 1 0 0 '
                 '1 0 1 3000 1 10 0 0 0',
        absdev = False,
    ),
)
