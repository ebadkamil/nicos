description = 'QMesyDAQ detector devices'

group = 'lowlevel'

nameservice = 'spodisrv.spodi.frm2'
caresspath = '/opt/caress'
toolpath = '/opt/caress'

includes = []

nethost = 'spodisrv.spodi.frm2'

devices = dict(

#   mon1 = device('devices.vendor.qmesydaq.taco.Counter',
#                 description = 'QMesyDAQ Counter0',
#                 tacodevice = '//%s/test/qmesydaq/counter0' % nethost,
#                 type = 'monitor',
#                ),
#   mon2 = device('devices.vendor.qmesydaq.taco.Counter',
#                 description = 'QMesyDAQ Counter1',
#                 tacodevice = '//%s/test/qmesydaq/counter1' % nethost,
#                 type = 'monitor',
#                ),
#   timer = device('devices.vendor.qmesydaq.taco.Timer',
#                  description = 'QMesyDAQ Timer',
#                  tacodevice = '//%s/test/qmesydaq/timer' % nethost,
#                 ),
#   ctrs   = device('devices.vendor.qmesydaq.taco.Image',
#                   description = 'QMesyDAQ MultiChannel Detector',
#                   tacodevice = '//%s/test/qmesydaq/det' % nethost,
#                  ),
#   qm_det  = device('devices.generic.Detector',
#                    description = 'QMesyDAQ Detector',
#                    timers = ['timer'],
#                    counters = [],
#                    monitors = ['mon1', 'mon2'],
#                    images = ['ctrs'],
#                    fileformats = [],
#                    subdir = '',
#                   ),

    mon = device('devices.vendor.qmesydaq.caress.Counter',
                 description = 'HWB MON',
                 fmtstr = '%d',
                 type = 'monitor',
                 nameserver = '%s' % (nameservice,),
                 config = 'MON 500 qmesydaq.caress_object monitor1',
                 caresspath = caresspath,
                 toolpath = toolpath,
                 lowlevel = True,
                 absdev = False,
                ),
    tim1 = device('devices.vendor.qmesydaq.caress.Timer',
                  description = 'HWB TIM1',
                  fmtstr = '%.2f',
                  unit = 's',
                  nameserver = '%s' % (nameservice,),
                  config = 'TIM1 500 qmesydaq.caress_object timer 1',
                  caresspath = caresspath,
                  toolpath = toolpath,
                  lowlevel = True,
                  absdev = False,
                 ),
    image = device('devices.vendor.qmesydaq.caress.Image',
                   description = 'Image data device',
                   fmtstr = '%d',
                   pollinterval = None,
                   nameserver = '%s' % (nameservice,),
                   caresspath = caresspath,
                   toolpath = toolpath,
                   config = 'HISTOGRAM 500 qmesydaq.caress_object histogram 0'
                            ' 80 256',
                   lowlevel = True,
                   absdev = False,
                  ),
    basedet = device('devices.generic.Detector',
                     description = 'Classical detector with single channels',
                     timers = ['tim1'],
                     monitors = ['mon'],
                     counters = [],
                     images = ['image'],
                     pollinterval = None,
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
    # histogram = device('frm2.qmesydaqsinks.HistogramSink',
    #                    description = 'Histogram data written via QMesyDAQ',
    #                    image = 'image',
    #                   ),
    # listmode = device('frm2.qmesydaqsinks.ListmodeSink',
    #                   description = 'Listmode data written via QMesyDAQ',
    #                   image = 'image',
    #                  ),
)
