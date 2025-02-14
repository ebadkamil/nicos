description = 'all values for detector positon'

group = 'lowlevel'

instrument_values = configdata('instrument.values')
showcase_values = configdata('cf_showcase.showcase_values')

tango_base = instrument_values['tango_base']
code_base = instrument_values['code_base']

devices = dict(
    primary_beam = device('nicos.devices.generic.ManualMove',
        description = 'Number of primary beam measurement for analysis',
        abslimits = (0, 100000000),
        default = 0,
        fmtstr = 'Nr %d',
        unit = '',
    ),
    det_drift = device('nicos.devices.generic.ManualSwitch',
        description = 'depth of detector drift1=40mm drift2=65mm',
        states = ['off','drift1', 'drift2'],
    ),
    hv_anode = device('nicos.devices.tango.PowerSupply',
        description = 'HV detector anode',
        tangodevice = tango_base + 'detector/anode/voltage',
        requires = {'level': 'admin'},
    ),
    hv_drift1 = device('nicos.devices.tango.PowerSupply',
        description = 'HV detector drift1',
        tangodevice = tango_base + 'detector/drift/voltage',
        requires = {'level': 'admin'},
    ),
    hv_drift2 = device('nicos.devices.tango.PowerSupply',
        description = 'HV detector drift1',
        tangodevice = tango_base + 'detector/drift2/voltage',
        requires = {'level': 'admin'},
    ),
    det_pivot = device(code_base + 'pivot.PivotPoint',
        description = 'Pivot point at floor of samplechamber',
        states = list(range(1, 15)),
        fmtstr = 'Point %d',
        unit = '',
    ),
    det_yoke_motor = device('nicos.devices.tango.Motor',
        description = 'yoke Motor',
        tangodevice = tango_base + 'test/tube/servostar',
        lowlevel = True,
    ),
    det_yoke = device('nicos.devices.generic.Axis',
        description = 'yoke height, refmove only in expertmode!',
        motor = 'det_yoke_motor',
        precision = 0.05,
        dragerror = 10.,
        fmtstr = '%.0f',
        lowlevel = False,
    ),
    det_yoke_enc_io = device('nicos.devices.tango.StringIO',
        description = 'Yoke big red: communication device',
        tangodevice = tango_base  + 'test/tube_enc/io',
        lowlevel = True,
    ),
    det_yoke_enc1 = device(code_base + 'det_yoke_enc.BasePos',
        description = 'one side',
        comm = 'det_yoke_enc_io',
        index = 1,
        lowlevel = True,
        unit = 'foo',
    ),
    det_yoke_enc2 = device(code_base + 'det_yoke_enc.BasePos',
        description = 'other side',
        comm = 'det_yoke_enc_io',
        index = 2,
        lowlevel = True,
        unit = 'foo',
    ),
    det_yoke_skew = device(code_base + 'skew_motor.SkewRead',
        description = 'SkewRead',
        one = 'det_yoke_enc1',
        two = 'det_yoke_enc2',
        lowlevel = True,
        unit = 'foo',
    ),
    det_yoke_enc = device(code_base + 'analogencoder.AnalogEncoder',
        description = 'Yoke big red: Encoder to validate position',
        device = 'det_yoke_skew',
        poly = [0, 1/(400.0*1.02543)],
        unit = 'mm',
        lowlevel = False,
    ),
    det_table_raw = device('nicos.devices.tango.Actuator',
        description = 'table inside scatteringtube mit Pluto',
        tangodevice = tango_base + 'det_table/plc/_TablePosition',
        unit = 'mm',
        userlimits = (1270, 11025), #for Cd (1140, 11025),
        lowlevel = False,
    ),
    det_table_poti = device('nicos.devices.tango.Sensor',
        description = 'Coder of detector table inside scatteringtube',
        tangodevice = tango_base + 'det_table/plc/_input_SeilzugPosition',
        unit = 'mm',
        lowlevel = False,
    ),
    det_table_cab_temp = device('nicos.devices.tango.Sensor',
        description = 'Temperature of Controller',
        tangodevice = tango_base + 'det_table/plc/_input_CabTemperature',
        unit = 'degC',
        lowlevel = False,
    ),
    det_table_motor_temp = device('nicos.devices.tango.Sensor',
        description = 'Temperature of Motorcore',
        tangodevice = tango_base + 'det_table/plc/_input_MotorTemperature',
        unit = 'degC',
        lowlevel = False,
    ),
    det_table_motor = device(code_base + 'analogencoder.AnalogMove',
        description = 'correcting error',
        device = 'det_table_raw',
        unit = 'mm',
        poly = [-211.5,  1.00460], # 2021-03-23 09:08:58 GM Laser poly = [-513.0, 0.9955], #2021-03-15 06:58:01 MP QAD Pluto 30Grad
        # poly = [-513.0, 0.9955], # 2021-03-15 06:58:01 MP QAD Pluto 30Grad
        lowlevel = False,
    ),
    det_table_acc = device(code_base + 'analog.Accuracy',
        description = 'calc error Motor and poti',
        motor = 'det_table_raw',
        analog = 'det_table_poti',
        lowlevel = showcase_values['hide_acc'],
        unit = 'mm'
    ),
    det_table = device(code_base + 'focuspoint.FocusPoint',
        description = 'detector table inside scatteringtube. with pivot',
        unit = 'mm',
        table = 'det_table_ctrl',
        pivot = 'det_pivot',
        abslimits = [1065, 10864],
    ),
    det_table_ctrl = device(code_base + 'controls.TemperatureControlled',
        description = 'MP only: to check for motor temp',
        device = 'det_table_motor',
        temperature = 'det_table_motor_temp',
        # maxtemp = 40,
        # timeout = 20,
        # precision = 2,
        unit = 'mm',
        lowlevel = False,
    ),
    dix_laser_acc = device(code_base + 'nok_support.MotorEncoderDifference',
        description = 'laser measurement of table accuracy',
        motor = 'det_table_motor',
        analog = 'dix_laser_analog',
        unit = 'mm',
    ),
    dix_laser_analog = device('nicos_mlz.refsans.devices.dimetix.DimetixLaser',
        description = 'laser measurement of table',
        signal = 'dix_laser_signalstrength',
        value = 'dix_laser_value',
        unit = 'mm',
        lowlevel = True,
    ),
    dix_laser_value = device('nicos.devices.tango.Sensor',
        description = 'laser measurement system value',
        tangodevice = tango_base + 'test/laser/value',
        lowlevel = True,
    ),
    dix_laser_signalstrength = device('nicos.devices.tango.Sensor',
        description = 'laser measurement system signal strength',
        tangodevice = tango_base + 'test/laser/signalstrength',
        unit = '',
        lowlevel = True,
    ),
    dix_laser_temperature = device('nicos.devices.tango.Sensor',
        description = 'laser measurement system temperature',
        tangodevice = tango_base + 'test/laser/temperature',
        unit = 'degC',
        lowlevel = True,
    ),
    tube_angle = device(code_base + 'tube.TubeAngle',
        description = 'Angle between flight tube and ground',
        yoke = 'det_yoke',
    ),
)
