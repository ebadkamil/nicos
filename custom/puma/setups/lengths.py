#  -*- coding: utf-8 -*-

description = 'Collimation and Lengths'

group = 'lowlevel'

includes = ['system']

# !!! keep in sync with custom/puma/lib/spectro.py !!!

devices = dict(
    lsm      = device('nicos.devices.generic.ManualMove',
                      description = 'distance source - mono',
                      default = 5633,
                      unit = 'mm',
                      fmtstr = '%.0f',
                      abslimits = (5633, 5633),
                      lowlevel = True,
                     ),
    lms      = device('nicos.devices.generic.ManualMove',
                      description = 'distance mono - sample',
                      default = 2090,
                      unit = 'mm',
                      fmtstr = '%.0f',
                      abslimits = (2090, 2100),
                      lowlevel = True,
                     ),
    lsa      = device('nicos.devices.generic.ManualMove',
                      description = 'distance sample - ana',
                      default = 910,
                      unit = 'mm',
                      fmtstr = '%.0f',
                      abslimits = (880, 1180),
                      lowlevel = True,
                     ),
    lad      = device('nicos.devices.generic.ManualMove',
                      description = 'distance ana - detector',
                      default = 750,
                      unit = 'mm',
                      fmtstr = '%.0f',
                      abslimits = (750, 750),
                      lowlevel = True,
                     ),

    cb1      = device('nicos.devices.generic.ManualMove',
                      description = 'vertical divergence before mono',
                      default = 240,
                      unit = 'min',
                      fmtstr = '%6.1f',
                      abslimits = (240, 240),
                      lowlevel = True,
                     ),
    cb2      = device('nicos.devices.generic.ManualMove',
                      description = 'vertical divergence after mono',
                      default = 240,
                      unit = 'min',
                      fmtstr = '%6.1f',
                      abslimits = (240, 240),
                      lowlevel = True,
                     ),
    cb3      = device('nicos.devices.generic.ManualMove',
                      description = 'vertical divergence before ana',
                      default = 240,
                      unit = 'min',
                      fmtstr = '%6.1f',
                      abslimits = (240, 240),
                      lowlevel = True,
                     ),
    cb4      = device('nicos.devices.generic.ManualMove',
                      description = 'vertical divergence after ana',
                      default = 240,
                      unit = 'min',
                      fmtstr = '%6.1f',
                      abslimits = (240, 240),
                      lowlevel = True,
                     ),

    ca1      = device('nicos.devices.generic.ManualSwitch',
                      description = 'monochromator collimator before mono',
                      states = ['none', '20m', '40m', '60m'],
                      lowlevel = True,
                     ),
    ca2      = device('nicos.devices.generic.ManualSwitch',
                      description = 'post monochromator collimator',
                      states = ['none', '14m', '20m', '24m', '30m', '45m', '60m'],
                      lowlevel = True,
                     ),
    ca3      = device('nicos.devices.generic.ManualSwitch',
                      description = 'pre analyser collimator',
                      states = ['none', '20m', '30m', '45m', '60m', '120m'],
                      lowlevel = True,
                     ),
    ca4      = device('nicos.devices.generic.ManualSwitch',
                      description = 'post analyser collimator',
                      states = ['none', '10m', '30m', '45m', '60m'],
                      lowlevel = True,
                     ),
)
