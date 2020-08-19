description = "neutronguide, radialcollimator"

group = 'lowlevel'

includes = ['nok_ref', 'zz_absoluts']
instrument_values = configdata('instrument.values')
showcase_values = configdata('cf_showcase.showcase_values')
optic_values = configdata('cf_optic.optic_values')

tango_base = instrument_values['tango_base']
code_base = instrument_values['code_base']

devices = dict(
    nok4 = device(code_base + 'nok_support.DoubleMotorNOK',
        # length: 1000.0 mm
        description = 'NOK4',
        fmtstr = '%.2f, %.2f',
        nok_start = 1326.0,
        nok_end = 2326.0,
        nok_gap = 1.0,
        inclinationlimits = (-40, 40),
        motor_r = 'nok4r_axis',
        motor_s = 'nok4s_axis',
        nok_motor = [1477.0, 2177.0],
        precision = 0.0,
        masks = {
            'ng': optic_values['ng'],
            'rc': optic_values['rc'],
            'vc': optic_values['ng'],
            'fc': optic_values['ng'],
        },
    ),
    nok4r_axis = device('nicos.devices.generic.Axis',
        description = 'Axis of NOK4, reactor side',
        motor = 'nok4r_motor',
        # obs = ['nok4r_analog'],
        backlash = -0.5,
        precision = optic_values['precision_ipcsms'],
        unit = 'mm',
        lowlevel = True,
    ),
    nok4r_acc = device(code_base + 'nok_support.MotorEncoderDifference',
         description = 'calc error Motor and poti',
         motor = 'nok4r_motor',
         analog = 'nok4r_analog',
         lowlevel = showcase_values['hide_acc'],
         unit = 'mm'
    ),
    nok4r_analog = device(code_base + 'nok_support.NOKPosition',
        description = 'Position sensing for NOK4, reactor side',
        reference = 'nok_refa2',
        measure = 'nok4r_poti',
        # 2020-04-26 10:15:29 poly = [36.179259, 1002.569 / 3.852],
        poly = [36.454, 1002.569 / 3.852],
        serial = 6509,
        length = 250.0,
        lowlevel = showcase_values['hide_poti'],
    ),
    nok4r_poti = device(code_base + 'nok_support.NOKMonitoredVoltage',
        description = 'Poti for NOK4, reactor side',
        tangodevice = tango_base + 'test/wb_a/2_0',
        scale = 1,   # mounted from bottom
        lowlevel = True,
    ),
    nok4s_axis = device('nicos.devices.generic.Axis',
        description = 'Axis of NOK4, sample side',
        motor = 'nok4s_motor',
        # obs = ['nok4s_analog'],
        backlash = -0.5,
        precision = optic_values['precision_ipcsms'],
        unit = 'mm',
        lowlevel = True,
    ),
    nok4s_acc = device(code_base + 'nok_support.MotorEncoderDifference',
         description = 'calc error Motor and poti',
         motor = 'nok4s_motor',
         analog = 'nok4s_analog',
         lowlevel = showcase_values['hide_acc'],
         unit = 'mm'
    ),
    nok4s_analog = device(code_base + 'nok_support.NOKPosition',
        description = 'Position sensing for NOK4, sample side',
        reference = 'nok_refa2',
        measure = 'nok4s_poti',
        # 2020-04-26 10:16:47 poly = [4.822946, 998.362 / 3.856],
        poly = [4.669, 998.362 / 3.856],
        serial = 6504,
        length = 250.0,
        lowlevel = showcase_values['hide_poti'],
    ),
    nok4s_poti = device(code_base + 'nok_support.NOKMonitoredVoltage',
        description = 'Poti for NOK4, sample side',
        tangodevice = tango_base + 'test/wb_a/2_1',
        scale = 1,   # mounted from bottom
        lowlevel = True,
    ),
)
