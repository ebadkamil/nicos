description = 'Actuators and feedback of the shutter, detector, and valves'

groupt = 'lowlevel'

tangobase = 'tango://localhost:10000/box/'

devices = dict(
    I1_pnCCD_Active = device('nicos.devices.tango.DigitalInput',
        description = 'high: Detector is turned on',
        tangodevice = tangobase + 'IOCard/Input1',
    ),
    I2_Shutter_safe = device('nicos.devices.tango.DigitalInput',
        description = 'high: safe for opening the shutter',
        tangodevice = tangobase + 'IOCard/Input2',
    ),
    I3_Det_chamber_vent_open = device('nicos.devices.tango.DigitalInput',
        description = 'high: Detector Chamber venting gauge open',
        tangodevice = tangobase + 'IOCard/Input3',
    ),
    I4_Exp_ch_vent_open = device('nicos.devices.tango.DigitalInput',
        description = 'high: Experiment Chamber venting gauge open',
        tangodevice = tangobase + 'IOCard/Input4',
    ),
    I5_Det_ch_pump_open = device('nicos.devices.tango.DigitalInput',
        description = 'high: Detector Chamber pumping gauge open',
        tangodevice = tangobase + 'IOCard/Input5',
    ),
    I6_Exp_ch_pump_open  = device('nicos.devices.tango.DigitalInput',
        description = 'high: Experiment Chamber pumping gauge open',
        tangodevice = tangobase + 'IOCard/Input6',
    ),
    I7_Exp_ch_vent_gas_selection = device('nicos.devices.tango.DigitalInput',
        description = 'Venting either with air or nitrogen',
        tangodevice = tangobase + 'IOCard/Input7',
    ),
    I8_unused = device('nicos.devices.tango.DigitalInput',
        description = '1 Bit wide digital input starting at E8',
        tangodevice = tangobase + 'IOCard/Input8',
    ),
    O1_pnCCD_Trigger = device('nicos.devices.tango.DigitalOutput',
        description = 'Send Trigger to detector to start collecting data',
        tangodevice = tangobase + 'IOCard/Output1',
    ),
    O2_Shutter_open = device('nicos.devices.tango.DigitalOutput',
        description = 'Open the shutter from LMJ',
        tangodevice = tangobase + 'IOCard/Output2',
    ),
    O3_Det_ch_vent = device('nicos.devices.tango.DigitalOutput',
        description = 'Vent Detector Chamber',
        tangodevice = tangobase + 'IOCard/Output3',
    ),
    O4_Exp_ch_vent= device('nicos.devices.tango.DigitalOutput',
        description = 'Vent Experiment Chamber',
        tangodevice = tangobase + 'IOCard/Output4',
    ),
    O5_Det_ch_pump = device('nicos.devices.tango.DigitalOutput',
        description = 'Open gauge from pump to Detector Chamber',
        tangodevice = tangobase + 'IOCard/Output5',
    ),
    O6_Exp_ch_pump = device('nicos.devices.tango.DigitalOutput',
        description = 'Open gauge from pump to Experiment Chamber',
        tangodevice = tangobase + 'IOCard/Output6',
    ),
    O7_Exp_ch_vent_gas = device('nicos.devices.tango.DigitalOutput',
        description = 'Choose either air or Nitrogen for venting',
        tangodevice = tangobase + 'IOCard/Output7',
    ),
    O8_unused = device('nicos.devices.tango.DigitalOutput',
        description = '1 Bit wide digital output starting at A8',
        tangodevice = tangobase + 'IOCard/Output8',
    ),
)
