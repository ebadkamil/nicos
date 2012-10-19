description = 'MIRA2 monochromator'
group = 'lowlevel'

includes = ['base', 'mslit2']

devices = dict(
    m2tt     = device('nicos.taco.HoveringAxis',
                      description = 'monochromator two-theta',
                      tacodevice = 'mira/axis/m2tt',
                      abslimits = (-170, -20),
                      startdelay = 1,
                      stopdelay = 3,
                      backlash = 1,
                      speed = 0.25,
                      switch = 'air_mono_sample_ana',
                      switchvalues = (0, 1),
                      fmtstr = '%.2f'),

    m2th     = device('nicos.taco.Axis',
                      description = 'monochromator theta',
                      tacodevice = 'mira/axis/m2th',
                      abslimits = (-54, -31),
                      fmtstr = '%.3f'),

    mono     = device('nicos.tas.Monochromator',
                      unit = 'A-1',
                      theta = 'm2th',
                      twotheta = 'm2tt',
                      focush = None,
                      focusv = None,
                      abslimits = (0, 10),
                      scatteringsense = -1,
                      dvalue = 3.355),

    m2tx     = device('nicos.taco.Axis',
                      tacodevice = 'mira/axis/m2tx',
                      abslimits = (-12.5, 10),
                      fmtstr = '%.2f'),
    m2ty     = device('nicos.taco.Axis',
                      tacodevice = 'mira/axis/m2ty',
                      abslimits = (-14.9, 9.9),
                      fmtstr = '%.2f'),
    m2gx     = device('nicos.taco.Axis',
                      tacodevice = 'mira/axis/m2gx',
                      abslimits = (-1, 1),
                      fmtstr = '%.2f'),
    m2fv     = device('nicos.taco.Axis',
                      description = 'monochromator vertical focus',
                      tacodevice = 'mira/axis/m2fv',
                      abslimits = (-360, 360),
                      fmtstr = '%.2f'),
    PBe      = device('nicos.mira.varian.VarianPump',
                      description = 'Be filter pressure',
                      tacodevice = 'mira/network/rs10_3',
                      fmtstr = '%.2g',
                      unit = 'mbar'),
    TBe      = device('nicos.taco.TemperatureSensor',
                      description = 'Sensor D: Be filter temperature',
                      tacodevice = 'mira/ls340/d',
                      pollinterval = 3,
                      maxage = 5,
                      fmtstr = '%.1f'),
)
