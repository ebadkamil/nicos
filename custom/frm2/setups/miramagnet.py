description = 'MIRA 0.5 T electromagnet'
group = 'optional'

includes = ['alias_B']

devices = dict(
    I_pol    = device('devices.tango.DigitalOutput',
                      tangodevice = 'tango://miramagnet:10000/box/beckhoff/plc_polarity',
                      fmtstr = '%+d',
                      lowlevel = True,
                     ),
    I        = device('devices.tango.PowerSupply',
                      description = 'MIRA Helmholtz magnet current',
                      tangodevice = 'tango://miramagnet:10000/box/lambdaess/current',
                      abslimits = (0, 250),
                      fmtstr = '%.1f',
                     ),
    B_mira   = device('frm2.magnet.MiraMagnet',
                      currentsource = 'I',
                      switch = 'I_pol',
                      description = 'MIRA magnetic field',
                      # no abslimits: they are automatically determined from I
                      unit = 'T',
                      fmtstr = "%.4f",
                     ),
    miramagnet_T1 = device('devices.tango.AnalogInput',
                           tangodevice = 'tango://miramagnet:10000/box/beckhoff/plc_t1',
                           fmtstr = '%d',
                           warnlimits = (0, 60),
                           unit = 'degC'),
    miramagnet_T2 = device('devices.tango.AnalogInput',
                           tangodevice = 'tango://miramagnet:10000/box/beckhoff/plc_t2',
                           fmtstr = '%d',
                           warnlimits = (0, 60),
                           unit = 'degC'),
    miramagnet_T3 = device('devices.tango.AnalogInput',
                           tangodevice = 'tango://miramagnet:10000/box/beckhoff/plc_t3',
                           fmtstr = '%d',
                           warnlimits = (0, 60),
                           unit = 'degC'),
    miramagnet_T4 = device('devices.tango.AnalogInput',
                           tangodevice = 'tango://miramagnet:10000/box/beckhoff/plc_t4',
                           fmtstr = '%d',
                           warnlimits = (0, 60),
                           unit = 'degC'),
)

startupcode = '''
B.alias = B_mira
'''
