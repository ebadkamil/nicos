description = 'virtual SANS devices'
group = 'basic'

sysconfig = dict(
    instrument = 'sans',
    datasinks = ['BerSANSImageSink', 'RawImageSink',
                 'LivePNGSinkLog', 'LivePNGSink',
                 'filesink',
                ],
)

excludes = ['detector', 'qmchannel']
includes = ['cryo', 'source']

devices = dict(
    Sample   = device('nicos_mlz.sans1.devices.sans1_sample.Sans1Sample',
                      description = 'sample object',
                     ),

    sans     = device('nicos.devices.instrument.Instrument',
                      description = 'instrument object',
                      responsible = 'R. Esponsible <r.esponsible@frm2.tum.de>',
                      instrument = 'SANS-V2',
                      website = 'http://www.nicos-controls.org',
                      operators = ['NICOS developer team'],
                      facility = 'NICOS demo instruments',
                     ),

    guide_m1  = device('nicos.devices.generic.VirtualMotor',
                       lowlevel = True,
                       abslimits = (0, 10),
                       speed = 0.5,
                       unit = 'mm',
                      ),
    guide1    = device('nicos.devices.generic.Switcher',
                       lowlevel = True,
                       moveable = 'guide_m1',
                       mapping = {'off': 0, 'ng': 3, 'P3': 6, 'P4': 9},
                       precision = 0,
                       blockingmove = False,
                      ),
    guide_m2  = device('nicos.devices.generic.VirtualMotor',
                       lowlevel = True,
                       abslimits = (0, 10),
                       speed = 0.5,
                       unit = 'mm',
                      ),
    guide2    = device('nicos.devices.generic.Switcher',
                       lowlevel = True,
                       moveable = 'guide_m2',
                       mapping = {'off': 0, 'ng': 3, 'P3': 6, 'P4': 9},
                       precision = 0,
                       blockingmove = False,
                      ),
    guide_m3  = device('nicos.devices.generic.VirtualMotor',
                       lowlevel = True,
                       abslimits = (0, 10),
                       speed = 0.5,
                       unit = 'mm',
                      ),
    guide3    = device('nicos.devices.generic.Switcher',
                       lowlevel = True,
                       moveable = 'guide_m3',
                       mapping = {'off': 0, 'ng': 3, 'P3': 6, 'P4': 9},
                       precision = 0,
                       blockingmove = False,
                      ),
    guide_m4  = device('nicos.devices.generic.VirtualMotor',
                       lowlevel = True,
                       abslimits = (0, 10),
                       speed = 0.5,
                       unit = 'mm',
                      ),
    guide4    = device('nicos.devices.generic.Switcher',
                       lowlevel = True,
                       moveable = 'guide_m4',
                       mapping = {'off': 0, 'ng': 3, 'P3': 6, 'P4': 9},
                       precision = 0,
                       blockingmove = False,
                      ),
    guide     = device('nicos.devices.generic.MultiSwitcher',
                       description = 'neutron guide switcher for collimation',
                       moveables = ['guide1', 'guide2', 'guide3', 'guide4'],
                       fallback = 'unknown',
                       mapping = {'off': ['off', 'off', 'off', 'off'],
                                  '1m':  ['off', 'off', 'off', 'ng' ],
                                  '2m':  ['off', 'off', 'ng',  'ng' ],
                                  '4m':  ['off', 'ng',  'ng',  'ng' ],
                                  '6m':  ['ng',  'ng',  'ng',  'ng' ],
                                  'P3':  ['P3',  'P3',  'P3',  'P3' ],
                                  'P4':  ['P4',  'P4',  'P4',  'P4' ],
                                  },
                       precision = [None],
                      ),

    coll_m    = device('nicos.devices.generic.VirtualMotor',
                       lowlevel = True,
                       abslimits = (0, 10),
                       speed = 1,
                       unit = 'deg',
                      ),
    coll      = device('nicos.devices.generic.Switcher',
                       description = 'collimation',
                       moveable = 'coll_m',
                       mapping = {'off': 0,
                                  '10m': 2,
                                  '15m': 4,
                                  '20m': 8},
                       precision = 0,
                      ),

    st1_x      = device('nicos.devices.generic.VirtualMotor',
                        description = 'sample table position',
                        abslimits = (-50, 50),
                        speed = 1,
                        unit = 'mm',
                        curvalue = 1,
                        fmtstr = '%.1f',
                       ),

    det1_z     = device('nicos.devices.generic.VirtualMotor',
                        description = 'detector1 position in the tube',
                        abslimits = (0, 21),
                        speed = 1,
                        unit = 'm',
                        curvalue = 1,
                        fmtstr = '%.1f',
                       ),

    det1_x     = device('nicos.devices.generic.VirtualMotor',
                        description = 'horizontal offset of detector inside tube',
                        abslimits = (-1, 5),
                        speed = 0.5,
                        unit = 'm',
                        curvalue = 0,
                       ),

    det1_omega = device('nicos.devices.generic.VirtualMotor',
                        description = 'tilt of detector',
                        abslimits = (-40, 40),
                        speed = 0.5,
                        unit = 'deg',
                        curvalue = 0,
                        fmtstr = '%.1f',
                       ),

    det_pos2   = device('nicos.devices.generic.VirtualMotor',
                        description = 'detector2 position in the tube',
                        abslimits = (1, 22),
                        speed = 0.5,
                        unit = 'm',
                        curvalue = 10,
                       ),

    BerSANSImageSink  = device('nicos_mlz.sans1.devices.bersans.BerSANSImageSink',
                               description = 'Saves image data in BerSANS format',
                               filenametemplate = ['D%(pointcounter)s.001',
                               '/%(proposal)s_%(pointcounter)s_%(pointnumber)s.bersans'],
                              ),
    RawImageSink      = device('nicos.devices.datasinks.RawImageSink',
                               description = 'Saves image data in RAW format',
                               filenametemplate = ['%(proposal)s_%(pointcounter)s.raw',
                               '%(proposal)s_%(scancounter)s_'
                               '%(pointcounter)s_%(pointnumber)s.raw'],
                              ),
    LivePNGSinkLog   = device('nicos.devices.datasinks.PNGLiveFileSink',
                              description = 'Saves live image as .png every now and then',
                              filename = 'data/live_log.png',
                              log10 = True,
                              interval = 1,
                             ),
    LivePNGSink      = device('nicos.devices.datasinks.PNGLiveFileSink',
                              description = 'Saves live image as .png every now and then',
                              filename = 'data/live_lin.png',
                              log10 = False,
                              interval = 1,
                             ),

    det1_timer = device('nicos.devices.generic.VirtualTimer',
                        description = 'demo timer',
                       ),
    det1_mon1 = device('nicos.devices.generic.VirtualCounter',
                       description = 'demo monitor',
                       type = 'monitor',
                      ),
    det1_mon2 = device('nicos.devices.generic.VirtualCounter',
                       description = 'demo monitor',
                       type = 'monitor',
                      ),
    det1_img  = device('nicos.devices.generic.VirtualImage',
                       description = 'demo 2D detector',
                       distance = 'det1_z',
                       collimation = 'guide',
                       sizes = (128, 128),
                      ),
    det      = device('nicos.devices.generic.GatedDetector',
                      description = 'demo 2D detector',
                      timers = ['det1_timer'],
                      monitors = ['det1_mon1', 'det1_mon2'],
                      images = ['det1_img'],
                     ),

    det_HV   = device('nicos.devices.generic.VirtualMotor',
                      description = 'high voltage at the detector',
                      requires = {'level': 'admin'},
                      abslimits = (0, 1000),
                      warnlimits = (990, 1010),
                      unit = 'V',
                      curvalue = 1000,
                      speed = 10,
                     ),

    scandet = device('nicos.devices.generic.VirtualScanningDetector',
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
