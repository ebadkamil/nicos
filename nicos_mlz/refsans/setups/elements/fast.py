description = 'devices for fast detector using comtec p7888 for REFSANS'

# to be included by refsans?
group = 'lowlevel'

nethost = 'refsanssrv.refsans.frm2'
tacodev = '//%s/test/fast' % nethost

sysconfig = dict(
    # datasinks = ['comtec_sink'],
    datasinks = ['RawFileSaver'],
)

devices = dict(
    fastctr_a = device('nicos.devices.taco.detector.FRMCounterChannel',
    # fastctr_a = device('nicos_mlz.refsans.devices.detector.ComtecCounter',
        description = "Channel A of Comtep P7888 Fast Counter",
        tacodevice = '%s/rate_a' % tacodev,
        type = 'counter',
        mode = 'normal',
        # lowlevel = True,
    ),
    fastctr_b = device('nicos.devices.taco.detector.FRMCounterChannel',
    # fastctr_b = device('nicos_mlz.refsans.devices.detector.ComtecCounter',
        description = "Channel B of Comtep P7888 Fast Counter",
        tacodevice = '%s/rate_b' % tacodev,
        type = 'counter',
        mode = 'normal',
        # lowlevel = True,
    ),
    fastctr_c = device('nicos.devices.taco.detector.FRMCounterChannel',
    # fastctr_c = device('nicos_mlz.refsans.devices.detector.ComtecCounter',
        description = "Channel C of Comtep P7888 Fast Counter",
        tacodevice = '%s/rate_c' % tacodev,
        type = 'counter',
        mode = 'normal',
        # lowlevel = True,
    ),
    fastctr_d = device('nicos.devices.taco.detector.FRMCounterChannel',
    # fastctr_d = device('nicos_mlz.refsans.devices.detector.ComtecCounter',
        description = "Channel D of Comtep P7888 Fast Counter",
        tacodevice = '%s/rate_d' % tacodev,
        type = 'counter',
        mode = 'normal',
        # lowlevel = True,
    ),
    fastctr_e = device('nicos.devices.taco.detector.FRMCounterChannel',
    # fastctr_e = device('nicos_mlz.refsans.devices.detector.ComtecCounter',
        description = "Channel E of Comtep P7888 Fast Counter",
        tacodevice = '%s/rate_e' % tacodev,
        type = 'counter',
        mode = 'normal',
        # lowlevel = True,
    ),
    fastctr_f = device('nicos.devices.taco.detector.FRMCounterChannel',
    # fastctr_f = device('nicos_mlz.refsans.devices.detector.ComtecCounter',
        description = "Channel F of Comtep P7888 Fast Counter",
        tacodevice = '%s/rate_f' % tacodev,
        type = 'counter',
        mode = 'normal',
        # lowlevel = True,
    ),
    fastctr_g = device('nicos.devices.taco.detector.FRMCounterChannel',
    # fastctr_g = device('nicos_mlz.refsans.devices.detector.ComtecCounter',
        description = "Channel G of Comtep P7888 Fast Counter",
        tacodevice = '%s/rate_g' % tacodev,
        type = 'counter',
        mode = 'normal',
        # lowlevel = True,
    ),
    fastctr_h = device('nicos.devices.taco.detector.FRMCounterChannel',
    # fastctr_h = device('nicos_mlz.refsans.devices.detector.ComtecCounter',
        description = "Channel H of Comtep P7888 Fast Counter",
        tacodevice = '%s/rate_h' % tacodev,
        type = 'counter',
        mode = 'normal',
        # lowlevel = True,
    ),
    comtec_sink = device('nicos_mlz.refsans.devices.detector.ComtecHeaderSink',
        description = 'Copies image data and saves header',
        detector = 'comtec_timer',
        fast_basepaths = ['/home/refsans-mca','/home/refsans-mcb'],
    ),
    RawFileSaver = device('nicos.devices.datasinks.SingleRawImageSink',
        description = 'Saves image data in RAW format',
        filenametemplate = [
            '%(proposal)s_%(pointcounter)s.raw', '%(proposal)s_%(scancounter)s'
            '_%(pointcounter)s_%(pointnumber)s.raw'
        ],
    ),
    comtec_timer = device('nicos_mlz.refsans.devices.detector.ComtecTimer',
        description = 'Comtec P7888 Fast System: Timer channel',
        tacodevice = '%s/detector' % tacodev,
    ),
    comtec_filename = device('nicos_mlz.refsans.devices.detector.ComtecFilename',
        description = 'Comtec P7888 Fast System: filename',
        tacodevice = '%s/detector' % tacodev,
        lowlevel = True,
    ),
    comtec = device('nicos.devices.generic.Detector',
        description = "detector, joining all channels",
        timers = ['comtec_timer'],
        images = [],
        # counters = ['fastctr_%c'%c for c in 'abcdefgh'],
        # others = ['comtec_filename'],
    ),
    # the following may not work as expected ! (or at all!)
    # comtec = device('nicos.devices.vendor.qmesydaq.QMesyDAQImage',
    #     description = 'Comtep P7888 Fast Counter Main detector device',
    #     tacodevice = '%s/detector' % tacodev,
    #     events = None,
    #     timer = None,
    #     counters = ['fastctr_a','fastctr_b','fastctr_c','fastctr_d',
    #     'fastctr_e','fastctr_f','fastctr_g','fastctr_h'],
    #     monitors = None,
    #     fileformats = ['RawFileSaver'],
    #     subdir = 'fast',
    # ),
)

startupcode = '''
# SetDetectors(comtec)
'''
