# -*- coding: utf-8 -*-

description = "Detector data acquisition setup"
group = "lowlevel"

includes = ['counter']
excludes = ['virtual_daq']

sysconfig = dict(
    datasinks = ['kwsformat', 'yamlformat'],
)

tango_base = "tango://phys.kws1.frm2:10000/kws1/"

devices = dict(
    rtswitch   = device('devices.tango.DigitalOutput',
                        tangodevice = tango_base + 'fzjdp_digital/rtswitch',
                        lowlevel = True,
                       ),

    det_img    = device('kws1.daq.JDaqChannel',
                        description = 'Image for the large KWS detector',
                        tacodevice = '//phys.kws1.frm2/kws1/jdaq/1',
                        rtswitch = 'rtswitch',
                       ),

    kwsformat  = device('kws1.kwsfileformat.KWSFileSink',
                        lowlevel = True,
                       ),

    yamlformat = device('kws1.yamlformat.YAMLFileSink',
                        lowlevel = True,
                       ),

    det        = device('kws1.daq.KWSDetector',
                        description = 'KWS detector',
                        timers = ['timer'],
                        monitors = ['mon1', 'mon2', 'mon3', 'selctr'],
                        images = ['det_img'],
                        others = ['freq'],
                        shutter = 'shutter',
                       ),
)

extended = dict(
    poller_cache_reader = ['shutter'],
)
