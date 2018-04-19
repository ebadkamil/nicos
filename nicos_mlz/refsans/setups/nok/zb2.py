description = "SingleSlit [slit k1] between nok6 and nok7"

group = 'lowlevel'

includes = ['nok_ref', 'nokbus2']
global_values = configdata('global.GLOBAL_Values')

nethost = 'refsanssrv.refsans.frm2'

devices = dict(
    # masks:
    # Debug (slit)
    # Debug (k1)
    zb2 = device('nicos_mlz.refsans.devices.slits.SingleSlit',
        description = 'zb2 singel Slit at nok6 before nok7',
        unit = 'mm',
        motor = 'zb2_motor',
        # coder = 'zb2_motor',
        # obs = ['zb2_obs'],
        nok_start = 7591.5,
        nok_length = 6.0,
        nok_end = 7597.5,
        nok_gap = 1.0,
        offset = 0.0,
        # nok_motor = 7597.5,
        masks = {
            'slit':     -2,
            'point':   -2,
            'gisans':    -122.0,
        },
        # backlash = -2,   # is this configured somewhere?
        # precision = 0.05,
    ),
    zb2_mode = device('nicos.devices.generic.ReadonlyParamDevice',
        description = 'zb2 mode',
        device = 'zb2',
        parameter = 'mode',
    ),
    # generated from global/inf/resources.inf, geometrie.inf, optic.inf and taco *.res files
    zb2_motor = device('nicos_mlz.refsans.devices.nok_support.NOKMotorIPC',
        description = 'IPC controlled Motor of ZB2',
        abslimits = (-681.9525, 568.04625),
        userlimits = (-215.69, 93.0),
        bus = 'nokbus2',     # from ipcsms_*.res
        addr = 0x47,     # from resources.inf
        slope = 800.0,   # FULL steps per physical unit
        speed = 50,
        accel = 50,
        confbyte = 32,
        ramptype = 2,
        microstep = 1,
        refpos = 68.0465,    # from ipcsms_*.res
        zerosteps = int(681.95 * 800),   # offset * slope
        lowlevel = global_values['hide_poti'],
    ),

    # generated from global/inf/poti_tracing.inf
    zb2_obs = device('nicos_mlz.refsans.devices.nok_support.NOKPosition',
        description = 'Position sensing for ZB2',
        reference = 'nok_refb2',
        measure = 'zb2_poti',
        poly = [-111.898256, 999.872 / 1.921],   # off, mul * 1000 / sensitivity, higher orders...
        serial = 7786,
        length = 500.0,
        lowlevel = global_values['hide_poti'],
    ),

    zb2_acc = device('nicos_mlz.refsans.devices.nok_support.MotorEncoderDifference',
         description = 'calc error Motor and poti',
         motor = 'zb2_motor',
         analog = 'zb2_obs',
         lowlevel = global_values['hide_acc'],
         unit = 'mm'
    ),

    # generated from global/inf/poti_tracing.inf
    zb2_poti = device('nicos_mlz.refsans.devices.nok_support.NOKMonitoredVoltage',
        description = 'Poti for ZB2',
        tacodevice = '//%s/test/wb_b/2_3' % nethost,
        scale = -1,  # mounted from top
        lowlevel = True,
    ),
)
