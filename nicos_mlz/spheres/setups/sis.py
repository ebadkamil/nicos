# -*- coding: utf-8 -*-

description = 'SIS detector setup'

includes = ['timer', 'shutter', 'sample']

sysconfig = dict(datasinks = ['sisasink', 'sisusink', 'sislive'])

tangohost = 'phys.spheres.frm2'
sis = 'tango://%s:10000/spheres/sis/' % tangohost

basename = '%(proposal)s_%(session.experiment.sample.filename)s_'

devices = dict(
    sis = device('nicos_mlz.spheres.devices.sisdetector.SISDetector',
        description = 'detector',
        timers = ['timer'],
        images = ['sisimg'],
        shutter = 'shutter',
        liveinterval = 1.,
        autoshutter = True,
    ),
    sisimg = device('nicos_mlz.spheres.devices.sisdetector.SISChannel',
        description = 'SIS detector',
        tangodevice = sis + 'counter',
        analyzers = 'Si111',
        monochromator = 'Si111',
        incremental = False,
    ),
    sisasink = device('nicos_mlz.spheres.devices.sissinks.AFileSink',
        description = 'DataSink which writes raw data',
        detectors = ['sis'],
        subdir = 'raw',
        filenametemplate = [basename + '%(scancounter)da%(pointnumber)d'],
    ),
    sisusink = device('nicos_mlz.spheres.devices.sissinks.UFileSink',
        description = 'DataSink which writes user data',
        detectors = ['sis'],
        subdir = 'user',
        filenametemplate = [basename + '%(scancounter)du%(pointnumber)d'],
        setpointdev = 'setpoint',
        envcontroller = 'c_temperature',
    ),
    sislive = device('nicos_mlz.spheres.devices.sissinks.PreviewSink',
        description = 'Sends image data to LiveViewWidget',
        detectors = ['sis'],
    ),
    flux=device('nicos_mlz.spheres.devices.flux.Flux',
        description='Device which stores averages of the regular detectors '
                    'of direct, elastic and inelastic flux',
        tangodevice=sis + 'counter',
    ),
)