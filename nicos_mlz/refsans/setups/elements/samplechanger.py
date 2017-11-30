description = 'Sample table devices'

group = 'optional'

nethost = 'refsanssrv.refsans.frm2'
tacodev = '//%s/test' % nethost

devices = dict(
    samplechanger = device('nicos.devices.generic.Axis',
        description = 'Samplechanger axis',
        motor = 'samplechanger_m',
        coder = 'samplechanger_m',
        precision = 0.01,
    ),
    samplechanger_m = device('nicos.devices.taco.Motor',
        description = 'Samplechanger axis motor',
        tacodevice = '%s/phytron/kanal_06' % tacodev,
        abslimits = (-.5, 400.5),
        lowlevel = True,
    ),
)
