description = 'NE1002 syringe pump'

pv_root = 'E04-SEE-FLUCO:NE1002x-001:'

devices = dict(
    inside_diameter=device(
        'nicos_ess.devices.epics.pva.EpicsAnalogMoveable',
        description='The Inside diameter of the syringe',
        readpv='{}DIAMETER'.format(pv_root),
        writepv='{}SET_DIAMETER'.format(pv_root),
        epicstimeout=3.0,
        abslimits=(0.1, 50),
    ),
    pump_volume=device(
        'nicos_ess.devices.epics.pva.EpicsAnalogMoveable',
        description='The volume to be pumped',
        readpv='{}VOLUME'.format(pv_root),
        writepv='{}SET_VOLUME'.format(pv_root),
        epicstimeout=3.0,
        abslimits=(0.1, 50),
    ),
    pump_volume_units=device(
        'nicos_ess.devices.epics.pva.EpicsMappedMoveable',
        description='The volume units',
        readpv='{}VOLUME_UNITS'.format(pv_root),
        writepv='{}SET_VOLUME_UNITS'.format(pv_root),
        mapping={'μL': 0, 'mL': 1},
    ),
    pump_rate=device(
        'nicos_ess.devices.epics.pva.EpicsAnalogMoveable',
        description='The pump rate',
        readpv='{}RATE'.format(pv_root),
        writepv='{}SET_RATE'.format(pv_root),
        epicstimeout=3.0,
        abslimits=(0.1, 50),
    ),
    pump_rate_units=device(
        'nicos_ess.devices.epics.pva.EpicsMappedMoveable',
        description='The rate units',
        readpv='{}RATE_UNITS'.format(pv_root),
        writepv='{}SET_RATE_UNITS'.format(pv_root),
        mapping={'μL / min': 0, 'mL / min': 1, 'μL / hr': 2, 'mL / hr': 3},
    ),
    pump_direction=device(
        'nicos_ess.devices.epics.pva.EpicsMappedMoveable',
        description='The pump direction',
        readpv='{}DIRECTION'.format(pv_root),
        writepv='{}SET_DIRECTION'.format(pv_root),
    ),
    volume_withdrawn=device(
        'nicos_ess.devices.epics.pva.EpicsReadable',
        description='The volume withdrawn',
        readpv='{}VOLUME_WITHDRAWN'.format(pv_root),
        epicstimeout=3.0,
    ),
    volume_infused=device(
        'nicos_ess.devices.epics.pva.EpicsReadable',
        description='The volume infused',
        readpv='{}VOLUME_INFUSED'.format(pv_root),
        epicstimeout=3.0,
    ),
    pump_status=device(
        'nicos.devices.epics.EpicsReadable',
        description='The pump status',
        readpv='{}STATUS'.format(pv_root),
        lowlevel=True,
        epicstimeout=3.0,
    ),
    pump_message=device(
        'nicos_ess.devices.epics.pva.EpicsStringReadable',
        description='The pump message',
        readpv='{}MESSAGE'.format(pv_root),
        lowlevel=True,
        epicstimeout=3.0,
    ),
    start_purge=device(
        'nicos_ess.devices.epics.pva.EpicsMappedMoveable',
        description='Start purging',
        readpv='{}PURGE'.format(pv_root),
        writepv='{}PURGE'.format(pv_root),
        mapping={'OFF': 0, 'ON': 1},
    ),
    start_pumping=device(
        'nicos_ess.devices.epics.extensions.EpicsMappedMoveable',
        description='Start pumping',
        readpv='{}RUN'.format(pv_root),
        writepv='{}RUN'.format(pv_root),
        mapping={'OFF': 0, 'ON': 1},
    ),
    pause_pumping=device(
        'nicos_ess.devices.epics.extensions.EpicsMappedMoveable',
        description='Pause pumping',
        readpv='{}PAUSE'.format(pv_root),
        writepv='{}PAUSE'.format(pv_root),
        mapping={'OFF': 0, 'ON': 1},
    ),
    stop_pumping=device(
        'nicos_ess.devices.epics.pva.EpicsMappedMoveable',
        description='Stop pumping',
        readpv='{}STOP'.format(pv_root),
        writepv='{}STOP'.format(pv_root),
        mapping={'OFF': 0, 'ON': 1},
    ),
    seconds_to_pause=device(
        'nicos.devices.epics.EpicsAnalogMoveable',
        description='How long to pause for (seconds)',
        readpv='{}SET_PAUSE'.format(pv_root),
        writepv='{}SET_PAUSE'.format(pv_root),
        epicstimeout=3.0,
        abslimits=(0.1, 50),
    ),
    zero_volume_withdrawn=device(
        'nicos.devices.epics.EpicsReadable',
        description='Zero volume withdrawn and infused',
        readpv='{}CLEAR_V_DISPENSED'.format(pv_root),
        epicstimeout=3.0,
    ),
)
