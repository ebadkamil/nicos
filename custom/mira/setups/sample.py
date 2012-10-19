description = 'sample table'
group = 'lowlevel'

devices = dict(
    phi      = device('nicos.taco.HoveringAxis',
                      description = 'sample two-theta',
                      tacodevice = 'mira/axis/phi',
                      abslimits = (-120, 120),
                      startdelay = 1,
                      stopdelay = 2,
                      switch = 'air_sample_ana',
                      switchvalues = (0, 1),
                      fmtstr = '%.3f'),

    air_mono_sample_ana = device('nicos.taco.MultiDigitalOutput',
                        outputs = ['air_mono', 'air_sample', 'air_ana'],
                        unit = '',
                        lowlevel = True),
    air_mono   = device('nicos.taco.DigitalOutput',
                        tacodevice = 'mira/phytronio/air_mono_2',
                        lowlevel = True),

    air_sample_ana = device('nicos.taco.MultiDigitalOutput',
                        outputs = ['air_sample', 'air_ana'],
                        unit = '',
                        lowlevel = True),
    air_sample = device('nicos.mira.refcountio.RefcountDigitalOutput',
                        tacodevice = 'mira/phytronio/air_sample_2',
                        lowlevel = True),

    air_ana    = device('nicos.mira.refcountio.RefcountDigitalOutput',
                        tacodevice = 'mira/phytronio/air_temp',
                        lowlevel = True),

    om       = device('nicos.taco.Axis',
                      description = 'sample theta',
                      tacodevice = 'mira/axis/om',
                      abslimits = (-180, 180),
                      fmtstr = '%.3f'),
    stx      = device('nicos.taco.Axis',
                      description = 'sample translation along the beam',
                      tacodevice = 'mira/axis/stx',
                      abslimits = (-25, 25),
                      fmtstr = '%.2f'),
    sty      = device('nicos.taco.Axis',
                      description = 'horizontal sample translation',
                      tacodevice = 'mira/axis/sty',
                      abslimits = (-25, 25),
                      fmtstr = '%.2f'),
    stz      = device('nicos.taco.Axis',
                      description = 'vertical sample translation',
                      tacodevice = 'mira/axis/stz',
                      abslimits = (0, 40),
                      fmtstr = '%.2f'),
    sgx      = device('nicos.taco.Axis',
                      description = 'sample tilt around beam axis',
                      tacodevice = 'mira/axis/sgx',
                      abslimits = (-5, 5),
                      fmtstr = '%.2f'),
    sgy      = device('nicos.taco.Axis',
                      description = 'sample tilt orthogonal to beam axis',
                      tacodevice = 'mira/axis/sgy',
                      abslimits = (-5, 5),
                      fmtstr = '%.2f'),
)
