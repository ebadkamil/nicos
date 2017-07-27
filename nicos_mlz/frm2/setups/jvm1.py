description = 'setup for JVM magnet box'

group = 'plugplay'
includes = ['alias_T']

tango_base = 'tango://jvm1:10000/box/'

devices = dict(
    vm5_piso = device('nicos.devices.tango.Sensor',
        description = 'Isolation vacuum pressure',
        tangodevice = tango_base + 'pressure/ch1',
        fmtstr = '%.3g',
    ),
    vm5_pvti = device('nicos.devices.tango.Sensor',
        description = 'VTI pressure',
        tangodevice = tango_base + 'pressure/ch2',
        fmtstr = '%.3g',
    ),
    vm5_psample = device('nicos.devices.tango.Sensor',
        description = 'Sample space pressure',
        tangodevice = tango_base + 'pressure/ch3',
        fmtstr = '%.3g',
    ),
    vm5_lhe = device('nicos.devices.tango.Sensor',
        description = 'Liquid helium level',
        tangodevice = tango_base + 'levelmeter/level',
        fmtstr = '%.0f',
        warnlimits = (40, 600),
    ),
    vm5_lhe_mode = device('nicos.devices.tango.NamedDigitalOutput',
        description = 'Readout mode of the levelmeter',
        tangodevice = tango_base + 'levelmeter/mode',
        mapping = {'standby': 0, 'slow': 1, 'fast': 2, 'continuous': 3},
        warnlimits = ('slow', 'slow'),
    ),
    T_vm5_magnet = device('nicos.devices.tango.Sensor',
        description = 'Coil temperature',
        tangodevice = tango_base + 'ls336/sensora',
        unit = 'K',
    ),
    T_vm5_vti = device('nicos.devices.tango.TemperatureController',
        description = 'VTI temperature',
        tangodevice = tango_base + 'ls336/control1',
        unit = 'K',
    ),
    T_vm5_sample = device('nicos.devices.tango.TemperatureController',
        description = 'Sample thermometer temperature',
        tangodevice = tango_base + 'ls336/control2',
        unit = 'K',
    ),
    vm5_nv_reg = device('nicos.devices.tango.TemperatureController',
        description = 'Needle valve regulation setpoint',
        tangodevice = tango_base + 'nv/regulation',
        unit = 'mbar',
    ),
    vm5_nv_manual = device('nicos.devices.tango.AnalogOutput',
        description = 'Needle valve opening',
        tangodevice = tango_base + 'ls336/control3mout',
    ),
    I_vm5 = device('nicos.devices.tango.Actuator',
        description = 'Current in the magnet',
        tangodevice = tango_base + 'supply/field',
        precision = 60,
    ),
    I_vm5_supply = device('nicos.devices.tango.Sensor',
        description = 'Current output of the power supply',
        tangodevice = tango_base + 'supply/actual',
    ),
)

alias_config = {
    'T':  {'T_vm5_vti': 200, 'T_vm5_sample': 190},
    'Ts': {'T_vm5_sample': 200, 'T_vm5_vti': 190},
}