description = 'virtual SANS devices'
group = 'basic'

sysconfig = dict(
    instrument = 'sans',
    datasinks = ['conssink', 'filesink', 'serialsink', 'livesink', 'dmnsink',
                 'BerSANSImageSink', 'RawImageSink',
                 'LivePNGSinkLog', 'LivePNGSink'],
)

modules = ['sans1.commands']

excludes = ['tas', 'refsans', 'detector', 'qmchannel']
includes = ['cryo']

devices = dict(
    Sample   = device('sans1.sans1_sample.Sans1Sample',
                      description = 'sample object',
                     ),

    sans     = device('devices.instrument.Instrument',
                      description = 'instrument object',
                      responsible = 'R. Esponsible <r.esponsible@frm2.tum.de>',
                      instrument = 'SANS-V2',
                      website = 'http://www.nicos-controls.org',
                      operators = ['NICOS developer team', ],
                      facility = 'NICOS demo instruments',
                     ),

    guide_m1  = device('devices.generic.VirtualMotor',
                       lowlevel = True,
                       abslimits = (0, 10),
                       speed = 0.5,
                       unit = 'mm',
                      ),
    guide1    = device('devices.generic.Switcher',
                       lowlevel = True,
                       moveable = 'guide_m1',
                       mapping = {'off': 0, 'ng': 3, 'P3': 6, 'P4': 9},
                       precision = 0,
                       blockingmove = False,
                      ),
    guide_m2  = device('devices.generic.VirtualMotor',
                       lowlevel = True,
                       abslimits = (0, 10),
                       speed = 0.5,
                       unit = 'mm',
                      ),
    guide2    = device('devices.generic.Switcher',
                       lowlevel = True,
                       moveable = 'guide_m2',
                       mapping = {'off': 0, 'ng': 3, 'P3': 6, 'P4': 9},
                       precision = 0,
                       blockingmove = False,
                      ),
    guide_m3  = device('devices.generic.VirtualMotor',
                       lowlevel = True,
                       abslimits = (0, 10),
                       speed = 0.5,
                       unit = 'mm',
                      ),
    guide3    = device('devices.generic.Switcher',
                       lowlevel = True,
                       moveable = 'guide_m3',
                       mapping = {'off': 0, 'ng': 3, 'P3': 6, 'P4': 9},
                       precision = 0,
                       blockingmove = False,
                      ),
    guide_m4  = device('devices.generic.VirtualMotor',
                       lowlevel = True,
                       abslimits = (0, 10),
                       speed = 0.5,
                       unit = 'mm',
                      ),
    guide4    = device('devices.generic.Switcher',
                       lowlevel = True,
                       moveable = 'guide_m4',
                       mapping = {'off': 0, 'ng': 3, 'P3': 6, 'P4': 9},
                       precision = 0,
                       blockingmove = False,
                      ),
    guide     = device('devices.generic.MultiSwitcher',
                       description = 'neutron guide switcher for collimation',
                       moveables = ['guide1', 'guide2', 'guide3', 'guide4'],
                       mapping = {'off': ['off', 'off', 'off', 'off'],
                                  '1m':  ['off', 'off', 'off', 'ng' ],
                                  '2m':  ['off', 'off', 'ng',  'ng' ],
                                  '4m':  ['off', 'ng',  'ng',  'ng' ],
                                  '6m':  ['ng',  'ng',  'ng',  'ng' ],
                                  'P3':  ['P3',  'P3',  'P3',  'P3' ],
                                  'P4':  ['P4',  'P4',  'P4',  'P4' ],
                                  },
                       precision = [None,],
                      ),

    coll_m    = device('devices.generic.VirtualMotor',
                       lowlevel = True,
                       abslimits = (0, 10),
                       speed = 1,
                       unit = 'deg',
                      ),
    coll      = device('devices.generic.Switcher',
                       description = 'collimation',
                       moveable = 'coll_m',
                       mapping = {'off': 0,
                                  '10m': 2,
                                  '15m': 4,
                                  '20m': 8},
                       precision = 0,
                      ),

    st1_x      = device('devices.generic.VirtualMotor',
                        description = 'sample table position',
                        abslimits = (-50, 50),
                        speed = 1,
                        unit = 'mm',
                        curvalue = 1,
                        fmtstr = '%.1f',
                       ),

    det1_z     = device('devices.generic.VirtualMotor',
                        description = 'detector1 position in the tube',
                        abslimits = (0, 21),
                        speed = 1,
                        unit = 'm',
                        curvalue = 1,
                        fmtstr = '%.1f',
                       ),

    det1_x     = device('devices.generic.VirtualMotor',
                        description = 'horizontal offset of detector inside tube',
                        abslimits = (-1, 5),
                        speed = 0.5,
                        unit = 'm',
                        curvalue = 0,
                       ),

    det1_omega = device('devices.generic.VirtualMotor',
                        description = 'tilt of detector',
                        abslimits = (-40, 40),
                        speed = 0.5,
                        unit = 'deg',
                        curvalue = 0,
                        fmtstr = '%.1f',
                       ),

    det_pos2   = device('devices.generic.VirtualMotor',
                        description = 'detector2 position in the tube',
                        abslimits = (1, 22),
                        speed = 0.5,
                        unit = 'm',
                        curvalue = 10,
                       ),

    BerSANSImageSink  = device('sans1.bersans.BerSANSImageSink',
                               description = 'Saves image data in BerSANS format',
                               filenametemplate = ['D%(pointcounter)s.001',
                               '/%(proposal)s_%(pointcounter)s_%(pointnumber)s.bersans'],
                               flipimage = 'none',
                              ),
    RawImageSink      = device('devices.datasinks.RawImageSink',
                               description = 'Saves image data in RAW format',
                               filenametemplate = ['%(proposal)s_%(pointcounter)s.raw',
                               '%(proposal)s_%(scancounter)s_'
                               '%(pointcounter)s_%(pointnumber)s.raw'],
                              ),
    LivePNGSinkLog   = device('devices.datasinks.PNGLiveFileSink',
                              description = 'Saves live image as .png every now and then',
                              filename = 'data/live_log.png',
                              log10 = True,
                              interval = 1,
                             ),
    LivePNGSink      = device('devices.datasinks.PNGLiveFileSink',
                              description = 'Saves live image as .png every now and then',
                              filename = 'data/live_lin.png',
                              log10 = False,
                              interval = 1,
                             ),

    det1_time = device('devices.generic.virtual.VirtualTimer',
                       description = 'demo timer',
                      ),
    det1_mon1 = device('devices.generic.virtual.VirtualCounter',
                       description = 'demo monitor',
                       type = 'monitor',
                      ),
    det1_mon2 = device('devices.generic.virtual.VirtualCounter',
                       description = 'demo monitor',
                       type = 'monitor',
                      ),
    det1_img  = device('devices.generic.virtual.VirtualImage',
                       description = 'demo 2D detector',
                       distance = 'det1_z',
                       collimation = 'guide',
                      ),
    det      = device('devices.generic.detector.Detector',
                      description = 'demo 2D detector',
                      timers = ['det1_time'],
                      monitors = ['det1_mon1', 'det1_mon2'],
                      images = ['det1_img'],
                     ),

    det_HV   = device('devices.generic.VirtualMotor',
                      description = 'high voltage at the detector',
                      requires = {'level': 'admin'},
                      abslimits = (0, 1000),
                      warnlimits = (990, 1010),
                      unit = 'V',
                      curvalue = 1000,
                      speed = 10,
                     ),

    scandet = device('devices.generic.virtual.VirtualScanningDetector',
                     description = 'Virtual SANS detector (HV depending moves)',
                     scandev = 'det_HV',
                     positions = [100, 200, 300],
                     detector = 'det'),
)

startupcode = '''
SetDetectors(det)
printinfo("============================================================")
printinfo("Welcome to the NICOS SANS demo setup.")
printinfo("Run count(1) to collect an image.")
printinfo("============================================================")
'''
