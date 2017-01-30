description = 'Simulated SPODI instrument'

group = 'basic'

excludes = ['detector', 'qmchannel']

sysconfig = dict(
    instrument = 'VSPODI',
    datasinks = ['spodisink'],
)

includes = ['source']

devices = dict(
    VSPODI = device('devices.instrument.Instrument',
                    description = 'Virtual SPODI instrument',
                    responsible = 'R. Esponsible <r.esponsible@frm2.tum.de>',
                    instrument = 'V-SPODI',
                    website = 'http://www.nicos-controls.org',
                    operators = ['NICOS developer team', ],
                    facility = 'NICOS demo instruments',
                    doi = 'http://dx.doi.org/10.17815/jlsrf-1-25',
                   ),
    tths = device('devices.generic.virtual.VirtualMotor',
                  description = 'Simulated HWB TTHS',
                  fmtstr = '%.2f',
                  unit = 'deg',
                  abslimits = (-3.1, 170),
                 ),
    omgs = device('devices.generic.virtual.VirtualMotor',
                  description = 'Simulated HWB OMGS',
                  fmtstr = '%.2f',
                  unit = 'deg',
                  abslimits = (-360, 360),
                 ),
#   omgm = device('devices.generic.virtual.VirtualMotor',
#                 description = 'Simulated HWB OMGM',
#                 fmtstr = '%.2f',
#                 unit = 'deg',
#                 abslimits = (-200, 200),
#                ),
#   tthm = device('devices.generic.virtual.VirtualMotor',
#                 description = 'virtual HWB TTHM',
#                 fmtstr = '%.2f',
#                 unit = 'deg',
#                 abslimits = (-200, 200),
#                ),
    mon1 = device('devices.generic.virtual.VirtualCounter',
                  description = 'Simulated HWB MON1',
                  fmtstr = '%d',
                  type = 'monitor',
                  lowlevel = True,
                 ),
    mon2 = device('devices.generic.virtual.VirtualCounter',
                  description = 'Simulated HWB MON2',
                  fmtstr = '%d',
                  type = 'monitor',
                  lowlevel = True,
                 ),
    tim1 = device('devices.generic.virtual.VirtualTimer',
                  description = 'Simulated HWB TIM1',
                  fmtstr = '%.2f',
                  unit = 's',
                  lowlevel = True,
                 ),
    image = device('devices.generic.virtual.VirtualImage',
                   description = 'Image data device',
                   fmtstr = '%d',
                   pollinterval = 86400,
                   lowlevel = True,
                   # sizes = (15, 16),
                   sizes = (80, 256),
                  ),
#   histogram = device('frm2.qmesydaqsinks.HistogramFileFormat',
#                      description = 'Histogram data written via QMesyDAQ',
#                      image = 'image',
#                     ),
#   listmode = device('frm2.qmesydaqsinks.ListmodeFileFormat',
#                     description = 'Listmode data written via QMesyDAQ',
#                     image = 'image',
#                    ),
    basedet = device('devices.generic.Detector',
                     description = 'Classical detector with single channels',
                     timers = ['tim1'],
                     monitors = ['mon1'],
                     counters = [],
                     images = ['image'],
                     maxage = 86400,
                     pollinterval = None,
#                    fileformats = ['listmode', 'histogram',],
                     lowlevel = True,
                    ),
    adet = device('spodi.detector.Detector',
                  description = 'Scanning (resolution steps) detector',
                  motor = 'tths',
                  detector = 'basedet',
                  pollinterval = None,
                  maxage = 86400,
                  liveinterval = 1,
                 ),
    wav = device('devices.generic.manual.ManualMove',
                 description = 'The incoming wavelength',
                 default = 1.7,
                 fmtstr = '%.2f',
                 unit = 'AA',
                 abslimits = (0.9, 2.5),
                ),
    spodisink = device('spodi.datasinks.CaressHistogram',
                       description = 'SPODI specific histogram file format',
                       lowlevel = True,
                       filenametemplate = ['m1%(pointcounter)08d.ctxt'],
                      ),
#   hv1   = device('devices.generic.virtual.VirtualMotor',
#                  description = 'ISEG HV power supply 1',
#                  requires = {'level': 'admin'},
#                  abslimits = (0, 3200),
#                  speed = 2,
#                  fmtstr = '%.1f',
#                  unit = 'V',
#                 ),
#   hv2   = device('devices.generic.virtual.VirtualMotor',
#                  description = 'ISEG HV power supply 2',
#                  requires = {'level': 'admin'},
#                  abslimits = (-2500, 0),
#                  speed = 2,
#                  fmtstr = '%.1f',
#                  unit = 'V',
#                 ),
)

display_order = 40

startupcode = '''
SetDetectors(adet)
'''
