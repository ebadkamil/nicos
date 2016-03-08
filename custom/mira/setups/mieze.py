description = 'MIEZE measurement setup'
group = 'basic'

includes = ['cascade', 'relay']
modules = ['nicos.mira.mieze']

tango_base = 'tango://mira1.mira.frm2:10000/mira/'

devices = dict(
    mieze    = device('mira.mieze.MiezeMaster',
                      description = 'master MIEZE control device',
                     ),

    amp1     = device('mira.rfcircuit.GeneratorDevice',
                      description = 'amplitude of first function generator',
                      tacodevice = '//mirasrv/mira/hp33220a_1/amp',
                      abslimits = (0, 1),
                     ),
    amp2     = device('mira.rfcircuit.GeneratorDevice',
                      description = 'amplitude of second function generator',
                      tacodevice = '//mirasrv/mira/hp33220a_2/amp',
                      abslimits = (0, 1),
                     ),
    amp3     = device('mira.rfcircuit.GeneratorDevice',
                      description = 'amplitude of third function generator',
                      tacodevice = '//mirasrv/mira/hp33220a_3/amp',
                      warnlimits = (4.999, 5.001),
                      abslimits = (0, 5),
                     ),

    freq1    = device('mira.rfcircuit.GeneratorDevice',
                      description = 'frequency of first function generator',
                      tacodevice = '//mirasrv/mira/hp33220a_1/freq',
                      fmtstr = '%.0f',
                      abslimits = (0, 80000000),
                     ),
    freq2    = device('mira.rfcircuit.GeneratorDevice',
                      description = 'frequency of second function generator',
                      tacodevice = '//mirasrv/mira/hp33220a_2/freq',
                      fmtstr = '%.0f',
                      abslimits = (0, 80000000),
                     ),
    freq3    = device('mira.rfcircuit.GeneratorDevice',
                      description = 'frequency of third function generator',
                      tacodevice = '//mirasrv/mira/hp33220a_3/freq',
                      fmtstr = '%.0f',
                      abslimits = (0, 80000000),
                     ),

    coilamp1 = device('devices.taco.AnalogInput',
                      description = 'readout of amplitude in first RF coil',
                      tacodevice = '//mirasrv/mira/tds2014/ch1_pk2pk',
                      pollinterval = 5,
                      maxage = 6,
                     ),
    coilamp2 = device('devices.taco.AnalogInput',
                      description = 'readout of amplitude in second RF coil',
                      tacodevice = '//mirasrv/mira/tds2014/ch2_pk2pk',
                      pollinterval = 5,
                      maxage = 6,
                     ),

    rf1      = device('mira.rfcircuit.RFCurrent',
                      description = 'automatic control of current in first RF coil',
                      unit = 'V',
                      abslimits = (0, 10),
                      amplitude = 'amp1',
                      readout = 'coilamp1',
                     ),
    rf2      = device('mira.rfcircuit.RFCurrent',
                      description = 'automatic control of current in second RF coil',
                      unit = 'V',
                      abslimits = (0, 10),
                      amplitude = 'amp2',
                      readout = 'coilamp2',
                     ),

    dc1      = device('devices.tango.PowerSupply',
                      description = 'current in first DC coil',
                      tangodevice = tango_base + 'heinzinger/curr',
                      abslimits = (0, 30),
                      fmtstr = '%.2f',
                      timeout = 5,
                      precision = 0.05,
                     ),
    dc2      = device('devices.tango.PowerSupply',
                      description = 'current in second DC coil',
                      tangodevice = tango_base + 'fug/curr',
                      abslimits = (0, 30),
                      fmtstr = '%.2f',
                      timeout = 5,
                      precision = 0.05,
                     ),

    cc1      = device('devices.tango.PowerSupply',
                      description = 'current in first coupling coil',
                      tangodevice = tango_base + 'tti1/out1',
                      abslimits = (0, 2),
                      timeout = 2,
                      precision = 0.005,
                     ),
    cc2      = device('devices.tango.PowerSupply',
                      description = 'current in second coupling coil',
                      tangodevice = tango_base + 'tti1/out2',
                      abslimits = (0, 2),
                      timeout = 2,
                      precision = 0.005,
                     ),

    fp1      = device('devices.taco.AnalogInput',
                      description = 'forward power in first RF amplifier',
                      tacodevice = '//mirasrv/mira/ag1016/fp1',
                     ),
    rp1      = device('devices.taco.AnalogInput',
                      description = 'reverse power in first RF amplifier',
                      tacodevice = '//mirasrv/mira/ag1016/rp1',
                      warnlimits = (0, 20),
                     ),
    fp2      = device('devices.taco.AnalogInput',
                      description = 'forward power in second RF amplifier',
                      tacodevice = '//mirasrv/mira/ag1016/fp2',
                     ),
    rp2      = device('devices.taco.AnalogInput',
                      description = 'reverse power in second RF amplifier',
                      tacodevice = '//mirasrv/mira/ag1016/rp2',
                      warnlimits = (0, 20),
                     ),

    Cbox1    = device('mira.beckhoff.DigitalOutput',
                      description = 'first capacitor box',
                      tangodevice = tango_base + 'beckhoff/beckhoff1',
                      startoffset = 8,
                      bitwidth = 32,
                     ),
    Cbox2    = device('mira.beckhoff.DigitalOutput',
                      description = 'second capacitor box',
                      tangodevice = tango_base + 'beckhoff/beckhoff1',
                      startoffset = 40,
                      bitwidth = 32,
                     ),

)
