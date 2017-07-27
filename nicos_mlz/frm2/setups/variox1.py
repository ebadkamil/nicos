description = 'Variox1 orange type cryostat with VTI'

group = 'plugplay'

includes = ['alias_T']

tango_base = 'tango://%s:10000/box/' % setupname

devices = {
    'T_%s' % setupname: device('nicos.devices.tango.TemperatureController',
                               description = 'The control temperature',
                               tangodevice = tango_base + 'itc/control',
                               unit = 'K',
                               fmtstr = '%.3f',
                               pollinterval = 1,
                               maxage = 2,
                              ),
    '%s_heater' % setupname: device('nicos.devices.tango.AnalogOutput',
                               description = 'The manual heater output',
                               tangodevice = tango_base + 'itc/manualheater',
                               unit = '%',
                               fmtstr = '%.1f',
                              ),
    '%s_control' % setupname: device('nicos.devices.tango.NamedDigitalOutput',
                               description = 'Selects which temperature to control',
                               tangodevice = tango_base + 'itc/controlchannel',
                               mapping = {'VTI': 1, 'Sample': 2},
                              ),
    'T_%s_vti' % setupname: device('nicos.devices.tango.Sensor',
                               description = 'The VTI temperature',
                               tangodevice = tango_base + 'itc/sensor1',
                               unit = 'K',
                               fmtstr = '%.3f',
                               pollinterval = 1.5,
                               maxage = 2.5,
                              ),
    'T_%s_sample' % setupname: device('nicos.devices.tango.Sensor',
                               description = 'The sample temperature',
                               tangodevice = tango_base + 'itc/sensor2',
                               unit = 'K',
                               fmtstr = '%.3f',
                               pollinterval = 1.5,
                               maxage = 2.5,
                              ),
    '%s_p' % setupname: device('nicos.devices.tango.TemperatureController',
                               description = 'Needle valve pressure regulation',
                               tangodevice = tango_base + 'lambda/reg',
                               unit = 'mbar',
                               fmtstr = '%.1f',
                               precision = 0.5,
                               pollinterval = 5,
                               maxage = 6,
                              ),
    '%s_nv' % setupname: device('nicos.devices.tango.AnalogOutput',
                                description = 'Needle valve setting',
                                tangodevice = tango_base + 'lambda/nv',
                                unit = '%',
                                fmtstr = '%.1f',
                                pollinterval = 1,
                                maxage = 2,
                               ),
    '%s_lhe_fill' % setupname: device('nicos.devices.tango.Sensor',
                                      description = 'Liquid Helium level',
                                      tangodevice = tango_base + 'ilm/lhe',
                                      unit = '%',
                                      fmtstr = '%.1f',
                                      pollinterval = 5,
                                      maxage = 6,
                                     ),
    '%s_ln2_fill' % setupname: device('nicos.devices.tango.Sensor',
                                      description = 'Liquid Nitrogen level',
                                      tangodevice = tango_base + 'ilm/ln2',
                                      unit = '%',
                                      fmtstr = '%.1f',
                                      pollinterval = 5,
                                      maxage = 6,
                                     ),
    '%s_piso' % setupname: device('nicos.devices.tango.Sensor',
                                description = 'Isolation vacuum pressure',
                                tangodevice = tango_base + 'gauge/iso',
                                unit = 'mbar',
                                fmtstr = '%.2g',
                               ),
    '%s_psample' % setupname: device('nicos.devices.tango.Sensor',
                                description = 'Sample tube pressure',
                                tangodevice = tango_base + 'gauge/sample',
                                unit = 'mbar',
                                fmtstr = '%.1f',
                               ),
    '%s_ppump' % setupname: device('nicos.devices.tango.Sensor',
                                description = 'Pressure at He pump',
                                tangodevice = tango_base + 'gauge/pump',
                                unit = 'mbar',
                                fmtstr = '%.1f',
                               ),
}

alias_config = {
    'T': {'T_%s' % setupname: 100},
    'Ts':  {'T_%s_sample' % setupname: 100, 'T_%s_vti' % setupname: 90},
}