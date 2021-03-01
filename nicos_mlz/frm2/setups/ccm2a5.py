description = 'High-Tc superconducting magnet'

group = 'plugplay'

includes = ['alias_B']

tango_base = 'tango://%s:10000/box/' % setupname

devices = {
    'B_%s' % setupname: device('nicos.devices.tango.RampActuator',
        description = 'magnetic field device',
        tangodevice = tango_base + 'plc/plc_magneticfield',
        unit = 'T',
        abslimits = (-2.2, 2.2),
        precision = 0.0005,
    ),
    'B_%s_readback' % setupname: device('nicos.devices.tango.AnalogInput',
        description = 'magnetic field device',
        tangodevice = tango_base + 'plc/plc_currentmonitor',
        unit = 'T',
        fmtstr = "%.2f",
        pollinterval = 1,
    ),
    '%s_watertemp' % setupname: device('nicos.devices.tango.AnalogInput',
        description = 'Temperature of cooling water',
        tangodevice = tango_base + 'plc/plc_watertemp',
        unit = 'degC',
        fmtstr = "%.1f",
        warnlimits = (5, 45),
    ),
    '%s_waterflow' % setupname: device('nicos.devices.tango.AnalogInput',
        description = 'Flow rate of cooling water',
        tangodevice = tango_base + 'plc/waterflow',
        unit = 'l/min',
        fmtstr = "%.1f",
        warnlimits = (5, 10),
    ),
    '%s_compressor' % setupname: device('nicos.devices.tango.NamedDigitalOutput',
        description = 'Compressor for cold head',
        tangodevice = tango_base + 'plc/plc_compressor',
        mapping = dict(on=1, off=0),
    ),
    '%s_T1' % setupname: device('nicos.devices.tango.AnalogInput',
        description = 'Temperature of the first stage of the '
        'cryo-cooler',
        tangodevice = tango_base + 'hts_mss/t1',
        unit = 'K',
        warnlimits = (0, 44),
    ),
    '%s_T2' % setupname: device('nicos.devices.tango.AnalogInput',
        description = 'Temperature of the second stage of the '
        'cryo-cooler',
        tangodevice = tango_base + 'hts_mss/t2',
        unit = 'K',
        warnlimits = (0, 12),
    ),
    '%s_TA' % setupname: device('nicos.devices.tango.AnalogInput',
        description = 'Temperature of coil pack A',
        tangodevice = tango_base + 'hts_mss/t3',
        unit = 'K',
        warnlimits = (0, 20),
    ),
    '%s_TB' % setupname: device('nicos.devices.tango.AnalogInput',
        description = 'Temperature of coil pack B',
        tangodevice = tango_base + 'hts_mss/t4',
        unit = 'K',
        warnlimits = (0, 20),
    ),
}

startupcode='''
B_%s.ramp = 0.1
''' % setupname

alias_config = {
    'B': {'B_%s' % setupname: 100},
}

extended = dict(
    representative = 'B_%s' % setupname,
)
