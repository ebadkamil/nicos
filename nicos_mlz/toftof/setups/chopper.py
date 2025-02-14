description = 'chopper setup'

group = 'lowlevel'

includes = ['choppermemograph']

tango_host = 'tango://tofhw.toftof.frm2:10000/'

devices = dict(
    ch = device('nicos_mlz.toftof.devices.chopper.Controller',
        description = 'TOFTOF chopper control device',
        io = device('nicos.devices.tango.StringIO',
            tangodevice = tango_host + 'toftof/rs232/ifchcontrol',
        ),
        speed_accuracy = 10,
        phase_accuracy = 10,
        ch5_90deg_offset = 0,
        timeout = 600,
        pollinterval = 10,
        maxage = 12,
        unit = 'rpm',
        fmtstr = '%.0f',
    ),
    chWL = device('nicos_mlz.toftof.devices.chopper.Wavelength',
        description = 'Neutron wavelength',
        chopper = 'ch',
        chdelay = 'chdelay',
        abslimits = (0.2, 16.0),
        pollinterval = 10,
        maxage = 12,
        unit = 'AA',
    ),
    chSpeed = device('nicos_mlz.toftof.devices.chopper.Speed',
        description = 'Setpoint of the chopper speed',
        chopper = 'ch',
        chdelay = 'chdelay',
        abslimits = (0, 22000.),
        pollinterval = 10,
        maxage = 12,
        fmtstr = '%.0f',
        unit = 'rpm',
    ),
    chRatio = device('nicos_mlz.toftof.devices.chopper.Ratio',
        description = 'Frame overlap ratio',
        chopper = 'ch',
        chdelay = 'chdelay',
        pollinterval = 10,
        maxage = 12,
    ),
    chCRC = device('nicos_mlz.toftof.devices.chopper.CRC',
        description = 'Chopper rotation sense (CRC=1, parallel=0)',
        requires = {'level': 'admin'},
        chopper = 'ch',
        chdelay = 'chdelay',
        pollinterval = 10,
        maxage = 12,
    ),
    chST = device('nicos_mlz.toftof.devices.chopper.SlitType',
        description = 'Chopper window; large window=0',
        requires = {'level': 'admin'},
        chopper = 'ch',
        chdelay = 'chdelay',
        pollinterval = 10,
        maxage = 12,
    ),
    chDS = device('nicos_mlz.toftof.devices.chopper.SpeedReadout',
        description = 'Speed of the disks 1 - 7',
        chopper = 'ch',
        fmtstr = '[%.0f, %.0f, %.0f, %.0f, %.0f, %.0f, %.0f]',
        pollinterval = 10,
        maxage = 12,
        unit = 'rpm',
    ),
    chdelaybus = device('nicos_mlz.toftof.devices.toni.ToniBus',
        tangodevice = tango_host + 'toftof/rs232/ifchdelay',
        lowlevel = True,
    ),
    chdelay = device('nicos_mlz.toftof.devices.toni.DelayBox',
        description = 'Trigger time-offset',
        requires = {'level': 'guest'},
        bus = 'chdelaybus',
        addr = 0xF1,
        unit = 'usec',
        fmtstr = '%d',
    ),
)
