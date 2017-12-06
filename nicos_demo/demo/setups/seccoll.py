description = 'PUMA secondary collimation changer'

group = 'optional'

excludes = ['tas', 'refsans', 'sxtal', 'table']

devices = dict(
    sca1b = device('nicos_mlz.puma.devices.PumaSecCollBlockChanger',
        description = 'sca1 block changer',
        ordnum = 0,
        a2_setting = 'a2_set',
        a2_status = 'a2_status',
    ),
    sca1 = device('nicos_mlz.puma.devices.PumaSecCollLift',
        description = 'sca1 - diaphragma',
        angle = -40.000, # 68462,
        # sec = 55996070,
        tt = 'mtt',
        st = 'phi',
        block = 'sca1b',
    ),
    sca2b = device('nicos_mlz.puma.devices.PumaSecCollBlockChanger',
        description = 'sca2 block changer',
        ordnum = 1,
        a2_setting = 'a2_set',
        a2_status = 'a2_status',
    ),
    sca2 = device('nicos_mlz.puma.devices.PumaSecCollLift',
        description = 'sca2 - diaphragma cover',
        angle = -14.952, # 63902,
        # sec = 55996070,
        tt = 'mtt',
        st = 'phi',
        block = 'sca2b',
    ),
    sca3b = device('nicos_mlz.puma.devices.PumaSecCollBlockChanger',
        description = 'sca3 block changer',
        ordnum = 2,
        a2_setting = 'a2_set',
        a2_status = 'a2_status',
    ),
    sca3 = device('nicos_mlz.puma.devices.PumaSecCollLift',
        description = 'sca3 - 30 min. collimator',
        angle = -109.732, # 81156,
        stpos = 109.,
        tt = 'mtt',
        st = 'phi',
        block = 'sca3b',
    ),
    scb1b = device('nicos_mlz.puma.devices.PumaSecCollBlockChanger',
        description = 'scb1 block changer',
        ordnum = 3,
        a2_setting = 'a2_set',
        a2_status = 'a2_status',
    ),
    scb1 = device('nicos_mlz.puma.devices.PumaSecCollLift',
        description = 'scb1 - 30 min. cover',
        angle = -84.826, # 76627,
        # sec': 55996070,
        tt = 'mtt',
        st = 'phi',
        block = 'scb1b',
    ),
    scb2b = device('nicos_mlz.puma.devices.PumaSecCollBlockChanger',
        description = 'scb2 block changer',
        ordnum = 4,
        a2_setting = 'a2_set',
        a2_status = 'a2_status',
    ),
    scb2 = device('nicos_mlz.puma.devices.PumaSecCollLift',
        description = 'scb2 - 45 min. collimator',
        angle = -97.305, # 13358,
        stpos = 109.,
        # sec': 55996070,
        tt = 'mtt',
        st = 'phi',
        block = 'scb2b',
    ),
    scb3b = device('nicos_mlz.puma.devices.PumaSecCollBlockChanger',
        description = 'scb3 block changer',
        ordnum = 5,
        a2_setting = 'a2_set',
        a2_status = 'a2_status',
    ),
    scb3 = device('nicos_mlz.puma.devices.PumaSecCollLift',
        description = 'scb3 - 45 min. cover',
        angle = -69.856, # 73897,
        # sec': 55996070,
        tt = 'mtt',
        st = 'phi',
        block = 'scb3b',
    ),
    scc1b = device('nicos_mlz.puma.devices.PumaSecCollBlockChanger',
        description = 'scc1 block changer',
        ordnum = 6,
        a2_setting = 'a2_set',
        a2_status = 'a2_status',
    ),
    scc1 = device('nicos_mlz.puma.devices.PumaSecCollLift',
        description = 'scc1 - 60 min. collimator',
        angle = -52.696, # 70743,
        # sec': 55996070,
        tt = 'mtt',
        st = 'phi',
        block = 'scc1b',
    ),
    scc2b = device('nicos_mlz.puma.devices.PumaSecCollBlockChanger',
        description = 'scc2 block changer',
        ordnum = 7,
        a2_setting = 'a2_set',
        a2_status = 'a2_status',
    ),
    scc2 = device('nicos_mlz.puma.devices.PumaSecCollLift',
        description = 'scc2 - 60 min. cover',
        angle = -27.394, # 66167,
        # sec': 55996070,
        tt = 'mtt',
        st = 'phi',
        block = 'scc2b',
    ),
    a2_set = device('nicos_mlz.puma.devices.virtual.DigitalOutput',
        description = 'set of alpha2 units',
        # first = 0,
        # last = 7,
    ),
    a2_status = device('nicos_mlz.puma.devices.virtual.LogoFeedBack',
        description = 'status of alpha2 units',
        input = 'a2_set',
        # first = 0,
        # last = 15,
    ),
    a2_lgon = device('nicos_mlz.puma.devices.virtual.DigitalOutput',
        description = 'switch on/off logos',
        # first = 6,
        # last = 6,
    ),
    a2_valon = device('nicos_mlz.puma.devices.virtual.DigitalOutput',
        description = 'switch on/off power of valve unit',
        # first = 7,
        # last = 7,
    ),
    a2_press = device('nicos_mlz.puma.devices.virtual.DigitalOutput',
        description = 'switch on/off pressure for valve unit',
        # first = 0,
        # last = 0,
    ),
    mtt = device('nicos.devices.generic.VirtualMotor',
        description  = 'Monochromator Two Theta',
        unit = 'deg',
        abslimits = (-110.1, -14.1),
    ),
    phi = device('nicos.devices.generic.VirtualMotor',
        description = 'Sample scattering angle Two Theta',
        unit = 'deg',
        abslimits = (-5, 116.1),
        userlimits = (9, 115),
    ),
    scpair1 = device('nicos_mlz.puma.devices.PumaSecCollPair',
        description = 'scpair1 - 200mm collimator',
        cover = 'scb1',
        frame = 'sca3',
        a2_press = 'a2_press',
        a2_lgon = 'a2_lgon',
        a2_powvalunit = 'a2_valon',
    ),
    scpair2 = device('nicos_mlz.puma.devices.PumaSecCollPair',
        description = 'scpair2 - 150mm collimator',
        cover = 'scb3',
        frame = 'scb2',
        a2_press = 'a2_press',
        a2_lgon = 'a2_lgon',
        a2_powvalunit = 'a2_valon',
    ),
    scpair3 = device('nicos_mlz.puma.devices.PumaSecCollPair',
        description = 'scpair3 - 100 collimator',
        cover = 'scc2',
        frame = 'scc1',
        a2_press = 'a2_press',
        a2_lgon = 'a2_lgon',
        a2_powvalunit = 'a2_valon',
    ),
    a2dia = device('nicos_mlz.puma.devices.PumaSecCollPair',
        description = 'a2dia - diaphragma',
        cover = 'sca2',
        frame = 'sca1',
        a2_press = 'a2_press',
        a2_lgon = 'a2_lgon',
        a2_powvalunit = 'a2_valon',
    ),
    alpha2 = device('nicos_mlz.puma.devices.PumaSecondaryCollimator',
        description = 'alpha2 - secondary collimator',
        diaphragma = 'a2dia',
        pair1 = 'scpair1',
        pair2 = 'scpair2',
        pair3 = 'scpair3',
        a2_status = 'a2_status',
        unit = 'min.',
        fmtstr = '%d',
    ),
)
