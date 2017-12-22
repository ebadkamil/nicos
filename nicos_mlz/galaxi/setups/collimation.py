# -*- coding: utf-8 -*-

description = 'GALAXI motors'

group = 'optional'

tango_base = 'tango://localhost:10000/galaxi/'

devices = dict(
    b1h = device('nicos_mlz.dns.devices.motor.Motor',
        description = 'Collimation slit B1 Height',
        tangodevice = tango_base + 'fzjs7/B1H',
        precision = 0.01,
    ),
    b1b = device('nicos_mlz.dns.devices.motor.Motor',
        description = 'Collimation slit B1 Width',
        tangodevice = tango_base + 'fzjs7/B1B',
        precision = 0.01,
    ),
    b1 = device('nicos.devices.generic.TwoAxisSlit',
        description = 'Slit b1 width and hight',
        pollinterval = 10,
        maxage = 61,
        fmtstr = '%.2f %.2f',
        horizontal = 'b1b',
        vertical = 'b1h',
    ),
    b1y = device('nicos_mlz.dns.devices.motor.Motor',
        description = 'Collimation slit B1 Left Right',
        tangodevice = tango_base + 'fzjs7/B1Y',
        precision = 0.01,
    ),
    b1z = device('nicos_mlz.dns.devices.motor.Motor',
        description = 'Collimation slit B1 Up Down',
        tangodevice = tango_base + 'fzjs7/B1Z',
        precision = 0.01,
    ),
    b2h = device('nicos_mlz.dns.devices.motor.Motor',
        description = 'Collimation slit B2 Height',
        tangodevice = tango_base + 'fzjs7/B2H',
        precision = 0.01,
    ),
    b2b = device('nicos_mlz.dns.devices.motor.Motor',
        description = 'Collimation slit B2 Width',
        tangodevice = tango_base + 'fzjs7/B2B',
        precision = 0.01,
    ),
    b2 = device('nicos.devices.generic.TwoAxisSlit',
        description = 'Slit b2 width and hight',
        pollinterval = 10,
        maxage = 61,
        fmtstr = '%.2f %.2f',
        horizontal = 'b2b',
        vertical = 'b2h',
    ),
    b2y = device('nicos_mlz.dns.devices.motor.Motor',
        description = 'Collimation slit B2 Left Right',
        tangodevice = tango_base + 'fzjs7/B2Y',
        precision = 0.01,
    ),
    b2z = device('nicos_mlz.dns.devices.motor.Motor',
        description = 'Collimation slit B2 Up Down',
        tangodevice = tango_base + 'fzjs7/B2Z',
        precision = 0.01,
    ),
    b3h = device('nicos_mlz.dns.devices.motor.Motor',
        description = 'Collimation slit B3 Height',
        tangodevice = tango_base + 'fzjs7/B3H',
        precision = 0.01,
    ),
    b3b = device('nicos_mlz.dns.devices.motor.Motor',
        description = 'Collimation slit B3 Width',
        tangodevice = tango_base + 'fzjs7/B3B',
        precision = 0.01,
    ),
    b3 = device('nicos.devices.generic.TwoAxisSlit',
        description = 'Slit b3 width and hight',
        pollinterval = 10,
        maxage = 61,
        fmtstr = '%.2f %.2f',
        horizontal = 'b3b',
        vertical = 'b3h',
    ),
    b3y = device('nicos_mlz.dns.devices.motor.Motor',
        description = 'Collimation slit B3 Left Right',
        tangodevice = tango_base + 'fzjs7/B3Y',
        precision = 0.01,
    ),
    b3z = device('nicos_mlz.dns.devices.motor.Motor',
        description = 'Collimation slit B3 Up Down',
        tangodevice = tango_base + 'fzjs7/B3Z',
        precision = 0.01,
    ),
)
