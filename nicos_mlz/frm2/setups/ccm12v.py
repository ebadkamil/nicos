description = 'setup for Oxford 12T recondensing magnet'

group = 'plugplay'
tango_base = 'tango://ccm12v:10000/box/'

includes = ['alias_T', 'alias_B', 'alias_sth']

devices = dict(
    sth_ccm12v = device('nicos_mlz.jcns.devices.motor.InvertableMotor',
        description = 'sample rotation motor',
        tangodevice = tango_base + 'motor/motx',
        fmtstr = '%.3f',
        precision = 0.002,
    ),
    T_ccm12v_vti = device('nicos.devices.tango.TemperatureController',
        description = 'temperature control of the VTI',
        tangodevice = tango_base + 'itc/vti_ctrl',
    ),
    T_ccm12v_nv = device('nicos.devices.tango.TemperatureController',
        description = 'control of the needle valve opening',
        tangodevice = tango_base + 'itc/nv_ctrl',
    ),
    T_ccm12v_stick = device('nicos.devices.tango.TemperatureController',
        description = 'temperature control of the sample stick',
        tangodevice = tango_base + 'itc/stick_ctrl',
    ),
    ccm12v_vti_heater = device('nicos.devices.tango.AnalogOutput',
        description = 'heater setting for VTI',
        tangodevice = tango_base + 'itc/vti_heater',
    ),
    ccm12v_vti_nv = device('nicos.devices.tango.AnalogOutput',
        description = 'needle valve opening for VTI',
        tangodevice = tango_base + 'itc/needlevalve',
    ),
    ccm12v_nv_heater = device('nicos.devices.tango.AnalogOutput',
        description = 'heater setting for VTI',
        tangodevice = tango_base + 'itc/nv_heater',
    ),
    B_ccm12v = device('nicos.devices.tango.Actuator',
        description = 'magnetic field',
        tangodevice = tango_base + 'ips/field',
        precision = 0.001,
    ),
    I_ccm12v_supply = device('nicos.devices.tango.AnalogInput',
        description = 'actual current output of power supplies',
        tangodevice = tango_base + 'ips/current',
    ),
    ccm12v_Tmag = device('nicos.devices.tango.Sensor',
        description = 'temperature of magnet coils',
        tangodevice = tango_base + 'ips/temp',
    ),
    ccm12v_Tpt1 = device('nicos.devices.tango.Sensor',
        description = 'temperature of pt1',
        tangodevice = tango_base + 'ips/pt1_temp',
    ),
    ccm12v_Tpt2 = device('nicos.devices.tango.Sensor',
        description = 'temperature of pt2',
        tangodevice = tango_base + 'ips/pt2_temp',
    ),
    ccm12v_pdewar = device('nicos.devices.tango.TemperatureController',
        description = 'He pressure in dewar',
        tangodevice = tango_base + 'itc/condenser_pressure',
    ),
    ccm12v_pdewar_heater = device('nicos.devices.generic.paramdev.ReadonlyParamDevice',
        description = 'heater output (in %) for dewar heating',
        device = 'ccm12v_pdewar',
        parameter = 'heateroutput',
    ),
    ccm12v_Precon = device('nicos.devices.tango.Sensor',
        description = 'Power applied at recondenser in W',
        tangodevice = tango_base + 'itc/recon_pwr',
    ),
    ccm12v_LHe = device('nicos.devices.tango.Sensor',
        description = 'liquid helium level',
        tangodevice = tango_base + 'ips/level',
    ),
)

alias_config = {
    'T': {'T_ccm12v_vti': 220, 'T_ccm12v_stick': 210},
    'Ts': {'T_ccm12v_stick': 120},
    'B': {'B_ccm12v': 100},
    'sth': {'sth_ccm12v': 200},
}

extended = dict(
    representative = 'B_ccm12v',
)