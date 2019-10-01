description = 'B3 aperture devices'

group = 'lowlevel'

lprecision = 0.01
tango_base = 'tango://refsanshw.refsans.frm2.tum.de:10000/'

devices = dict(
    b3 = device('nicos_mlz.refsans.devices.slits.DoubleSlitSequence',
        description = 'b3 and h3 inside Samplechamber. towards TOFTOF is plus',
        fmtstr = '%.3f, %.3f',
        unit = 'mm',
        slit_r = 'b3r',
        slit_s = 'b3s',
        # nok_motor = [-1, -1],
    ),
    b3r = device('nicos_mlz.refsans.devices.slits.SingleSlit',
       description = 'b3 slit, reactor side',
       lowlevel = True,
       motor = 'b3_rm',
       nok_start = 11334.5,
       nok_end = 11334.5,
       masks = {
           'slit': 136.9795,
           'point': 136.9795,
           'gisans': 136.9795,
       },
       unit = 'mm',
    ),
    b3s = device('nicos_mlz.refsans.devices.slits.SingleSlit',
       description = 'b3 slit, sample side',
       lowlevel = True,
       motor = 'b3_sm',
       nok_start = 11334.5,
       nok_end = 11334.5,
       masks = {
           'slit': 103.3345,
           'point': 103.3345,
           'gisans': 103.3345,
       },
       unit = 'mm',
    ),
    b3_rm = device('nicos_mlz.refsans.devices.beckhoff.nok.BeckhoffMotorCab1M0x',
        description = 'tbd',
        tangodevice = tango_base + 'refsans/b3/modbus',
        address = 0x3214+3*10, # decimal 12820
        slope = -10000,
        unit = 'mm',
        abslimits = (42, 180.0),
        ruler = -200.0,
        lowlevel = True,
    ),
    b3_sm = device('nicos_mlz.refsans.devices.beckhoff.nok.BeckhoffMotorCab1M0x',
        description = 'tbd',
        tangodevice = tango_base + 'refsans/b3/modbus',
        address = 0x3214+2*10, # decimal 12820
        slope = 10000,
        unit = 'mm',
        abslimits = (22.0, 160.0),
        ruler = 0.0,
        lowlevel = True,
    ),
    h3 = device('nicos_mlz.refsans.devices.slits.DoubleSlit',
        description = 'h3 together with b3',
        fmtstr = 'open: %.3f, xpos: %.3f',
        maxheight = 80,
        unit = 'mm',
        slit_r = 'h3r',
        slit_s = 'h3s',
    ),
    h3r = device('nicos_mlz.refsans.devices.slits.SingleSlit',
        description = 'h3 blade TOFTOF',
        motor = 'h3_r',
        masks = {
            'slit':   151.0, # 115.5,
            'point':  0,
            'gisans': 0,
        },
        lowlevel = True,
        unit = 'mm',
    ),
    h3s = device('nicos_mlz.refsans.devices.slits.SingleSlit',
        description = 'h3 blade KWS',
        motor = 'h3_s',
        masks = {
            'slit':   48.0, # 83.5,
            'point':  0,
            'gisans': 0,
        },
        lowlevel = True,
        unit = 'mm',
    ),
    h3_r = device('nicos.devices.generic.Axis',
        description = 'h3, TOFTOF',
        motor = 'h3_rm',
        coder = 'h3_rm',
        # offset = 0.0,
        precision = 0.03,
        lowlevel = True,
    ),
    h3_s = device('nicos.devices.generic.Axis',
        description = 'h3, ',
        motor = 'h3_sm',
        coder = 'h3_sm',
        # offset = 0.0,
        precision = 0.03,
        lowlevel = True,
    ),
    h3_rm = device('nicos_mlz.refsans.devices.beckhoff.nok.BeckhoffMotorCab1M0x',
        description = 'tbd',
        tangodevice = tango_base + 'refsans/b3/modbus',
        address = 0x3214+0*10, # decimal 12820
        slope = -10000,
        unit = 'mm',
        # abslimits = (-193.0, 130.0),
        abslimits = (-393.0, 330.0),
        ruler = -200.0,
        lowlevel = True,
    ),
    h3_sm = device('nicos_mlz.refsans.devices.beckhoff.nok.BeckhoffMotorCab1M0x',
        description = 'tbd',
        tangodevice = tango_base + 'refsans/b3/modbus',
        address = 0x3214+1*10, # decimal 12820
        slope = 10000,
        unit = 'mm',
        abslimits = (-102.0, 170.0),
        ruler = 0.0,
        lowlevel = True,
    ),
)

alias_config = {
    'last_aperture': {'b3.height': 100},
}
