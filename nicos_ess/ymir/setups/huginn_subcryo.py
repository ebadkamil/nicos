description = 'The Huginn sub cryostat.'

pv_root = 'Huginn:'
pv_root_ls = 'Huginn_LS:'

devices = dict(
    subcryo_state=device(
        'nicos_ess.devices.epics.extensions.EpicsMappedMoveable',
        description='Turn the sub cryo on or off',
        readpv='{}SUBCRYO_ONOFF'.format(pv_root),
        writepv='{}SUBCRYO_ONOFF_S'.format(pv_root),
        mapping={'Off': 0,
                 'On': 1},
        ),
    T_subcryo_setpoint=device(
        'nicos.devices.epics.EpicsAnalogMoveable',
        description='The setpoint for the sub cryo',
        readpv='{}SUBCRYO_SETP'.format(pv_root),
        writepv='{}SUBCRYO_SETP_S'.format(pv_root),
        abslimits=(0.0, 400),
        ),
    T_maincryo_setpoint=device(
        'nicos.devices.epics.EpicsAnalogMoveable',
        description='The setpoint for the main cryo',
        readpv='{}MAINCRYO_SETP'.format(pv_root),
        writepv='{}MAINCRYO_SETP'.format(pv_root),
        abslimits=(0.0, 400),
        ),
    T_sample=device('nicos.devices.epics.EpicsReadable',
        description='The sample temperature',
        readpv='{}KRDG2'.format(pv_root_ls),
        ),
    T_base=device('nicos.devices.epics.EpicsReadable',
        description='The base temperature',
        readpv='{}KRDG3'.format(pv_root_ls),
        ),
    T_peltier_top=device('nicos.devices.epics.EpicsReadable',
        description='The top peltier temperature',
        readpv='{}KRDG0'.format(pv_root_ls),
        ),
    T_peltier_bottom=device('nicos.devices.epics.EpicsReadable',
        description='The bottom peltier temperature',
        readpv='{}KRDG1'.format(pv_root_ls),
        ),
    subcryo_mode=device(
        'nicos_ess.devices.epics.extensions.EpicsMappedMoveable',
        description='The mode for the sub cryo',
        readpv='{}SUBCRYO_MODE'.format(pv_root),
        writepv='{}SUBCRYO_MODE_S'.format(pv_root),
        lowlevel=True,
        mapping={'Manual': 0,
                 'Auto': 1},
        ),
    server_status=device('nicos.devices.epics.EpicsReadable',
        description='The status of the MatLab server',
        readpv='{}MATLAB_SERVER_STATUS'.format(pv_root),
        lowlevel=True,
        ),
    T_subcryo_setpoint_min=device(
        'nicos.devices.epics.EpicsReadable',
        description='The minimum value for the setpoint',
        readpv='{}SUBCRYO_SETP_MIN'.format(pv_root),
        lowlevel=True,
        ),
    T_subcryo_setpoint_max=device(
        'nicos.devices.epics.EpicsReadable',
        description='The maximum value for the setpoint',
        readpv='{}SUBCRYO_SETP_MAX'.format(pv_root),
        lowlevel=True,
        ),
    subcryo_status=device('nicos.devices.epics.EpicsReadable',
        description='The status of the sub cryo',
        readpv='{}SUBCRYO_STATUS'.format(pv_root),
        lowlevel=True,
        ),
)
